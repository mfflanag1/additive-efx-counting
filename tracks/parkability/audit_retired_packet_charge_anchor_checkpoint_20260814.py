#!/usr/bin/env python3
"""Provenance/status audit for the Aug-14 charge-or-anchor checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    checkpoint = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CHECKPOINT_20260814.md"
    files = [
        checkpoint,
        ROOT / "results/AUG14_COLLISION_CANDIDATE_TRANSITION_ADMISSIBILITY_AUDIT_20260814.md",
        ROOT / "results/CANONICAL_WHOLE_HIT_BILATERAL_SWAP_OR_SOURCE_UNDERPAYMENT_LEMMA_20260814.md",
        ROOT / "results/RETIREMENT_SUPPLIER_THREE_CYCLE_OR_TWO_ROW_CUT_LEMMA_20260814.md",
        ROOT / "results/FOUR_OWNER_CURRENT_BUNDLE_COMPENSATION_PATH_HALL_THEOREM_20260814.md",
        ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md",
        Path(__file__).resolve(),
    ]
    text = checkpoint.read_text()
    required = (
        "theorem not yet proved or refuted",
        "five-path current-bundle Hall cut",
        "protected/base-floor response",
        "No complete-contract counterexample",
    )
    assert all(phrase in text for phrase in required)
    return {
        "schema": "retired-packet-charge-anchor-checkpoint-20260814-audit-v1",
        "status": "CURRENT_WHOLE_HIT_REDUCED_TO_FIVE_PATH_HALL_CUT",
        "conditional_global_candidates_downgraded": True,
        "current_response_path_family_exhausted": True,
        "protected_floor_response_closed": False,
        "normalization_bypass_closed": False,
        "full_T_L_times_theorem_closed": False,
        "full_T_L_times_theorem_refuted": False,
        "next_gate": "GG_inequalities_force_compensation_path_or_anchor_exchange",
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path) for path in files
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
