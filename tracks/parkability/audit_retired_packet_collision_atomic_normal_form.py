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
        "TARGET_ENVELOPE_UNIVERSAL_PAYMENT_OR_PI_LEMMA_20260813.md",
        "target_envelope_universal_payment_or_pi_audit.json",
        "TARGET_ENVELOPE_PROTECTED_PAIR_OR_SAME_SOURCE_STAR_LEMMA_20260813.md",
        "target_envelope_protected_pair_or_star_audit.json",
        "SAFE_CENTER_THREE_OFFER_RETURN_OR_REJECTION_LEMMA_20260813.md",
        "safe_center_three_offer_return_or_rejection_audit.json",
        "SAFE_CENTER_THREE_OFFER_PRIORITY_SPLIT_REDUCTION_20260813.md",
        "safe_center_three_offer_priority_split_audit.json",
        "LEDGER_NORMALIZED_ROOT_EXTERNAL_STAR_ASCENT_OR_PRICE_THEOREM_20260813.md",
        "ledger_normalized_root_external_star_ascent_or_price_audit.json",
        "COMPLETE_HOLDER_PRICE_POOL_REVERSAL_OR_UNDERPAYMENT_LEMMA_20260813.md",
        "complete_holder_price_pool_reversal_or_underpayment_audit.json",
        "RETIRED_PACKET_BIROW_SPLIT_OR_CUT_LEMMA_20260813.md",
        "retired_packet_birow_split_or_cut_audit.json",
        "PRIORITY_SACRIFICE_PROPER_RETIRED_PACKET_SPLIT_THEOREM_20260813.md",
        "priority_sacrifice_proper_retired_packet_split_audit.json",
        "RETIRED_PACKET_BIROW_CUT_SCALAR_REALIZABILITY_20260813.md",
        "retired_packet_birow_cut_scalar_realizability_audit.json",
        "MINIMAL_SAFE_ROOT_ANCHOR_OR_ATOMWISE_CORE_LEMMA_20260813.md",
        "minimal_safe_root_anchor_or_atomwise_core_audit.json",
        "retired_packet_charge_anchor_gate_audit.json",
    ]
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-collision-atomic-normal-form-audit-v1",
        "status": "T_L_TIMES_REDUCED_TO_INDIVISIBLE_OR_ROOT_DOUBLE_ATOMIC_CUT",
        "recipient_capture_identity": gate["capture_identity"],
        "holder_payment_identity": gate["holder_payment_identity"],
        "response_intersection_trichotomy": intersection_trichotomy,
        "typed_failure_routes": routes,
        "atomic_survivors": [
            "atomwise_critical_whole_packet_bilateral_deadlock",
            "root_facing_anchor_critical_packet",
            "external_star_routes_to_holder_price_or_progress",
        ],
        "full_T_L_times_theorem_closed": False,
        "smallest_missing_operations": [
            "controlled anchor release for a recipient-indivisible packet",
            "root conversion across the double-atomic bi-row cut",
        ],
        "dependencies": [
            {"path": f"results/{name}", "sha256": sha256(results / name)}
            for name in dependencies
        ],
        "claim_boundary": (
            "cap-free conventional reduction using existing lemma premises; "
            "recipient indivisibility, the root double-atomic cut, and the full theorem remain open"
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
