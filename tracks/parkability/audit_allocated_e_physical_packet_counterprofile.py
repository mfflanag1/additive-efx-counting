#!/usr/bin/env python3
"""Expand a packet-tail model and search full physical PI/EFX escapes."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


ROOT = Path(__file__).resolve().parents[2]


def expand(source):
    payload = json.loads(source.read_text())
    totals = {
        owner: {piece: Fraction(amount) for piece, amount in row.items()}
        for owner, row in payload["totals"].items()
    }
    least = {
        owner: {piece: Fraction(amount) for piece, amount in row.items()}
        for owner, row in payload["least_values"].items()
    }
    classes = payload["packet_cardinality_class"]
    expansion = {}
    values = {owner: {} for owner in OWNERS}
    for piece in GOODS:
        names = (piece,) if classes[piece] == "singleton" else (f"{piece}.0", f"{piece}.1")
        expansion[piece] = names
        for owner in OWNERS:
            if len(names) == 1:
                amounts = (totals[owner][piece],)
                assert totals[owner][piece] == least[owner][piece]
            else:
                amounts = (least[owner][piece], totals[owner][piece] - least[owner][piece])
                assert amounts[1] >= amounts[0] > 0
            values[owner].update(zip(names, amounts, strict=True))
    base = {
        owner: tuple(good for piece in pieces for good in expansion[piece])
        for owner, pieces in ALLOCATED_E_BASE.items()
    }
    support = {
        owner: tuple(good for piece in pieces for good in expansion[piece])
        for owner, pieces in SUPPORT_STATE.items()
    }
    return payload, expansion, values, base, support


def subset_tables(values, goods):
    size = 1 << len(goods)
    totals = {owner: [Fraction(0)] * size for owner in OWNERS}
    minima = {owner: [None] * size for owner in OWNERS}
    for mask in range(1, size):
        bit = mask & -mask
        index = bit.bit_length() - 1
        prior = mask ^ bit
        good = goods[index]
        for owner in OWNERS:
            amount = values[owner][good]
            totals[owner][mask] = totals[owner][prior] + amount
            old = minima[owner][prior]
            minima[owner][mask] = amount if old is None else min(old, amount)
    return totals, minima


def minimal_cores(values, goods):
    totals, minima = subset_tables(values, goods)
    result = {}
    for source in OWNERS:
        rows = []
        for mask in range(1, 1 << len(goods)):
            source_total = totals[source][mask]
            if source_total <= 1:
                continue
            if any(totals[observer][mask] - minima[observer][mask] > 1 for observer in OWNERS):
                continue
            # Common safety is deletion-monotone. Hence a common-safe desired
            # core is inclusion-minimal exactly when every one-good deletion
            # destroys source desire.
            if any(
                source_total - values[source][goods[index]] > 1
                for index in range(len(goods)) if mask & (1 << index)
            ):
                continue
            rows.append(mask)
        result[source] = tuple(rows)
    return result


def find_closed_disjoint_families(values, goods, base, minimum_size=1, maximum=None):
    cores = minimal_cores(values, goods)
    good_index = {good: index for index, good in enumerate(goods)}
    owner_mask = {
        owner: sum(1 << good_index[good] for good in rows)
        for owner, rows in base.items()
    }
    witnesses = []
    for size in range(minimum_size, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, size):
            allowed = owner_mask["charity"]
            for owner in subset:
                allowed |= owner_mask[owner]
            choices = {owner: tuple(mask for mask in cores[owner] if not mask & ~allowed)
                       for owner in subset}
            if any(not choices[owner] for owner in subset):
                continue
            order = tuple(sorted(subset, key=lambda owner: len(choices[owner])))

            def search(position, used, selected):
                if maximum is not None and len(witnesses) >= maximum:
                    return
                if position == len(order):
                    witnesses.append(dict(selected))
                    return
                owner = order[position]
                for mask in choices[owner]:
                    if not mask & used:
                        search(position + 1, used | mask, (*selected, (owner, mask)))
                        if maximum is not None and len(witnesses) >= maximum:
                            return

            search(0, 0, ())
            if maximum is not None and len(witnesses) >= maximum:
                break
        if maximum is not None and len(witnesses) >= maximum:
            break
    decoded = tuple({
        owner: [goods[index] for index in range(len(goods)) if mask & (1 << index)]
        for owner, mask in witness.items()
    } for witness in witnesses)
    return decoded, {owner: len(rows) for owner, rows in cores.items()}


def find_closed_disjoint_family(values, goods, base):
    witnesses, counts = find_closed_disjoint_families(
        values, goods, base, maximum=1,
    )
    return (witnesses[0] if witnesses else None), counts


def find_four_edge_efx(values, goods, support, timeout_seconds, random_seed):
    holder = {good: z3.Int(f"physical_holder_{index}") for index, good in enumerate(goods)}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    for variable in holder.values():
        solver.add(variable >= 0, variable < len(OWNERS))
    for target_index in range(len(OWNERS)):
        solver.add(z3.Or(*(holder[good] == target_index for good in goods)))
    utility = {}
    for observer in OWNERS:
        for target_index in range(len(OWNERS)):
            utility[observer, target_index] = z3.Sum(*(
                z3.If(holder[good] == target_index,
                      z3.RealVal(str(values[observer][good])), z3.RealVal(0))
                for good in goods
            ))
    for observer_index, observer in enumerate(OWNERS):
        own = utility[observer, observer_index]
        for target_index in range(len(OWNERS)):
            if target_index == observer_index:
                continue
            for good in goods:
                solver.add(z3.Implies(
                    holder[good] == target_index,
                    own >= utility[observer, target_index] - z3.RealVal(str(values[observer][good])),
                ))
    supplier = {good: owner for owner, rows in support.items() for good in rows}
    edge_atoms = []
    for source in support:
        for target_index, target in enumerate(OWNERS):
            if source == target:
                continue
            atom = z3.Bool(f"physical_edge_{source}_{target}")
            carried = [holder[good] == target_index for good in support[source]]
            solver.add(atom == z3.Or(*carried))
            edge_atoms.append(atom)
    solver.add(z3.Sum(*(z3.If(atom, 1, 0) for atom in edge_atoms)) <= 4)
    status = solver.check()
    if status != z3.sat:
        return str(status), None
    model = solver.model()
    allocation = {owner: [] for owner in OWNERS}
    for good in goods:
        allocation[OWNERS[model.eval(holder[good]).as_long()]].append(good)
    final = {good: owner for owner, rows in allocation.items() for good in rows}
    edges = sorted({(supplier[good], final[good]) for good in goods if supplier[good] != final[good]})
    return "sat", {"allocation": allocation, "edges": edges}


def run(source: Path, output: Path, timeout_seconds: int, random_seed: int):
    source = source.resolve()
    payload, expansion, values, base, support = expand(source)
    goods = tuple(good for piece in GOODS for good in expansion[piece])
    started = time.monotonic()
    pi, counts = find_closed_disjoint_family(values, goods, base)
    efx_status = None
    efx = None
    if pi is None:
        efx_status, efx = find_four_edge_efx(
            values, goods, support, timeout_seconds, random_seed,
        )
    result = {
        "schema": "allocated-e-physical-packet-counterprofile-audit-v1",
        "status": (
            "FULL_GENERALIZED_PI_FOUND" if pi is not None
            else "FOUR_EDGE_EFX_FOUND" if efx is not None
            else "NO_PI_OR_EFX_FOUND" if efx_status == "unsat"
            else "UNKNOWN"
        ),
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "physical_good_count": len(goods),
        "expansion": {piece: list(rows) for piece, rows in expansion.items()},
        "minimal_common_safe_desired_core_counts": counts,
        "generalized_pi_witness": pi,
        "efx_search_status": efx_status,
        "four_edge_efx_witness": efx,
        "elapsed_seconds": time.monotonic() - started,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact expansion of every named packet into one or two positive goods. "
            "A PI witness refutes only the seven-endpoint physical-tail selector, "
            "not the universal theorem. Absence of the searched objects would still "
            "require auditing all saturated fixed-U continuation premises."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=123457)
    args = parser.parse_args()
    result = run(args.source, args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "physical_goods": result["physical_good_count"],
        "core_counts": result["minimal_common_safe_desired_core_counts"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
