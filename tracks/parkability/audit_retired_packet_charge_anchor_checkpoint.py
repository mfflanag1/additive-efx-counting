#!/usr/bin/env python3
"""Integrity audit for the retired-packet charge/anchor checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


EXPECTED = {
    "retired_packet_charge_anchor_gate_audit.json":
        "RECIPIENT_CAPTURE_DOES_NOT_PAY_HOLDER_GATE_OPEN",
    "whole_retired_packet_atomwise_criticality_audit.json":
        "PROPER_PACKET_REDUCTION_OR_ATOMWISE_CRITICAL_SURVIVOR",
    "root_facing_anchor_surplus_band_audit.json":
        "ROOT_FACING_SURVIVOR_REDUCED_TO_CLOSED_SURPLUS_BAND",
    "root_facing_holder_price_duality_audit.json":
        "ROOT_BAND_IDENTIFIED_WITH_BOUNDED_HOLDER_PRICE_SEPARATOR",
    "normalization_bypass_reservoir_reversal_audit.json":
        "BYPASS_REDUCED_TO_COLLISION_OR_SAFE_PAYMENT_WALL",
    "normalization_bypass_three_reservoir_fan_audit.json":
        "ALL_UNSAFE_FAN_ALWAYS_HAS_SUPPLIER_CLOSED_PI_CYCLE",
    "retired_packet_collision_atomic_normal_form_audit.json":
        "T_L_TIMES_REDUCED_TO_INDIVISIBLE_OR_ROOT_DOUBLE_ATOMIC_CUT",
    "target_envelope_universal_payment_or_pi_audit.json":
        "ONE_TARGET_HAS_UNIVERSAL_EXTERNAL_PAYER_OR_SUPPLIED_PI",
    "target_envelope_protected_pair_or_star_audit.json":
        "SAFE_PAYMENT_WALL_REDUCED_TO_TWO_HOLE_OR_THREE_OFFER_STAR",
    "safe_center_three_offer_return_or_rejection_audit.json":
        "SAFE_CENTER_STAR_ENTERS_TWO_HOLE_OR_THREE_ROW_REJECTION",
    "safe_center_three_offer_priority_split_audit.json":
        "STAR_ROUTES_TO_ROOT_PRICE_OR_EXISTING_EXTERNAL_STAR",
    "ledger_normalized_root_external_star_ascent_or_price_audit.json":
        "EXTERNAL_STAR_SIGNS_ROUTE_TO_ASCENT_RANK_OR_ROOT_PRICE",
    "complete_holder_price_pool_reversal_or_underpayment_audit.json":
        "HOLDER_GATE_REDUCED_TO_PAYMENT_RESPONSE_OR_AGGREGATE_UNDERPAYMENT",
    "retired_packet_birow_split_or_cut_audit.json":
        "PROPER_PACKET_REDUCTION_OR_EXACT_BIROW_CUT",
    "priority_sacrifice_proper_retired_packet_split_audit.json":
        "SACRIFICE_SPLIT_ROUTES_TO_PROGRESS_OR_PROTECTED_CUT",
    "retired_packet_birow_cut_scalar_realizability_audit.json":
        "BIROW_CUT_CAPFREE_SCALAR_REALIZABILITY",
    "minimal_safe_root_anchor_or_atomwise_core_audit.json":
        "ROOT_RESELECTS_PROPER_SAFE_CORE_OR_IS_ATOMWISE_BASE_CRITICAL",
}


def run(repo: Path) -> dict:
    results = repo / "results"
    dependencies = []
    for name, status in EXPECTED.items():
        path = results / name
        data = json.loads(path.read_text())
        assert data["status"] == status
        assert not data["full_T_L_times_theorem_closed"] if (
            "full_T_L_times_theorem_closed" in data
        ) else not data["full_T_L_times_theorem_refuted"]
        dependencies.append({
            "path": str(path.relative_to(repo)),
            "sha256": sha256(path),
            "status": status,
        })

    fan = json.loads(
        (results / "normalization_bypass_three_reservoir_fan_audit.json").read_text()
    )
    assert fan["source_assignments_checked"] == 324
    assert fan["supplier_cycle_assignments"] == 324

    theorem = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CHECKPOINT_20260813.md"
    completion = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_COMPLETION_AUDIT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-charge-anchor-checkpoint-audit-v1",
        "status": "T_L_TIMES_NARROWED_TO_INDIVISIBLE_OR_ROOT_DOUBLE_ATOMIC_CUT",
        "dependencies": dependencies,
        "all_unsafe_normalization_fan_closed": True,
        "strict_whole_packet_charge": "(|K|-1)*mu <= d",
        "strict_sacrifice_indivisibility_charge": "(|K|-1)*mu < d",
        "root_holder_price": "0 <= pi_r(D) <= x-delta",
        "birow_cut_scalar_realizable_inside_root_band": True,
        "final_aggregate_separator": (
            "v_s(T)>=d implies v_h(T)>sigma+M_h(T) for every T subset K"
        ),
        "remaining_separator_families": [
            "recipient_indivisible_whole_packet",
            "root_double_atomic_birow_cut",
        ],
        "full_T_L_times_theorem_closed": False,
        "full_T_L_times_theorem_refuted": False,
        "claim_boundary": (
            "verified cap-free reduction checkpoint; the indivisible/cut-to-anchor "
            "gate and complete GG closure remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "checkpoint": str(theorem.relative_to(repo)),
            "checkpoint_sha256": sha256(theorem),
            "completion_audit": str(completion.relative_to(repo)),
            "completion_audit_sha256": sha256(completion),
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
        "remaining_separator_families": result["remaining_separator_families"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
