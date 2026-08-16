#!/usr/bin/env python3
"""CEGAR over witness identity at fixed totals and minima.

Every named multi-good role is realized by the two physical goods `g:0` and
`g:1`.  A *side pattern* `s[g,i]` in {0,1} says which of the two carries
observer `i`'s minimum:

    v_i(g:0) = M[i,g] + s[g,i] * D[i,g],
    v_i(g:1) = T[i,g] - M[i,g] - s[g,i] * D[i,g],   D[i,g] = T[i,g] - 2M[i,g].

For every side pattern the role total is `T[i,g]` and the role minimum is
`M[i,g]`, so the whole family shares one totals/minima profile and differs only
in the coincidence partition `ker(s[g, .])`, which ranges over the eight
partitions of the four observers into at most two blocks.  Swapping `g:0` with
`g:1` relabels goods, so `s[g,r]` is fixed to zero without loss.

The loop alternates a side-pattern master, which seeks a pattern defeating
every allocation found so far, with the exact concrete four-support-edge EFX
decision for the pattern it proposes.  A concrete `unsat` is an exact
countermodel showing that totals and minima do not determine the four-edge
gate; a master `unsat` proves the opposite over the accumulated menu.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import (
    build_decision,
    support_supplier,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def rational(value):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_profile(path):
    raw = json.loads(path.read_text())
    totals = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_totals"].items()
    }
    minima = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_minima"].items()
    }
    return raw, totals, minima


def role_layout(totals, minima):
    """Physical good names per role and the multi-good role list."""
    role_goods = {}
    multi = []
    for role in GOODS:
        singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        if singleton:
            role_goods[role] = (f"{role}:0",)
        else:
            for observer in OWNERS:
                assert 2 * minima[observer][role] <= totals[observer][role], role
            role_goods[role] = (f"{role}:0", f"{role}:1")
            multi.append(role)
    return role_goods, tuple(multi)


def concrete_values(totals, minima, role_goods, sides):
    """Physical value table for one side pattern, keyed (observer, good)."""
    physical = {}
    for role, names in role_goods.items():
        for observer in OWNERS:
            if len(names) == 1:
                physical[observer, names[0]] = totals[observer][role]
                continue
            gap = totals[observer][role] - 2 * minima[observer][role]
            shift = gap if sides[role, observer] else Fraction(0)
            physical[observer, names[0]] = minima[observer][role] + shift
            physical[observer, names[1]] = (
                totals[observer][role] - minima[observer][role] - shift
            )
            assert physical[observer, names[0]] > 0
            assert physical[observer, names[1]] > 0
            assert min(
                physical[observer, names[0]], physical[observer, names[1]]
            ) == minima[observer][role]
    return physical


def symbolic_values(totals, minima, role_goods, side):
    """Physical value table as linear expressions in the side Booleans."""
    physical = {}
    for role, names in role_goods.items():
        for observer in OWNERS:
            if len(names) == 1:
                physical[observer, names[0]] = rational(totals[observer][role])
                continue
            gap = totals[observer][role] - 2 * minima[observer][role]
            shift = z3.If(side[role, observer], rational(gap), z3.RealVal(0))
            physical[observer, names[0]] = rational(minima[observer][role]) + shift
            physical[observer, names[1]] = (
                rational(totals[observer][role] - minima[observer][role]) - shift
            )
    return physical


def failure_clause(allocation, physical):
    """Some observer's EFX comparison against some target bundle breaks."""
    utility = {
        (observer, target): z3.Sum(*(
            physical[observer, good] for good in allocation[target]
        )) if allocation[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    return z3.Or(*(
        utility[observer, observer]
        < utility[observer, target] - physical[observer, good]
        for observer in OWNERS
        for target in OWNERS
        if target != observer
        for good in allocation[target]
    ))


def decide(physical, role_goods, edge_cap, timeout_seconds):
    solver, assign, _, split, goods = build_decision(
        physical, role_goods, split_cap=None, edge_cap=edge_cap
    )
    solver.set(timeout=timeout_seconds * 1000)
    status = solver.check()
    if status != z3.sat:
        return str(status), None, (
            solver.reason_unknown() if status == z3.unknown else None
        )
    model = solver.model()
    allocation = {
        owner: [g for g in goods if z3.is_true(model.eval(assign[g, owner]))]
        for owner in OWNERS
    }
    split_roles = sorted(
        role for role, flag in split.items() if z3.is_true(model.eval(flag))
    )
    return "sat", (allocation, split_roles), None


def audit_allocation(allocation, physical, edge_cap):
    """Recheck completeness, the edge budget and EFX in exact arithmetic."""
    supplier = support_supplier()
    placed = [good for goods in allocation.values() for good in goods]
    assert len(placed) == len(set(placed))
    edges = sorted({
        (supplier[good.split(":", 1)[0]], owner)
        for owner, goods in allocation.items()
        for good in goods
        if supplier[good.split(":", 1)[0]] != owner
    })
    assert len(edges) <= edge_cap
    for observer in OWNERS:
        own = sum((physical[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            total = sum(
                (physical[observer, g] for g in allocation[target]), Fraction()
            )
            for good in allocation[target]:
                assert own >= total - physical[observer, good]
    return edges


def partition_of(sides, multi, role):
    blocks = {}
    for observer in OWNERS:
        blocks.setdefault(bool(sides[role, observer]), []).append(observer)
    return "|".join(
        "".join(block) for block in sorted(blocks.values(), key=lambda b: b[0])
    )


def run(profile_path, output_path, edge_cap, maximum_rounds, timeout_seconds):
    raw, totals, minima = load_profile(profile_path)
    role_goods, multi = role_layout(totals, minima)

    side = {
        (role, observer): z3.Bool(f"side_{role}_{observer}")
        for role in multi for observer in OWNERS
    }
    master = z3.Solver()
    # Swapping the two goods of a role is a relabelling, so pin observer r.
    master.add(*(z3.Not(side[role, "r"]) for role in multi))
    symbolic = symbolic_values(totals, minima, role_goods, side)

    rounds = []
    terminal = None
    status = "ROUND_LIMIT"

    # Baseline: the canonical realization every banked script uses is the
    # all-coincide pattern, in which one good carries every observer's minimum.
    canonical_sides = {(role, o): False for role in multi for o in OWNERS}
    canonical_physical = concrete_values(totals, minima, role_goods, canonical_sides)
    canonical_status, canonical_found, canonical_reason = decide(
        canonical_physical, role_goods, edge_cap, timeout_seconds
    )
    baseline = {
        "coincidence_partition": "rqds",
        "status": canonical_status,
        "reason_unknown": canonical_reason,
    }
    if canonical_found is not None:
        allocation, split_roles = canonical_found
        baseline["allocation"] = allocation
        baseline["split_roles"] = split_roles
        baseline["used_edges"] = [
            list(edge) for edge in
            audit_allocation(allocation, canonical_physical, edge_cap)
        ]
        master.add(failure_clause(allocation, symbolic))
        rounds.append({"iteration": 0, "origin": "baseline",
                       "allocation": allocation, "split_roles": split_roles})

    for iteration in range(1, maximum_rounds + 1):
        outcome = master.check()
        if outcome == z3.unsat:
            status = "UNSAT_EVERY_SIDE_PATTERN_ADMITS_A_BANKED_ALLOCATION"
            break
        if outcome == z3.unknown:
            status = "UNKNOWN"
            break
        model = master.model()
        sides = {
            key: z3.is_true(model.eval(flag)) for key, flag in side.items()
        }
        physical = concrete_values(totals, minima, role_goods, sides)
        pattern = {role: partition_of(sides, multi, role) for role in multi}
        concrete_status, found, reason = decide(
            physical, role_goods, edge_cap, timeout_seconds
        )
        record = {
            "iteration": iteration,
            "coincidence_partitions": pattern,
            "concrete_status": concrete_status,
        }
        if concrete_status == "unsat":
            record["origin"] = "identity_countermodel"
            terminal = {
                "coincidence_partitions": pattern,
                "physical_values": {
                    observer: {
                        good: str(physical[observer, good])
                        for role in GOODS for good in role_goods[role]
                    }
                    for observer in OWNERS
                },
            }
            rounds.append(record)
            status = "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL"
            break
        if concrete_status != "sat":
            record["reason_unknown"] = reason
            rounds.append(record)
            status = "UNKNOWN"
            break
        allocation, split_roles = found
        audit_allocation(allocation, physical, edge_cap)
        record["allocation"] = allocation
        record["split_roles"] = split_roles
        rounds.append(record)
        master.add(failure_clause(allocation, symbolic))

    result = {
        "schema": "identity-aware-witness-side-cegar-v1",
        "status": status,
        "source_profile": str(profile_path),
        "source_profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "source_profile_status": raw.get("status"),
        "edge_cap": edge_cap,
        "edge_origin": "support",
        "multi_good_roles": list(multi),
        "singleton_roles": [r for r in GOODS if len(role_goods[r]) == 1],
        "side_pattern_family": (
            "two physical goods per multi-good role; the coincidence partition "
            "of each role ranges over the eight partitions of the four "
            "observers into at most two blocks"
        ),
        "canonical_baseline": baseline,
        "rounds": rounds,
        "terminal": terminal,
        "claim_boundary": (
            "Every side pattern realizes the same totals and minima.  A "
            "terminal concrete unsat together with a satisfiable canonical "
            "baseline proves that the totals/minima abstraction does not "
            "determine the four-support-edge EFX gate.  A master unsat proves "
            "only that no side pattern in this two-good family defeats the "
            "accumulated allocation menu.  Neither outcome resolves the "
            "universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=200)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(args.profile, args.output, args.edge_cap,
                 args.maximum_rounds, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
        "canonical_baseline": result["canonical_baseline"]["status"],
        "canonical_split_roles": result["canonical_baseline"].get("split_roles"),
        "terminal_partitions": (
            result["terminal"]["coincidence_partitions"] if result["terminal"] else None
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
