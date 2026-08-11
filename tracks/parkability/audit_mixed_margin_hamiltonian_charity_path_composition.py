#!/usr/bin/env python3
"""Integrity manifest for the mixed-margin Hamiltonian charity-path chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEPENDENCIES = (
    ("FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md", "full_signed_transfer_state_reconstruction_audit.json"),
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
    ("COMPONENT_WIDE_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "component_wide_return_compensation_selector_audit.json"),
    ("COMPONENT_WIDE_CURRENT_OR_BASE_FLOOR_HANDOFF_LEMMA_20260811.md", "component_wide_current_or_base_floor_handoff_audit.json"),
    ("FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md", "four_owner_decorated_component_exhaustion_audit.json"),
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

    script = Path(__file__).resolve()
    checkpoint = result_dir / "MIXED_MARGIN_HAMILTONIAN_CHARITY_PATH_CHECKPOINT_20260811.md"
    return {
        "schema": "mixed-margin-hamiltonian-charity-path-composition-audit-v1",
        "status": "DEPENDENCIES_REPLAYABLE" if verified else "OPEN",
        "dependency_count": len(records),
        "records": records,
        "proved_reduction": (
            "all mixed-margin states reduce to EFX/lex, PI, support/response "
            "progress, or the six-clause full-owner critical-top-up separator"
        ),
        "exact_surviving_separator": (
            "anchor-containing full-owner target-critical top-up failure after "
            "Bq floater substitution and root-source anchor return, with the "
            "remaining physical role obstruction at q-source collision"
        ),
        "claim_boundary": (
            "integrity and reduction manifest only; the critical-top-up separator, "
            "mixed-margin theorem, GG, and EFX remain open"
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
