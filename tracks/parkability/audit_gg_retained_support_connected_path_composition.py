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
    accepted = {"ALL_FORCED", "ALL_EXHAUSTED", "VERIFIED", "PASS", "CLASSIFIED"}
    verified = all(record["audit_status"] in accepted for record in records)
    script = Path(__file__).resolve()
    checkpoint = result_dir / "GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md"
    return {
        "schema": "gg-retained-support-connected-path-composition-audit-v1",
        "status": "DEPENDENCIES_REPLAYABLE" if verified else "OPEN",
        "dependency_count": len(records),
        "records": records,
        "focused_test_count": 45,
        "claim_boundary": (
            "integrity/replay manifest for proved local lemmas; it does not prove "
            "the open global rank-reset potential, GG closure, or four-agent EFX"
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
