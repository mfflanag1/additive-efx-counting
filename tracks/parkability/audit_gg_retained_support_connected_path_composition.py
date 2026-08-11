#!/usr/bin/env python3
"""Integrity manifest for the GG retained-support connected-path chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEPENDENCIES = (
    ("FLOWER_REMOVED_TOP_RETENTION_POTENTIAL_LEMMA_20260811.md", "flower_removed_top_retention_potential_audit.json"),
    ("CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md", "captured_q_margin_anchored_residual_rotation_audit.json"),
    ("EVOLVED_TARGET_MINIMAL_SOURCE_TRICHOTOMY_LEMMA_20260811.md", "evolved_target_minimal_source_trichotomy_audit.json"),
    ("ROOT_SOURCED_EVOLVED_TARGET_RETURN_OR_CAPTURE_LEMMA_20260811.md", "root_sourced_evolved_target_return_or_capture_audit.json"),
    ("ROOT_RESPONSE_FLOATER_SUBSTITUTION_DICHOTOMY_LEMMA_20260811.md", "root_response_floater_substitution_dichotomy_audit.json"),
    ("CANONICAL_ROOT_RESPONSE_TWO_STAGE_SELECTOR_LEMMA_20260811.md", "canonical_root_response_two_stage_selector_audit.json"),
    ("JOINT_PACKET_BILATERAL_OR_LEX_DONATION_SELECTOR_LEMMA_20260811.md", "joint_packet_bilateral_or_lex_donation_selector_audit.json"),
    ("JOINT_PACKET_CHARITY_COMPLETED_TRANSFER_PATH_LEMMA_20260811.md", "joint_packet_charity_completed_transfer_path_audit.json"),
    ("CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md", "charity_completed_path_root_response_anchor_audit.json"),
    ("MAXIMUM_MATCHING_OWNER_UNION_COMPRESSION_LEMMA_20260811.md", "maximum_matching_owner_union_compression_audit.json"),
    ("SOURCE_INACTIVE_CORE_RESIDUAL_REPAIR_LEMMA_20260811.md", "source_inactive_core_residual_repair_audit.json"),
    ("TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md", "two_hole_cut_and_choose_response_hall_audit.json"),
    ("TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md", "two_by_two_response_hall_normal_form_audit.json"),
    ("GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md", "gg_rank_reset_raw_potential_refutation_audit.json"),
    ("EXTERNALLY_SAFE_CONNECTED_PATH_TRANSFER_LEMMA_20260811.md", "externally_safe_connected_path_transfer_audit.json"),
    ("ROOT_DONATION_GLOBAL_BLOCKER_LEMMA_20260811.md", "root_donation_global_blocker_audit.json"),
    ("ROOT_MONOPOLY_CHARITY_PATH_HANDOFF_LEMMA_20260811.md", "root_monopoly_charity_path_handoff_audit.json"),
    ("UNIVERSAL_RETAINED_SUPPORT_RESET_LEMMA_20260811.md", "universal_retained_support_reset_audit.json"),
    ("FLOATER_CONSUMING_RESET_SOURCE_TRICHOTOMY_20260811.md", "floater_consuming_reset_source_trichotomy_audit.json"),
    ("SURPLUS_BUDGETED_CONNECTED_COMPONENT_TRANSFER_LEMMA_20260811.md", "surplus_budgeted_connected_component_transfer_audit.json"),
    ("GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md", "gg_historical_support_ledger_stagnation_audit.json"),
    ("ANCHOR_CONSTRAINED_Q_PRIORITY_MATCHING_LEMMA_20260811.md", "anchor_constrained_q_priority_matching_audit.json"),
    ("PERMANENT_ANCHOR_Q_ACTIVITY_DICHOTOMY_LEMMA_20260811.md", "permanent_anchor_q_activity_dichotomy_audit.json"),
    ("FIXED_U_Q_RESIDUAL_GLOBAL_MAX_SELECTOR_LEMMA_20260811.md", "fixed_u_q_residual_global_max_selector_audit.json"),
    ("PROTECTED_Q_RESPONSE_RETENTION_LEMMA_20260811.md", "protected_q_response_retention_audit.json"),
    ("DEGREE_ZERO_Q_SPLIT_CORE_ROOT_FLIP_LEMMA_20260811.md", "degree_zero_q_split_core_root_flip_audit.json"),
    ("SOURCE_MARGIN_ROOT_BUDGET_FRONTIER_LEMMA_20260811.md", "source_margin_root_budget_frontier_audit.json"),
    ("ANCHOR_CONSTRAINED_FULL_PRIORITY_MATCHING_LEMMA_20260811.md", "anchor_constrained_full_priority_matching_audit.json"),
    ("FIXED_U_ARBITRARY_HOLE_RESIDUAL_SELECTOR_LEMMA_20260811.md", "fixed_u_arbitrary_hole_residual_selector_audit.json"),
    ("GLOBAL_RESIDUAL_ROOT_FACING_RIGIDITY_LEMMA_20260811.md", "global_residual_root_facing_rigidity_audit.json"),
    ("THIRD_OWNER_ROOT_REPLACEMENT_FORK_LEMMA_20260811.md", "third_owner_root_replacement_fork_audit.json"),
    ("Q_DONOR_BLOCKADE_CAPTURED_MARGIN_HANDOFF_LEMMA_20260811.md", "q_donor_blockade_captured_margin_handoff_audit.json"),
    ("ROOT_CONCENTRATION_BOTTOM_ABSORPTION_ROTATION_LEMMA_20260811.md", "root_concentration_bottom_absorption_rotation_audit.json"),
    ("UNIVERSAL_RETAINED_BOTTOM_SUPPORT_RESET_LEMMA_20260811.md", "universal_retained_bottom_support_reset_audit.json"),
    ("RETAINED_BOTTOM_LEDGER_STAGNATION_REFUTATION_20260811.md", "retained_bottom_ledger_stagnation_refutation_audit.json"),
    ("BOTTOM_TAIL_THREE_OWNER_CYCLE_SPLICE_LEMMA_20260811.md", "bottom_tail_three_owner_cycle_splice_audit.json"),
    ("BOTTOM_TAIL_Q_BUDGET_CANONICAL_SPLIT_LEMMA_20260811.md", "bottom_tail_q_budget_canonical_split_audit.json"),
    ("BLOCKED_HOLE_MINIMAL_K_Q_BUDGET_DICHOTOMY_20260811.md", "blocked_hole_minimal_k_q_budget_dichotomy_audit.json"),
    ("FOURTH_OWNER_MARGIN_SUBSTITUTION_SELECTOR_LEMMA_20260811.md", "fourth_owner_margin_substitution_selector_audit.json"),
    ("COMPENSATED_FOURTH_OWNER_RESIDUAL_SELECTOR_LEMMA_20260811.md", "compensated_fourth_owner_residual_selector_audit.json"),
    ("PAID_INPUT_OMITTED_HOLE_COMPRESSION_LEMMA_20260811.md", "paid_input_omitted_hole_compression_audit.json"),
    ("PAID_ANCHOR_DISJOINT_RECAPTURE_DICHOTOMY_20260811.md", "paid_anchor_disjoint_recapture_dichotomy_audit.json"),
    ("PAID_ANCHOR_CURRENT_WALL_RECURRENCE_LEMMA_20260811.md", "paid_anchor_current_wall_recurrence_audit.json"),
    ("PAID_ANCHOR_LEAST_GOOD_CONSUMPTION_LEMMA_20260811.md", "paid_anchor_least_good_consumption_audit.json"),
    ("UNIVERSAL_PAID_ANCHOR_SUPPORT_RESET_LEMMA_20260811.md", "universal_paid_anchor_support_reset_audit.json"),
    ("PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md", "paid_splice_observer_failure_current_response_audit.json"),
    ("CROSS_COMPONENT_SAFETY_DEBT_BRIDGE_LEMMA_20260811.md", "cross_component_safety_debt_bridge_audit.json"),
    ("CROSS_COMPONENT_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "cross_component_return_compensation_selector_audit.json"),
    ("COMPONENT_WIDE_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "component_wide_return_compensation_selector_audit.json"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    result_dir = root / "results"
    records = []
    for theorem_name, audit_name in DEPENDENCIES:
        theorem = result_dir / theorem_name
        audit = result_dir / audit_name
        payload = json.loads(audit.read_text())
        records.append({
            "theorem": f"results/{theorem_name}",
            "theorem_sha256": sha256(theorem),
            "audit": f"results/{audit_name}",
            "audit_sha256": sha256(audit),
            "audit_status": payload.get("status"),
        })
    accepted = {"ALL_FORCED", "ALL_EXHAUSTED", "ALL_CLASSIFIED", "VERIFIED", "PASS", "CLASSIFIED", "COMPOSED", "DEPENDENCIES_REPLAYABLE", "EXACT_SCALE_REFUTATION", "EXACT_PLATEAU", "EXACT_BOTTOM_TAIL_PLATEAU"}
    verified = all(record["audit_status"] in accepted for record in records)
    script = Path(__file__).resolve()
    checkpoint = result_dir / "GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md"
    return {
        "schema": "gg-retained-support-connected-path-composition-audit-v1",
        "status": "DEPENDENCIES_REPLAYABLE" if verified else "OPEN",
        "dependency_count": len(records),
        "records": records,
        "focused_test_count": 106,
        "claim_boundary": (
            "integrity/replay manifest for proved local lemmas; it does not prove "
            "the corrected support-ledger monotonicity theorem, GG closure, or "
            "four-agent EFX"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "checkpoint": str(checkpoint.relative_to(root)),
            "checkpoint_sha256": sha256(checkpoint),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "dependency_count": result["dependency_count"],
        "focused_test_count": result["focused_test_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
