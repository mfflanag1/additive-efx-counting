#!/usr/bin/env python3
"""Census the dual-anchor selector across frozen full-capture profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .audit_dual_anchor_strict_separated_profile import run as run_profile
except ImportError:
    from audit_dual_anchor_strict_separated_profile import run as run_profile


PROFILE_NAMES = (
    "three_nonsingleton_flower_full_capture_arm_hub_gate.json",
    "three_nonsingleton_flower_full_capture_arm_response_gate.json",
    "three_nonsingleton_flower_full_capture_no_hub_component_growth_gate.json",
    "three_nonsingleton_flower_full_capture_no_hub_component_growth_strong_gate.json",
    "three_nonsingleton_flower_full_capture_no_hub_no_safe_gate.json",
    "three_nonsingleton_flower_full_capture_no_hub_no_two_edge_path_gate.json",
    "three_nonsingleton_flower_full_capture_no_hub_no_two_good_component_gate.json",
    "three_nonsingleton_flower_full_capture_packet_gate.json",
    "three_nonsingleton_flower_full_capture_path_gate.json",
    "three_nonsingleton_flower_full_capture_swap_gate.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    records = []
    for name in PROFILE_NAMES:
        path = root / "results" / name
        result = run_profile(root, path)
        records.append({
            "profile": f"results/{name}",
            "profile_sha256": sha256(path),
            "strict_separated_q_order": result["strict_separated_q_order"],
            "root_payable": result["root_payable"],
            "status": result["status"],
            "efx_wall_count": len(result["efx_walls"]),
            "internal_matching_count": len(result["internal_matchings"]),
            "incoming_disjoint": result["incoming_disjoint"],
            "all_incoming_supplied": result["all_incoming_supplied"],
        })

    script = Path(__file__).resolve()
    return {
        "schema": "dual-anchor-frozen-profile-census-v1",
        "status": (
            "ALL_PI_RESPONSE_MATCHING"
            if all(
                record["root_payable"]
                and record["status"] == "PI_RESPONSE_MATCHING"
                and record["incoming_disjoint"]
                and record["all_incoming_supplied"]
                for record in records
            )
            else "OPEN"
        ),
        "profile_count": len(records),
        "strict_separated_count": sum(
            record["strict_separated_q_order"] for record in records
        ),
        "records": records,
        "claim_boundary": (
            "exact-Fraction adversarial census on ten bounded representative "
            "full-capture profiles; uniform PI closure supports but does not prove "
            "the cap-free dual-anchor response theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
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
        "profiles": result["profile_count"],
        "strict_separated": result["strict_separated_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
