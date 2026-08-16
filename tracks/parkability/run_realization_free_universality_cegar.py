#!/usr/bin/env python3
"""Realization-free universality: CEGAR over tame splits only.

Two facts from the identity-aware note combine into a decision procedure that
is exact for *every* physical realization of a totals/minima profile, with no
slack hypothesis and no cardinality cap.

*Lemma C (split-locality), cardinality-free form.*  A role that an allocation
does not split contributes its total `T[i,g]` to the owning bundle and offers
`M[i,g]` as that bundle's smallest deletion candidate from within the role,
whatever the role's cardinality and whatever the witness identities.  So an
unsplit role of any width is exactly modelled by the two goods `M, T-M`.

*Lemma B.*  A role of slack `rho(g) <= 2` has at most two goods, and a
multi-good one has the forced column `{M, T-M}`.  Its only freedom is the side
pattern `s[g,i]` saying which good carries observer `i`'s minimum.

Call a multi-good role *tame* when `rho(g) <= 2` and *wild* otherwise.  This
driver searches for allocations that split tame roles only, and runs the
side-pattern CEGAR over the tame roles' patterns.  A master `unsat` then means:
for every physical realization of the profile, at every cardinality of every
wild role and every witness identity, some allocation of the accumulated menu
is a complete EFX allocation within the support-edge budget.

That verdict is exhaustive.  It supersedes the two-good-family verdict, which
covered only the realizations with two goods per role.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import build_decision
from .run_identity_aware_witness_side_batch import distinct_profiles, slack
from .run_identity_aware_witness_side_cegar import (
    audit_allocation,
    concrete_values,
    failure_clause,
    load_profile,
    partition_of,
    role_layout,
    symbolic_values,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def classify_roles(totals, minima):
    """Split the multi-good roles into tame (slack <= 2) and wild ones."""
    role_goods, multi = role_layout(totals, minima)
    tame = tuple(g for g in multi if slack(totals, minima, g) <= 2)
    wild = tuple(g for g in multi if slack(totals, minima, g) >= 3)
    return role_goods, multi, tame, wild


def decide_tame(physical, role_goods, wild, edge_cap, timeout_seconds):
    """Four-edge EFX decision in which no wild role may be split."""
    solver, assign, _, split, goods = build_decision(
        physical, role_goods, split_cap=None, edge_cap=edge_cap
    )
    for role in wild:
        solver.add(z3.Not(split[role]))
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
    assert not set(split_roles) & set(wild), split_roles
    return "sat", (allocation, split_roles), None


def audit_no_wild_split(allocation, wild, role_goods):
    """Confirm directly that every wild role sits inside a single bundle."""
    for role in wild:
        holders = {
            owner for owner, goods in allocation.items()
            if set(goods) & set(role_goods[role])
        }
        assert len(holders) == 1, (role, sorted(holders))


def solve_profile(totals, minima, edge_cap, maximum_rounds, timeout_seconds):
    role_goods, multi, tame, wild = classify_roles(totals, minima)

    side = {
        (role, observer): z3.Bool(f"side_{role}_{observer}")
        for role in multi for observer in OWNERS
    }
    master = z3.Solver()
    # Swapping a role's two goods is a relabelling, so pin observer r.
    master.add(*(z3.Not(side[role, "r"]) for role in multi))
    # A wild role is never split, so its two-good stand-in carries no identity
    # freedom: only its total and its minimum reach any bundle.
    master.add(*(z3.Not(side[role, observer])
                 for role in wild for observer in OWNERS))
    symbolic = symbolic_values(totals, minima, role_goods, side)

    canonical = {(role, o): False for role in multi for o in OWNERS}
    canonical_physical = concrete_values(totals, minima, role_goods, canonical)
    baseline_status, baseline_found, baseline_reason = decide_tame(
        canonical_physical, role_goods, wild, edge_cap, timeout_seconds
    )
    rounds = 0
    baseline_split_roles = None
    if baseline_found is not None:
        allocation, baseline_split_roles = baseline_found
        audit_allocation(allocation, canonical_physical, edge_cap)
        audit_no_wild_split(allocation, wild, role_goods)
        master.add(failure_clause(allocation, symbolic))
        rounds = 1
    elif baseline_status == "unsat":
        return {
            "status": "UNSAT_NO_TAME_SPLIT_ALLOCATION",
            "baseline_status": baseline_status,
            "cegar_rounds": 0,
            "tame_roles": list(tame),
            "wild_roles": list(wild),
            "realization_free": False,
            "baseline_split_roles": None,
            "terminal_coincidence_partitions": None,
        }
    else:
        return {
            "status": "UNKNOWN",
            "baseline_status": baseline_status,
            "baseline_reason_unknown": baseline_reason,
            "cegar_rounds": 0,
            "tame_roles": list(tame),
            "wild_roles": list(wild),
            "realization_free": False,
            "baseline_split_roles": None,
            "terminal_coincidence_partitions": None,
        }

    status = "ROUND_LIMIT"
    terminal_pattern = None
    for _ in range(maximum_rounds):
        outcome = master.check()
        if outcome == z3.unsat:
            status = "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"
            break
        if outcome == z3.unknown:
            status = "UNKNOWN"
            break
        model = master.model()
        sides = {k: z3.is_true(model.eval(f)) for k, f in side.items()}
        physical = concrete_values(totals, minima, role_goods, sides)
        concrete_status, found, _ = decide_tame(
            physical, role_goods, wild, edge_cap, timeout_seconds
        )
        rounds += 1
        if concrete_status == "unsat":
            status = "TAME_SPLIT_REALIZATION_COUNTERMODEL"
            terminal_pattern = {r: partition_of(sides, tame, r) for r in tame}
            break
        if concrete_status != "sat":
            status = "UNKNOWN"
            break
        allocation, _ = found
        audit_allocation(allocation, physical, edge_cap)
        audit_no_wild_split(allocation, wild, role_goods)
        master.add(failure_clause(allocation, symbolic))

    return {
        "status": status,
        "baseline_status": baseline_status,
        "baseline_split_roles": baseline_split_roles,
        "cegar_rounds": rounds,
        "tame_roles": list(tame),
        "wild_roles": list(wild),
        "maximum_role_slack": str(max(slack(totals, minima, g) for g in GOODS)),
        "realization_free":
            status == "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION",
        "terminal_coincidence_partitions": terminal_pattern,
    }


def run(trace_paths, profile_paths, output_path, edge_cap, maximum_rounds,
        timeout_seconds, limit):
    profiles = distinct_profiles(trace_paths) if trace_paths else []
    for path in profile_paths or ():
        raw, totals, minima = load_profile(path)
        profiles.append({
            "source": path.name, "iteration": "terminal",
            "totals": totals, "minima": minima,
        })
    if limit is not None:
        profiles = profiles[:limit]

    records = []
    for index, profile in enumerate(profiles):
        outcome = solve_profile(
            profile["totals"], profile["minima"],
            edge_cap, maximum_rounds, timeout_seconds,
        )
        outcome.update({
            "index": index,
            "source": profile["source"],
            "source_iteration": profile["iteration"],
        })
        records.append(outcome)
        print(index, profile["source"][:34], profile["iteration"],
              outcome["status"], "rounds", outcome["cegar_rounds"],
              "wild", len(outcome["wild_roles"]), flush=True)

    result = {
        "schema": "realization-free-universality-cegar-v1",
        "traces": [
            {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in (trace_paths or ())
        ],
        "profiles_examined": len(records),
        "edge_cap": edge_cap,
        "status_tally": dict(Counter(r["status"] for r in records)),
        "realization_free_count": sum(1 for r in records if r["realization_free"]),
        "records": records,
        "claim_boundary": (
            "A realization_free verdict is exhaustive for the profile: every "
            "physical realization of its totals and minima, at every "
            "cardinality of every role and every witness identity, admits a "
            "complete EFX allocation within the support-edge budget.  It rests "
            "on Lemma B (a slack-two role has the forced two-good column) and "
            "the cardinality-free form of Lemma C (an unsplit role of any "
            "width is exactly modelled by its total and its minimum).  It does "
            "not establish chart coverage or the universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", default=[])
    parser.add_argument("--profile", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=60)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    result = run(tuple(args.trace), tuple(args.profile), args.output,
                 args.edge_cap, args.maximum_rounds, args.timeout_seconds,
                 args.limit)
    print(json.dumps({
        "profiles_examined": result["profiles_examined"],
        "status_tally": result["status_tally"],
        "realization_free_count": result["realization_free_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
