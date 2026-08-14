#!/usr/bin/env python3
"""Integrity and exact arithmetic audit for the T_{L,times} normal form."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion, logic: str = "QF_LIA") -> bool:
    solver = z3.SolverFor(logic)
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    results = repo / "results"
    gate = json.loads((results / "retired_packet_charge_anchor_gate_audit.json").read_text())
    assert gate["status"] == "RECIPIENT_CAPTURE_DOES_NOT_PAY_HOLDER_GATE_OPEN"
    assert gate["capture_identity"] and gate["holder_payment_identity"]
    assert not gate["full_T_L_times_theorem_refuted"]

    # Cap-free trichotomy for the intersection of a response with nonempty K.
    k_size, intersection_size = z3.Ints("k_size intersection_size")
    intersection_trichotomy = prove(
        [k_size > 0, intersection_size >= 0, intersection_size <= k_size],
        z3.Or(
            intersection_size == 0,
            z3.And(intersection_size > 0, intersection_size < k_size),
            intersection_size == k_size,
        ),
    )
    assert intersection_trichotomy

    # The typed failure partition is ordered: an own-floor failure is handled
    # before EFX comparison, and release is tested only after both pass.
    routes = []
    for own_floor_fails in (False, True):
        for strict_original in (False, True):
            for comparison_fails in (False, True):
                for release_fails in (False, True):
                    if own_floor_fails:
                        route = "strict_capture" if strict_original else "equality_critical"
                    elif comparison_fails:
                        route = "base_or_observer_debt"
                    elif release_fails:
                        route = "release_failure"
                    else:
                        route = "candidate_closes"
                    routes.append({
                        "own_floor_fails": own_floor_fails,
                        "strict_original": strict_original,
                        "comparison_fails": comparison_fails,
                        "release_fails": release_fails,
                        "route": route,
                    })
    assert len(routes) == 16

    dependencies = [
        "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md",
        "RETIRED_PACKET_COLLISION_ATOMIC_NORMAL_FORM_20260813.md",
        "DECORATED_HEAD_PROTECTED_BUNDLE_HALL_DICHOTOMY_20260813.md",
        "ONE_HEAD_NONROOT_COMPRESSION_STAR_HANDOFF_LEMMA_20260813.md",
        "ALTERNATING_TWO_HEAD_ROOT_COVERED_COMPRESSION_LEMMA_20260813.md",
        "TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md",
        "TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md",
        "ROOT_ANCHORED_ONE_HEAD_TWO_HOLE_SELECTOR_LEMMA_20260813.md",
        "PERMANENT_ANCHOR_RETIRE_ON_BACKUP_EXCHANGE_THEOREM_20260813.md",
        "ROOT_FACING_ANCHOR_SURPLUS_BAND_DICHOTOMY_20260813.md",
        "ROOT_FACING_HOLDER_PRICE_DUALITY_LEMMA_20260813.md",
        "root_facing_holder_price_duality_audit.json",
        "WHOLE_RETIRED_PACKET_ATOMWISE_CRITICALITY_LEMMA_20260813.md",
        "whole_retired_packet_atomwise_criticality_audit.json",
        "NORMALIZATION_BYPASS_RESERVOIR_REVERSAL_LEMMA_20260813.md",
        "normalization_bypass_reservoir_reversal_audit.json",
        "NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_DICHOTOMY_20260813.md",
        "normalization_bypass_three_reservoir_fan_audit.json",
        "retired_packet_charge_anchor_gate_audit.json",
    ]
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-collision-atomic-normal-form-audit-v1",
        "status": "T_L_TIMES_REDUCED_TO_THREE_ATOMIC_SURVIVORS",
        "recipient_capture_identity": gate["capture_identity"],
        "holder_payment_identity": gate["holder_payment_identity"],
        "response_intersection_trichotomy": intersection_trichotomy,
        "typed_failure_routes": routes,
        "atomic_survivors": [
            "atomwise_critical_whole_packet_bilateral_deadlock",
            "root_facing_anchor_critical_packet",
            "safe_payment_normalization_wall",
        ],
        "full_T_L_times_theorem_closed": False,
        "smallest_missing_operations": [
            "controlled unretirement or proper packet split",
            "reverse root-surplus band or release anchor within it",
            "nonresetting adaptive selector commitment with source/rank potential",
        ],
        "dependencies": [
            {"path": f"results/{name}", "sha256": sha256(results / name)}
            for name in dependencies
        ],
        "claim_boundary": (
            "cap-free conventional reduction using existing lemma premises; "
            "the three atomic survivors and the full theorem remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
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
        "atomic_survivors": result["atomic_survivors"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
