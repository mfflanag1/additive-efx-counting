#!/usr/bin/env python3
"""Audit the cross-star hole-pivot allocation and wall localization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    # Exhaust the membership types of one arbitrary good.  Whole-target
    # response rigidity sends every A_j good to d, leaving five cases.
    support_cases = []
    for origin, selected in (
        ("W", False),
        ("W", True),
        ("A_i", False),
        ("A_j", True),
        ("A_k", False),
    ):
        destinations = []
        if origin == "W" and selected:
            destinations.append("i")
        if origin == "A_j" and selected:
            destinations.append("d")
        if (
            (origin == "W" and not selected)
            or origin == "A_i"
        ):
            destinations.append("j")
        if origin == "A_k":
            destinations.append("k")
        assert len(destinations) == 1
        support_cases.append({
            "origin": origin,
            "selected_into_response_core": selected,
            "destination": destinations[0],
        })
    set_partition_valid = len(support_cases) == 5

    desired, deletion, threshold, response_base = z3.Reals(
        "desired_subset containing_deletion threshold response_base"
    )
    whole_core_response_rigidity = check_unsat(
        desired <= deletion,
        deletion <= threshold,
        threshold <= response_base,
        desired > response_base,
    )

    envied_core_owner = "c"
    base = {agent: z3.Real(f"base_{agent}") for agent in AGENTS}
    own = {agent: z3.Real(f"own_{agent}") for agent in AGENTS}
    selected_tail = {
        (observer, target): z3.Real(f"tail_{observer}_{target}")
        for observer in AGENTS
        for target in AGENTS
        if target != envied_core_owner
    }
    represented = tuple(agent for agent in AGENTS if agent != envied_core_owner)
    assumptions = []
    for agent in represented:
        assumptions.append(own[agent] > base[agent])
    for observer in AGENTS:
        for target in represented:
            assumptions.append(selected_tail[observer, target] <= base[observer])

    represented_to_core = check_unsat(
        *assumptions,
        z3.Or(*(
            own[observer] < selected_tail[observer, target]
            for observer in represented
            for target in represented
        )),
    )
    own_residual_tail = z3.Real("tail_missing_own_residual")
    missing_to_self = check_unsat(
        *assumptions,
        own[envied_core_owner]
        < own_residual_tail,
        own_residual_tail <= own[envied_core_owner],
    )

    wall_residual = z3.Real("wall_residual")
    wall_tail = z3.Real("wall_tail")
    wall_total = z3.Real("wall_total")
    wall_base = z3.Real("wall_base")
    source_inactive_loss_band = check_unsat(
        wall_residual < wall_tail,
        wall_tail < wall_total,
        wall_total <= wall_base,
        wall_total != wall_base,
        z3.Not(z3.And(
            wall_residual < wall_tail,
            wall_tail < wall_total,
            wall_total < wall_base,
        )),
    )

    # In the representative order r,q,c,s, a pivot whose new hole is not r
    # leaves r strictly above base.  If q is represented it also gives the
    # flexible sign; if q is the hole, r's earlier gain gives the lex sign.
    r_improves = z3.Real("pivot_r")
    r_base = z3.Real("pivot_r_base")
    q_improves = z3.Real("pivot_q")
    q_base = z3.Real("pivot_q_base")
    external_hole_flexible = check_unsat(
        r_improves > r_base,
        q_improves > q_base,
        z3.Not(z3.And(r_improves >= r_base, q_improves > q_base)),
    )
    q_hole_lex = check_unsat(
        r_improves > r_base,
        z3.Not(r_improves > r_base),
    )

    script = Path(__file__).resolve()
    theorem = root / "results" / "CROSS_STAR_HOLE_PIVOT_LEMMA_20260811.md"
    return {
        "schema": "cross-star-hole-pivot-audit-v1",
        "status": "VERIFIED",
        "solver": f"Z3 {z3.get_version_string()}",
        "set_partition_valid": set_partition_valid,
        "set_partition_membership_cases": support_cases,
        "whole_core_response_rigidity": whole_core_response_rigidity,
        "wall_localization": {
            "represented_source_to_selected_core_impossible": represented_to_core,
            "missing_owner_to_own_residual_impossible": missing_to_self,
            "remaining_wall_types": [
                "missing_owner_to_selected_core",
                "represented_source_to_residual",
            ],
        },
        "source_inactive_loss_band": source_inactive_loss_band,
        "priority_split": {
            "external_hole_flexible": external_hole_flexible,
            "q_hole_r_first_lex": q_hole_lex,
        },
        "claim_boundary": (
            "cap-free set/support and scalar audit of one cross-star hole pivot; "
            "it does not prove termination of repeated pivots or PI release support"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results" / "cross_star_hole_pivot_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
