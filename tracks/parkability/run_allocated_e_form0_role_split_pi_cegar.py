#!/usr/bin/env python3
"""Exact generalized-PI CEGAR for a maximally role-split R2 cell.

The twelve named provenance atoms in the original allocated-E form-R2
master are split at the three load-bearing response witnesses r->q, q->r,
and s->d.  Both sides of every split are required to be nonempty (all item
values are strictly positive).  The generalized-PI oracle is a binary LRA
set-packing model, so it does not enumerate all 2^21 bundles.

This is a finite adversarial strengthening, not a cap-free reduction: an
arbitrary physical packet may still contain further EFX-critical splits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")

# Each original atom in A+H, Q, or W is split by membership in the fixed
# witness core aimed at that current target. E and P are not response targets
# in the numerical core and remain unsplit.
ORIGINAL = (
    ("a0", "r", "A", "q"),
    ("a1", "q", "A", "q"),
    ("h", "d", "H", "q"),
    ("j", "q", "Q", "r"),
    ("k", "d", "Q", "r"),
    ("q0", "d", "Q", "r"),
    ("l", "d", "E", None),
    ("e", "s", "E", None),
    ("m", "r", "W", "s"),
    ("gq", "q", "W", "s"),
    ("gr", "charity", "W", "s"),
    ("p", "s", "P", None),
)


def split_name(name: str, inside: bool) -> str:
    return f"{name}_{'in' if inside else 'out'}"


GOODS = tuple(
    split_name(name, inside) if response_source is not None else name
    for name, _, _, response_source in ORIGINAL
    for inside in ((True, False) if response_source is not None else (True,))
)

BASE_OWNER = {
    (split_name(name, inside) if response_source is not None else name): owner
    for name, owner, _, response_source in ORIGINAL
    for inside in ((True, False) if response_source is not None else (True,))
}

PACKET = {
    packet: tuple(
        good for good in GOODS
        if next(row[2] for row in ORIGINAL if good == row[0] or good.startswith(row[0] + "_")) == packet
    )
    for packet in ("A", "H", "Q", "E", "W", "P")
}

BASE = {
    owner: tuple(good for good in GOODS if BASE_OWNER[good] == owner)
    for owner in (*OWNERS, "charity")
}

SUPPORT = {
    "r": (*PACKET["A"], *PACKET["H"]),
    "q": PACKET["Q"],
    "d": PACKET["W"],
    "s": PACKET["E"],
    "charity": PACKET["P"],
}

CURRENT_HOLDER = {
    good: holder for holder, goods in SUPPORT.items() for good in goods
}

RESPONSE_CORE = {
    source: tuple(
        split_name(name, True)
        for name, _, _, response_source in ORIGINAL
        if response_source == source
    )
    for source in ("r", "q", "s")
}


def total(value, observer, goods):
    terms = tuple(value[good, observer] for good in goods)
    return z3.Sum(*terms) if terms else z3.RealVal(0)


def tail_constraints(value, observer, goods, floor, present=None):
    goods = tuple(goods)
    if len(goods) <= 1:
        return ()
    rows = tuple(
        total(value, observer, (g for g in goods if g != removed)) <= floor
        for removed in goods
    )
    if present is None:
        return rows
    return tuple(
        z3.Implies(present[removed], row)
        for removed, row in zip(goods, rows, strict=True)
    )


def base_response(value, source, goods, present=None):
    goods = tuple(goods)
    return z3.And(
        total(value, source, goods) > 1,
        *(constraint
          for observer in OWNERS
          for constraint in tail_constraints(
              value, observer, goods, 1, present=present
          )),
    )


def current_response(value, source, goods, present=None):
    goods = tuple(goods)
    current = {owner: total(value, owner, SUPPORT[owner]) for owner in OWNERS}
    return z3.And(
        total(value, source, goods) > current[source],
        *(constraint
          for observer in OWNERS
          for constraint in tail_constraints(
              value, observer, goods, current[observer], present=present
          )),
    )


def build_master():
    value = {
        (good, observer): z3.Real(f"rs_v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    present = {good: z3.Bool(f"rs_present_{good}") for good in GOODS}
    solver = z3.SolverFor("QF_LRA")
    for good in GOODS:
        for observer in OWNERS:
            solver.add(z3.If(
                present[good], value[good, observer] > 0,
                value[good, observer] == 0,
            ))
    for name, _, _, response_source in ORIGINAL:
        if response_source is None:
            solver.add(present[name])
        else:
            solver.add(z3.Or(
                present[split_name(name, True)],
                present[split_name(name, False)],
            ))

    for owner in OWNERS:
        solver.add(total(value, owner, BASE[owner]) == 1)
        solver.add(total(value, owner, BASE["charity"]) <= 1)
        for target in OWNERS:
            if target == owner:
                continue
            solver.add(*tail_constraints(
                value, owner, BASE[target], 1, present=present
            ))

    # Three selected retained cores and the d->Q base response.
    solver.add(base_response(value, "r", PACKET["A"], present))
    solver.add(base_response(value, "q", PACKET["Q"], present))
    solver.add(base_response(value, "s", PACKET["E"], present))
    solver.add(base_response(value, "d", PACKET["Q"], present))

    # Fixed witnesses for exactly the three response edges used by the
    # minimized numerical core. Each may be old/base-safe or current-safe.
    solver.add(z3.Or(
        base_response(value, "r", RESPONSE_CORE["r"], present),
        current_response(value, "r", RESPONSE_CORE["r"], present),
    ))
    solver.add(z3.Or(
        base_response(value, "q", RESPONSE_CORE["q"], present),
        current_response(value, "q", RESPONSE_CORE["q"], present),
    ))
    solver.add(z3.Or(
        base_response(value, "s", RESPONSE_CORE["s"], present),
        current_response(value, "s", RESPONSE_CORE["s"], present),
    ))

    d_floor = total(value, "d", PACKET["W"])
    # Root-facing means at least one deletion tail of A exceeds d's floor.
    solver.add(z3.Or(*(
        z3.And(
            present[removed],
            total(value, "d", (g for g in PACKET["A"] if g != removed)) > d_floor,
        )
        for removed in PACKET["A"]
    )))
    solver.add(*tail_constraints(
        value, "d", PACKET["Q"], d_floor, present=present
    ))
    solver.add(*tail_constraints(
        value, "d", PACKET["E"], d_floor, present=present
    ))
    solver.add(d_floor >= total(value, "d", PACKET["P"]))
    return solver, value, present


def rational(model, expression) -> Fraction:
    return Fraction(str(model.eval(expression, model_completion=True)))


def values_from_model(model, value, present):
    values = {
        observer: {
            good: rational(model, value[good, observer]) for good in GOODS
        }
        for observer in OWNERS
    }
    active = tuple(
        good for good in GOODS
        if z3.is_true(model.eval(present[good], model_completion=True))
    )
    return values, active


def find_closed_families(values, active_goods=None, maximum=250):
    """Return closed disjoint common-safe desired-core families, if any."""
    active = set(GOODS if active_goods is None else active_goods)
    families = []
    for mask in range(1, 1 << len(OWNERS)):
        sources = tuple(
            owner for index, owner in enumerate(OWNERS) if mask & (1 << index)
        )
        allowed = {
            good for good in GOODS
            if good in active and BASE_OWNER[good] in (*sources, "charity")
        }
        solver = z3.SolverFor("QF_LRA")
        chosen = {
            (source, good): z3.Bool(f"oracle_{mask}_{source}_{good}")
            for source in sources for good in GOODS
        }
        for source in sources:
            solver.add(z3.Or(*(chosen[source, good] for good in allowed)))
            for good in GOODS:
                if good not in allowed:
                    solver.add(z3.Not(chosen[source, good]))
            solver.add(z3.Sum(*(
                z3.If(chosen[source, good], z3.RealVal(str(values[source][good])), 0)
                for good in GOODS
            )) > 1)
            for observer in OWNERS:
                selected_total = z3.Sum(*(
                    z3.If(
                        chosen[source, good],
                        z3.RealVal(str(values[observer][good])), 0,
                    )
                    for good in GOODS
                ))
                for removed in GOODS:
                    solver.add(z3.Implies(
                        chosen[source, removed],
                        selected_total - z3.RealVal(
                            str(values[observer][removed])
                        ) <= 1,
                    ))
        for good in GOODS:
            solver.add(z3.Sum(*(
                z3.If(chosen[source, good], 1, 0) for source in sources
            )) <= 1)
        while len(families) < maximum and solver.check() == z3.sat:
            model = solver.model()
            family = {
                source: tuple(
                    good for good in GOODS
                    if z3.is_true(
                        model.eval(chosen[source, good], model_completion=True)
                    )
                )
                for source in sources
            }
            families.append(family)
            solver.add(z3.Or(*(
                chosen[source, good] != model.eval(
                    chosen[source, good], model_completion=True
                )
                for source in sources for good in GOODS
            )))
        if len(families) >= maximum:
            break
    return tuple(families)


def find_closed_family(values, active_goods=None):
    families = find_closed_families(values, active_goods, maximum=1)
    return families[0] if families else None


def family_cut(value, present, family):
    return z3.Not(z3.And(*(
        base_response(value, source, goods, present)
        for source, goods in family.items()
    )))


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def find_complete_efx_four_edge_endpoints(values, active_goods, maximum=250):
    """Find exact complete EFX allocations using at most four move edges."""
    active = tuple(active_goods)
    owner_index = {owner: index for index, owner in enumerate(OWNERS)}
    destination = {good: z3.Int(f"efx_destination_{good}") for good in active}
    solver = z3.Solver()
    for good in active:
        solver.add(destination[good] >= 0, destination[good] < len(OWNERS))

    possible_edges = tuple(
        (supplier, target)
        for supplier in (*OWNERS, "charity") for target in OWNERS
        if supplier != target
    )
    edge = {
        pair: z3.Bool(f"efx_edge_{pair[0]}_{pair[1]}")
        for pair in possible_edges
    }
    for good in active:
        supplier = CURRENT_HOLDER[good]
        for target in OWNERS:
            if target == supplier:
                continue
            solver.add(z3.Implies(
                destination[good] == owner_index[target],
                edge[supplier, target],
            ))
    solver.add(z3.PbLe([(variable, 1) for variable in edge.values()], 4))

    utility = {}
    for observer in OWNERS:
        for recipient in OWNERS:
            utility[observer, recipient] = z3.Sum(*(
                z3.If(
                    destination[good] == owner_index[recipient],
                    z3.RealVal(str(values[observer][good])), 0,
                )
                for good in active
            ))
    for observer in OWNERS:
        for target in OWNERS:
            if observer == target:
                continue
            for removed in active:
                solver.add(z3.Implies(
                    destination[removed] == owner_index[target],
                    utility[observer, observer]
                    >= utility[observer, target]
                    - z3.RealVal(str(values[observer][removed])),
                ))
    results = []
    while len(results) < maximum and solver.check() == z3.sat:
        model = solver.model()
        allocation = {owner: [] for owner in OWNERS}
        for good in GOODS:
            if good in destination:
                target = OWNERS[model.eval(destination[good]).as_long()]
            else:
                supplier = CURRENT_HOLDER[good]
                target = supplier if supplier in OWNERS else "r"
            allocation[target].append(good)
        actual_edges = sorted({
            (CURRENT_HOLDER[good], owner)
            for owner, goods in allocation.items() for good in goods
            if good in active and CURRENT_HOLDER[good] != owner
        })
        assert len(actual_edges) <= 4
        result = {
            "allocation": {
                owner: tuple(goods) for owner, goods in allocation.items()
            },
            "transfer_edges": tuple(actual_edges),
        }
        assert verify_complete_efx_endpoint(values, active, result)
        results.append(result)
        solver.add(z3.Or(*(
            destination[good] != model.eval(destination[good]) for good in active
        )))
    return tuple(results)


def find_complete_efx_four_edge(values, active_goods):
    endpoints = find_complete_efx_four_edge_endpoints(
        values, active_goods, maximum=1
    )
    return endpoints[0] if endpoints else None


def verify_complete_efx_endpoint(values, active_goods, endpoint):
    """Independent exact-arithmetic verifier for a four-edge endpoint."""
    active = set(active_goods)
    allocation = endpoint["allocation"]
    assigned = [good for owner in OWNERS for good in allocation[owner] if good in active]
    if len(assigned) != len(set(assigned)) or set(assigned) != active:
        return False
    edges = {
        (CURRENT_HOLDER[good], owner)
        for owner in OWNERS for good in allocation[owner]
        if good in active and CURRENT_HOLDER[good] != owner
    }
    if len(edges) > 4 or edges != set(endpoint["transfer_edges"]):
        return False
    utility = {
        (observer, recipient): sum(
            (values[observer][good] for good in allocation[recipient]
             if good in active),
            Fraction(),
        )
        for observer in OWNERS for recipient in OWNERS
    }
    return all(
        utility[observer, observer]
        >= utility[observer, target] - values[observer][removed]
        for observer in OWNERS for target in OWNERS if observer != target
        for removed in allocation[target] if removed in active
    )


def complete_efx_formula(value, present, allocation):
    utility = {
        (observer, recipient): total(value, observer, allocation[recipient])
        for observer in OWNERS for recipient in OWNERS
    }
    return z3.And(*(
        z3.Implies(
            present[removed],
            utility[observer, observer]
            >= utility[observer, target] - value[removed, observer],
        )
        for observer in OWNERS for target in OWNERS if observer != target
        for removed in allocation[target]
    ))


def run(output: Path, timeout_seconds: int, maximum_iterations: int,
        random_seed: int, resume: Path | None = None,
        maximum_families_per_round: int = 250,
        separate_complete_efx: bool = False,
        maximum_efx_per_round: int = 250):
    solver, value, present = build_master()
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    signatures = set()
    allocation_signatures = set()
    resume_record = None
    if resume is not None:
        root = Path(__file__).resolve().parents[2]
        chain = []
        seen_paths = set()

        def load_chain(path):
            resolved = path.resolve()
            if resolved in seen_paths:
                raise ValueError("cyclic role-split resume chain")
            seen_paths.add(resolved)
            payload = json.loads(resolved.read_text())
            parent = (payload.get("resume") or {}).get("source")
            if parent:
                load_chain(root / parent)
            chain.append((resolved, payload))

        load_chain(resume)
        for _, payload in chain:
            if payload.get("goods") != list(GOODS):
                raise ValueError("resume goods do not match role-split cell")
            for record in payload.get("iterations", ()):
                endpoint_rows = record.get("complete_efx_allocations")
                if endpoint_rows is None:
                    allocation = record.get("complete_efx_allocation")
                    endpoint_rows = () if allocation is None else (
                        {"allocation": allocation},
                    )
                for endpoint_row in endpoint_rows:
                    allocation = endpoint_row["allocation"]
                    normalized_allocation = {
                        owner: tuple(goods)
                        for owner, goods in allocation.items()
                    }
                    allocation_signature = tuple(
                        (owner, tuple(normalized_allocation[owner]))
                        for owner in OWNERS
                    )
                    if allocation_signature not in allocation_signatures:
                        allocation_signatures.add(allocation_signature)
                        solver.add(z3.Not(complete_efx_formula(
                            value, present, normalized_allocation
                        )))
                families = record.get("closed_families")
                if families is None:
                    family = record.get("closed_family")
                    families = () if family is None else (family,)
                for family in families:
                    normalized = {
                        source: tuple(goods) for source, goods in family.items()
                    }
                    signature = tuple(
                        (source, tuple(goods))
                        for source, goods in sorted(normalized.items())
                    )
                    if signature in signatures:
                        continue
                    signatures.add(signature)
                    solver.add(family_cut(value, present, normalized))
        resume_record = {
            "source": f"results/{resume.name}",
            "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
            "chain_length": len(chain),
            "loaded_cut_count": len(signatures),
            "loaded_complete_efx_cut_count": len(allocation_signatures),
        }
    result = {
        "schema": "allocated-e-form0-role-split-pi-cegar-v1",
        "status": "RUNNING",
        "goods": list(GOODS),
        "base": {owner: list(goods) for owner, goods in BASE.items()},
        "support": {owner: list(goods) for owner, goods in SUPPORT.items()},
        "response_cores": {
            owner: list(goods) for owner, goods in RESPONSE_CORE.items()
        },
        "timeout_seconds_per_check": timeout_seconds,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "separate_complete_efx": separate_complete_efx,
        "maximum_efx_per_round": maximum_efx_per_round,
        "random_seed": random_seed,
        "resume": resume_record,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "iterations": [],
        "claim_boundary": (
            "Exact 21-good maximally role-split R2 necessary-premise cell. "
            + (
                "The separator excludes both complete EFX allocations using "
                "at most four current-supplier transfer edges and closed "
                "generalized-PI families. "
                if separate_complete_efx else
                "The separator excludes closed generalized-PI families. "
            )
            + "UNSAT is a bounded split-cell theorem, not a cap-free lift. "
            "A SAT terminal is an exact countermodel only to the declared "
            "finite necessary-premise menu, not to general additive EFX."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {"iteration": iteration, "solver_status": str(checked)}
        if checked == z3.unsat:
            result["status"] = "UNSAT"
            result["iterations"].append(record)
            checkpoint()
            break
        if checked == z3.unknown:
            result["status"] = "UNKNOWN"
            record["reason_unknown"] = solver.reason_unknown()
            result["iterations"].append(record)
            checkpoint()
            break
        values, active = values_from_model(solver.model(), value, present)
        result["last_values"] = serialize_values(values)
        result["last_active_goods"] = list(active)
        if separate_complete_efx:
            endpoints = find_complete_efx_four_edge_endpoints(
                values, active, maximum=maximum_efx_per_round
            )
            if endpoints:
                fresh_endpoints = []
                for endpoint in endpoints:
                    allocation = endpoint["allocation"]
                    allocation_signature = tuple(
                        (owner, tuple(allocation[owner])) for owner in OWNERS
                    )
                    if allocation_signature in allocation_signatures:
                        continue
                    allocation_signatures.add(allocation_signature)
                    solver.add(z3.Not(complete_efx_formula(
                        value, present, allocation
                    )))
                    fresh_endpoints.append({
                        "allocation": {
                            owner: list(goods)
                            for owner, goods in allocation.items()
                        },
                        "transfer_edges": [
                            list(edge) for edge in endpoint["transfer_edges"]
                        ],
                    })
                if not fresh_endpoints:
                    raise AssertionError(
                        "oracle repeated only installed EFX allocations"
                    )
                record["complete_efx_allocations"] = fresh_endpoints
                result["iterations"].append(record)
                checkpoint()
                continue
        families = find_closed_families(
            values, active, maximum=maximum_families_per_round
        )
        if not families:
            result["status"] = (
                "SAT_NO_COMPLETE_EFX_OR_GENERALIZED_PI"
                if separate_complete_efx else "SAT_NO_GENERALIZED_PI"
            )
            result["values"] = serialize_values(values)
            result["active_goods"] = list(active)
            result["iterations"].append(record)
            checkpoint()
            break
        fresh = []
        for family in families:
            signature = tuple(
                (source, tuple(goods))
                for source, goods in sorted(family.items())
            )
            if signature in signatures:
                continue
            signatures.add(signature)
            solver.add(family_cut(value, present, family))
            fresh.append({source: list(goods) for source, goods in family.items()})
        if not fresh:
            raise AssertionError("oracle repeated only installed families")
        record["closed_families"] = fresh
        result["iterations"].append(record)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    result["generalized_pi_cut_count"] = len(signatures)
    result["complete_efx_cut_count"] = len(allocation_signatures)
    checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--maximum-families-per-round", type=int, default=250)
    parser.add_argument("--separate-complete-efx", action="store_true")
    parser.add_argument("--maximum-efx-per-round", type=int, default=250)
    args = parser.parse_args()
    result = run(
        args.output, args.timeout_seconds, args.maximum_iterations,
        args.random_seed, resume=args.resume,
        maximum_families_per_round=args.maximum_families_per_round,
        separate_complete_efx=args.separate_complete_efx,
        maximum_efx_per_round=args.maximum_efx_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
