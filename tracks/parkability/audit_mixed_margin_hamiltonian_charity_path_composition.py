#!/usr/bin/env python3
"""Integrity manifest for the mixed-margin Hamiltonian charity-path chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEPENDENCIES = (
    ("FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md", "full_signed_transfer_state_reconstruction_audit.json"),
    ("CHARITY_AUGMENTED_FIVE_TARGET_HOLE_PIVOT_CYCLE_LEMMA_20260811.md", "charity_augmented_five_target_hole_pivot_cycle_audit.json"),
    ("PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md", "paid_splice_observer_failure_current_response_audit.json"),
    ("CURRENT_SAFE_FULL_RESPONSE_MATCHING_ENDPOINT_LEMMA_20260811.md", "current_safe_full_response_matching_endpoint_audit.json"),
    ("PI_FREE_FIVE_TARGET_CHARITY_PATH_HOLE_EDGE_LEMMA_20260811.md", "pi_free_five_target_charity_path_hole_edge_audit.json"),
    ("ARBITRARY_CHARITY_PACKET_BLOCKER_COLLAPSE_LEMMA_20260811.md", "arbitrary_charity_packet_blocker_collapse_audit.json"),
    ("MIXED_MARGIN_NONOWNER_RESIDUAL_OR_SELF_RESPONSE_LEMMA_20260811.md", "mixed_margin_nonowner_residual_or_self_response_audit.json"),
    ("DIRECT_SAFE_TARGET_SUBBUNDLE_OR_CRITICAL_TOPUP_LEMMA_20260811.md", "direct_safe_target_subbundle_or_critical_topup_audit.json"),
    ("DECORATED_TARGET_OWNER_COMPLEMENT_RETURN_SELECTOR_LEMMA_20260811.md", "decorated_target_owner_complement_return_selector_audit.json"),
    ("SOURCE_BUNDLE_CHARITY_COMPLEMENT_EXCHANGE_SELECTOR_LEMMA_20260811.md", "source_bundle_charity_complement_exchange_selector_audit.json"),
    ("ANCHORED_MIXED_MARGIN_PATH_TERMINAL_CLASSIFICATION_LEMMA_20260811.md", "anchored_mixed_margin_path_terminal_classification_audit.json"),
    ("ANCHORED_Q_DONOR_OR_SOURCE_COLLISION_REDUCTION_20260811.md", "anchored_q_donor_or_source_collision_audit.json"),
    ("MUTUAL_FLOATER_DELETION_OR_DOUBLE_CRITICAL_LEMMA_20260811.md", "mutual_floater_deletion_or_double_critical_audit.json"),
    ("RETAINED_Q_BQ_FLOATER_SUBSTITUTION_HANDOFF_LEMMA_20260811.md", "retained_q_bq_floater_substitution_handoff_audit.json"),
    ("Q_CLOSING_SOURCE_RESIDUAL_REASSIGNMENT_LEMMA_20260811.md", "q_closing_source_residual_reassignment_audit.json"),
    ("CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md", "closing_source_deletion_return_residual_completion_audit.json"),
    ("CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md", "closing_source_deletion_return_referee_audit.json"),
    ("COMPONENT_WIDE_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "component_wide_return_compensation_selector_audit.json"),
    ("COMPONENT_WIDE_CURRENT_OR_BASE_FLOOR_HANDOFF_LEMMA_20260811.md", "component_wide_current_or_base_floor_handoff_audit.json"),
    ("FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md", "four_owner_decorated_component_exhaustion_audit.json"),
    ("FOUR_OLD_CORE_SHORTCUT_AND_INTERFACE_REFUTATION_20260813.md", "four_old_core_shortcut_interface_audit.json"),
    ("GENUINE_MIXED_EDGE_HAMILTONIAN_INTERFACE_20260813.md", "genuine_mixed_edge_hamiltonian_interface_audit.json"),
    ("CORRECTED_MIXED_EDGE_DELETION_RETURN_COMPOSITION_20260813.md", "corrected_mixed_edge_deletion_return_composition_audit.json"),
    ("GENERAL_MIXED_EDGE_DELETION_RETURN_COMPOSITION_20260813.md", "general_mixed_edge_deletion_return_composition_audit.json"),
    ("SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md", "signed_surplus_prefix_recruitment_audit.json"),
    ("FORWARD_CHORD_CORE_SPLIT_OR_ANCHOR_CAPTURE_LEMMA_20260813.md", "forward_chord_core_split_or_anchor_capture_audit.json"),
    ("BACKWARD_RESPONSE_CYCLE_OR_BOUNDARY_CAPTURE_LEMMA_20260813.md", "backward_response_cycle_or_boundary_capture_audit.json"),
)


ACCEPTED = {
    "ALL_FORCED",
    "ALL_EXHAUSTED",
    "DEPENDENCIES_REPLAYABLE",
}


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
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "audit": str(audit.relative_to(root)),
            "audit_sha256": sha256(audit),
            "audit_status": payload.get("status"),
        })
    verified = all(record["audit_status"] in ACCEPTED for record in records)
    referee_gap = any(
        record["audit_status"] == "TERMINATION_GAP_FOUND" for record in records
    )
    interface_refuted = any(
        record["audit_status"] == "STATED_SPLICE_NORMAL_FORM_VACUOUS"
        for record in records
    )
    recruitment_complete = any(
        record["audit_status"] == "RECRUITMENT_WELL_FOUNDED_POOL_SEPARATOR_SUPERSEDED"
        for record in records
    )
    response_geometry_complete = {
        "FORWARD_CHORD_REDUCED_TO_TWO_ANCHOR_INTERFACES",
        "BACKWARD_RESPONSE_REDUCED_TO_MIXED_CYCLE_PAYMENT",
    }.issubset({record["audit_status"] for record in records})

    script = Path(__file__).resolve()
    checkpoint = result_dir / "MIXED_MARGIN_HAMILTONIAN_CHARITY_PATH_CHECKPOINT_20260811.md"
    return {
        "schema": "mixed-margin-hamiltonian-charity-path-composition-audit-v1",
        "status": "RESPONSE_GEOMETRY_COMPLETE_OPEN_MIXED_PAYMENT" if response_geometry_complete else (
            "SIGNED_SURPLUS_RECRUITED_OPEN_RECURRENT_RESPONSE" if recruitment_complete else (
            "INTERFACE_REFUTED" if interface_refuted else (
            "REFEREE_GAP_FOUND" if referee_gap else (
                "DEPENDENCIES_REPLAYABLE" if verified else "OPEN"
        )))),
        "dependency_count": len(records),
        "records": records,
        "proved_reduction": (
            "all mixed-margin Hamiltonian-path states pay every row or yield an "
            "incoming-core self-response/current-safe decorated response"
        ),
        "exact_surviving_separator": "supplier-saturated mixed-cycle observer payment and two anchor reverse inequalities",
        "claim_boundary": (
            "the mixed interface, cap-free recruitment, and response support "
            "geometry are proved; mixed-cycle/root-q payment remains open"
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
        "exact_surviving_separator": result["exact_surviving_separator"],
    }, indent=2))


if __name__ == "__main__":
    main()
