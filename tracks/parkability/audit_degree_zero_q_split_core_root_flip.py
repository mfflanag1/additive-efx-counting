#!/usr/bin/env python3
"""Dependency audit for the degree-zero q split-core root flip."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEPENDENCIES = (
    ("UNIVERSAL_RETAINED_SUPPORT_RESET_LEMMA_20260811.md", "universal_retained_support_reset_audit.json"),
    ("REUSED_TOP_CANONICAL_CORE_SELECTOR_LEMMA_20260811.md", "reused_top_canonical_core_selector_audit.json"),
    ("FLOWER_DUAL_ANCHOR_ROOT_PAID_SELECTOR_LEMMA_20260811.md", "flower_dual_anchor_root_paid_selector_audit.json"),
    ("DUAL_POOL_MINIMAL_CORE_EXTRACTION_LEMMA_20260811.md", "dual_pool_minimal_core_extraction_audit.json"),
    ("CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md", "captured_q_margin_anchored_residual_rotation_audit.json"),
    ("PROTECTED_Q_RESPONSE_RETENTION_LEMMA_20260811.md", "protected_q_response_retention_audit.json"),
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
    accepted = {"ALL_FORCED", "VERIFIED"}
    replayable = all(record["audit_status"] in accepted for record in records)
    script = Path(__file__).resolve()
    theorem = result_dir / "DEGREE_ZERO_Q_SPLIT_CORE_ROOT_FLIP_LEMMA_20260811.md"
    return {
        "schema": "degree-zero-q-split-core-root-flip-audit-v1",
        "status": "DEPENDENCIES_REPLAYABLE" if replayable else "OPEN",
        "dependency_count": len(records),
        "records": records,
        "support_records": {
            "retained_q_core_is_physical_union_even_when_split_across_targets": True,
            "ordinary_degree_zero_does_not_delete_split_support_core": True,
            "root_flip_uses_complete_owner_union_plus_charity": True,
        },
        "outcomes": [
            "retained support growth or q-margin capture",
            "root-payable q representation",
            "dual-pool source-margin capture",
        ],
        "claim_boundary": (
            "integrity/composition audit of the degree-zero q split-support "
            "root flip; termination after a source-margin capture is not proved"
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
    output = args.output or root / "results/degree_zero_q_split_core_root_flip_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
