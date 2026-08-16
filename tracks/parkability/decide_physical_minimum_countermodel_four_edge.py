#!/usr/bin/env python3
"""Decide the four-support-edge EFX gate for a physical-minimum profile.

The totals/minima profile is realized canonically: a singleton role becomes
one good, while a multi-good role becomes two goods of values M and T-M for
every observer.  The Boolean allocation encoding then ranges over *every*
assignment of those physical goods to the four owners under at most four
distinct support-supplier/recipient pairs.  Thus UNSAT is an exact refutation
of the local four-edge conclusion for the concrete physical profile; SAT
returns a complete EFX allocation and minimizes the number of roles split
between recipients.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


def q(value: Fraction):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_physical_profile(path: Path):
    raw = json.loads(path.read_text())
    totals = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_totals"].items()
    }
    minima = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_minima"].items()
    }
    physical = {}
    role_goods = {}
    for role in GOODS:
        singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        names = (f"{role}:0",) if singleton else (f"{role}:0", f"{role}:1")
        role_goods[role] = names
        for observer in OWNERS:
            physical[observer, names[0]] = minima[observer][role]
            if not singleton:
                physical[observer, names[1]] = (
                    totals[observer][role] - minima[observer][role]
                )
                assert physical[observer, names[1]] >= physical[observer, names[0]] > 0
    return raw, totals, minima, physical, role_goods


def support_supplier():
    return {
        role: supplier
        for supplier, roles in SUPPORT_STATE.items()
        for role in roles
    }


def build_decision(physical, role_goods, split_cap=None, edge_cap=4):
    goods = tuple(g for role in GOODS for g in role_goods[role])
    supplier = support_supplier()
    x = {(g, owner): z3.Bool(f"x_{g.replace(':', '_')}_{owner}")
         for g in goods for owner in OWNERS}
    edges = {
        (source, target): z3.Bool(f"edge_{source}_{target}")
        for source in SUPPORT_STATE
        for target in OWNERS
        if source != target
    }
    solver = z3.Solver()
    for g in goods:
        solver.add(z3.PbEq([(x[g, owner], 1) for owner in OWNERS], 1))
        role = g.split(":", 1)[0]
        source = supplier[role]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[g, target], edges[source, target]))
    solver.add(z3.PbLe([(edge, 1) for edge in edges.values()], edge_cap))

    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[g, target], q(physical[observer, g]), z3.RealVal(0))
            for g in goods
        ))
        for observer in OWNERS for target in OWNERS
    }
    # EFX means the inequality holds after deleting every individual good in
    # the target bundle.  The implication scopes deletion to assigned goods.
    for observer in OWNERS:
        own = utility[observer, observer]
        for target in OWNERS:
            if target == observer:
                continue
            for g in goods:
                solver.add(z3.Implies(
                    x[g, target],
                    own >= utility[observer, target] - q(physical[observer, g]),
                ))

    split = {}
    for role, members in role_goods.items():
        if len(members) == 1:
            continue
        g0, g1 = members
        split[role] = z3.Or(*(
            z3.And(x[g0, left], x[g1, right])
            for left in OWNERS for right in OWNERS if left != right
        ))
    if split_cap is not None:
        solver.add(z3.PbLe([(flag, 1) for flag in split.values()], split_cap))
    return solver, x, edges, split, goods


def exact_audit(allocation, physical, supplier, edge_cap):
    edges = {
        (supplier[g.split(":", 1)[0]], owner)
        for owner, goods in allocation.items()
        for g in goods
        if supplier[g.split(":", 1)[0]] != owner
    }
    assert len(edges) <= edge_cap
    for observer in OWNERS:
        own = sum((physical[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            total = sum((physical[observer, g] for g in allocation[target]), Fraction())
            for g in allocation[target]:
                assert own >= total - physical[observer, g]
    return sorted(edges)


def run(input_path: Path, output_path: Path, edge_cap: int, timeout_seconds: int):
    raw, _, _, physical, role_goods = load_physical_profile(input_path)
    attempts = []
    terminal = None
    for split_cap in range(0, sum(len(v) == 2 for v in role_goods.values()) + 1):
        solver, x, edges, split, goods = build_decision(
            physical, role_goods, split_cap=split_cap, edge_cap=edge_cap
        )
        solver.set(timeout=timeout_seconds * 1000)
        status = solver.check()
        attempt = {"split_cap": split_cap, "status": str(status)}
        if status == z3.unknown:
            attempt["reason_unknown"] = solver.reason_unknown()
        attempts.append(attempt)
        if status == z3.sat:
            model = solver.model()
            allocation = {
                owner: [g for g in goods if z3.is_true(model.eval(x[g, owner]))]
                for owner in OWNERS
            }
            used_edges = exact_audit(allocation, physical, support_supplier(), edge_cap)
            split_roles = [
                role for role, flag in split.items() if z3.is_true(model.eval(flag))
            ]
            terminal = {
                "allocation": allocation,
                "used_edges": [list(edge) for edge in used_edges],
                "split_roles": split_roles,
                "physical_values": {
                    observer: {g: str(physical[observer, g]) for g in goods}
                    for observer in OWNERS
                },
            }
            break
        if status == z3.unknown:
            break

    result = {
        "schema": "physical-minimum-concrete-four-edge-decision-v1",
        "status": (
            "SAT_COMPLETE_EFX_SPLIT_REPAIR" if terminal is not None
            else ("UNKNOWN" if attempts[-1]["status"] == "unknown"
                  else "UNSAT_CONCRETE_FOUR_EDGE_COUNTERMODEL")
        ),
        "source_profile": str(input_path),
        "source_profile_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "source_profile_status": raw["status"],
        "edge_cap": edge_cap,
        "edge_origin": "support",
        "physical_good_count": sum(map(len, role_goods.values())),
        "singleton_roles": [role for role, gs in role_goods.items() if len(gs) == 1],
        "two_good_roles": [role for role, gs in role_goods.items() if len(gs) == 2],
        "attempts": attempts,
        "terminal": terminal,
        "claim_boundary": (
            "Exact for the canonical physical realization of this exact-response "
            "form-2 profile and all complete allocations using at most the declared "
            "number of support-supplier/recipient pairs. It does not by itself "
            "establish chart coverage or the universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(args.input, args.output, args.edge_cap, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "attempts": result["attempts"],
        "split_roles": (
            result["terminal"]["split_roles"] if result["terminal"] else None
        ),
        "used_edges": result["terminal"]["used_edges"] if result["terminal"] else None,
    }, indent=2))


if __name__ == "__main__":
    main()
