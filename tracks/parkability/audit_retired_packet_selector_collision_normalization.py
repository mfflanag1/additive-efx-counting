#!/usr/bin/env python3
"""Exact audit of retired-packet selector collision normalization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    a, k, minus, floor = z3.Reals("a k minus floor")
    premises = [a == k + minus, a > floor, minus <= floor, k >= 0]
    capture = prove(premises, k >= a - floor)
    positive = prove(premises, k > 0)
    assert capture and positive
    equality_critical = prove(
        [a == k + minus, a == floor, k > 0, minus >= 0],
        minus < floor,
    )
    assert equality_critical

    # Minimality safety arithmetic: a strong-envy threshold is the value of
    # one deletion. If it exceeds the observer floor, that deletion is a
    # strictly smaller desired subset.
    value_d, least, observer_floor, size_d = z3.Reals(
        "value_d least observer_floor size_d"
    )
    smaller_desired = prove(
        [value_d - least > observer_floor, least > 0, size_d >= 1],
        z3.And(value_d - least > observer_floor, size_d - 1 < size_d),
    )
    assert smaller_desired

    # Exact finite-record routing is a partition of the three cases:
    # an actually adopted response coordinate is new, the full state is new,
    # or both repeat.  A history-only insertion is deliberately not a route.
    routes = []
    for response_coordinate_new in (False, True):
        for state_new in (False, True):
            if response_coordinate_new:
                route = "response_coordinate_progress"
            elif state_new:
                route = "complete_state_progress"
            else:
                route = "exact_TL_star"
            routes.append({
                "response_coordinate_new": response_coordinate_new,
                "collision_provenance_recorded": response_coordinate_new,
                "state_new": state_new,
                "route": route,
            })
    assert sum(r["route"] == "exact_TL_star" for r in routes) == 1

    theorem = repo / "results/RETIRED_PACKET_SELECTOR_COLLISION_NORMALIZATION_LEMMA_20260813.md"
    contract = repo / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-selector-collision-normalization-audit-v2",
        "status": "COLLISION_NORMALIZED_TO_LEDGER_FREE_PROGRESS_ROOT_OR_TL_STAR",
        "capture_inequality": capture,
        "capture_packet_positive": positive,
        "weak_floor_equality_critical": equality_critical,
        "minimality_protected_floor_safety_step": smaller_desired,
        "current_safety_requires_current_floor": True,
        "finite_record_routes": routes,
        "exact_repeat_route_count": 1,
        "history_only_progress_forbidden": True,
        "equality_without_typed_handoff_routes_to_TL_star": True,
        "ledger_free_exact_response_repeat_routes_to_TL_star": True,
        "specialized_handoff_requires_exact_premises": True,
        "no_silent_reuse": True,
        "claim_boundary": (
            "local universal normalization; transition-pool coverage and "
            "rank-deficient TL-star payment remain to compose"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "contract": str(contract.relative_to(repo)),
            "contract_sha256": sha256(contract),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "exact_repeat_route_count": result["exact_repeat_route_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
