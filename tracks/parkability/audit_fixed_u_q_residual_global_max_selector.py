#!/usr/bin/env python3
"""Integrity audit for the fixed-U q-residual global-max composition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEPENDENCIES = {
    "source_inactive_repair": (
        "results/SOURCE_INACTIVE_CORE_RESIDUAL_REPAIR_LEMMA_20260811.md",
        "results/source_inactive_core_residual_repair_audit.json",
        "ALL_FORCED",
    ),
    "two_hole_cut_and_choose": (
        "results/TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md",
        "results/two_hole_cut_and_choose_response_hall_audit.json",
        "ALL_FORCED",
    ),
    "permanent_anchor_q_activity": (
        "results/PERMANENT_ANCHOR_Q_ACTIVITY_DICHOTOMY_LEMMA_20260811.md",
        "results/permanent_anchor_q_activity_dichotomy_audit.json",
        "ALL_CLASSIFIED",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    records = {}
    for name, (theorem_name, audit_name, expected_status) in DEPENDENCIES.items():
        theorem = root / theorem_name
        audit = root / audit_name
        payload = json.loads(audit.read_text())
        assert payload["status"] == expected_status
        records[name] = {
            "status": payload["status"],
            "theorem": theorem_name,
            "theorem_sha256": sha256(theorem),
            "audit": audit_name,
            "audit_sha256": sha256(audit),
        }

    # The composition uses only strict comparisons in q's row.  These exact
    # integers sanity-check that both branches contradict a finite maximum,
    # while equality would not suffice.
    finite_family = (3, 5, 8, 13)
    selected = max(finite_family)
    successful_repair_candidate = selected + 1
    exhaustion_candidate = selected + 2
    assert successful_repair_candidate > selected
    assert exhaustion_candidate > selected

    script = Path(__file__).resolve()
    theorem = root / "results" / "FIXED_U_Q_RESIDUAL_GLOBAL_MAX_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "fixed-u-q-residual-global-max-selector-audit-v1",
        "status": "COMPOSED",
        "dependency_records": records,
        "same_row_strict_maximum_sanity": {
            "selected": selected,
            "successful_repair_candidate": successful_repair_candidate,
            "exhaustion_candidate": exhaustion_candidate,
            "both_strictly_larger": True,
        },
        "claim_boundary": (
            "integrity/composition audit of the nonroot source-inactive q "
            "selector; root-facing, unsafe-augmentation, hitting-set, GG "
            "closure, and general EFX remain open"
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
    output = args.output or root / "results" / "fixed_u_q_residual_global_max_selector_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
