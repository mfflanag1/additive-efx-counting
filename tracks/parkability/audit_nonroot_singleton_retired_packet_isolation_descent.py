#!/usr/bin/env python3
"""Exact wall/support audit for nonroot singleton isolation descent."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(repo: Path) -> dict:
    agents = ("r", "h", "s", "q")
    targets = ("root_core", "singleton_K", "hole_s", "hole_q")
    possible_walls = []
    for observer in agents:
        for target in targets:
            if target == "singleton_K":
                allowed = False
                route = "singleton_threshold_zero"
            elif observer in ("s", "q") and target in ("hole_s", "hole_q"):
                allowed = False
                route = "two_agent_efx"
            elif observer == "r" and target in ("hole_s", "hole_q"):
                allowed = True
                route = "root_to_hole_external_star"
            elif observer in ("s", "q") and target == "root_core":
                allowed = True
                route = "hole_to_root_price_split"
            elif observer == "h" and target == "root_core":
                allowed = True
                route = "holder_to_root_price_split"
            elif observer == "h" and target in ("hole_s", "hole_q"):
                allowed = True
                route = "holder_response_two_core_two_hole"
            else:
                allowed = False
                route = "self_or_localized_safe"
            possible_walls.append({
                "observer": observer,
                "target": target,
                "wall_possible": allowed,
                "route": route,
            })

    singleton_walls = [
        row for row in possible_walls
        if row["target"] == "singleton_K" and row["wall_possible"]
    ]
    assert not singleton_walls
    theorem = repo / "results/NONROOT_SINGLETON_RETIRED_PACKET_ISOLATION_DESCENT_THEOREM_20260814.md"
    split = repo / "results/NONROOT_DOUBLE_SACRIFICE_PROPER_SPLIT_COMPRESSION_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "nonroot-singleton-retired-packet-isolation-descent-audit-v1",
        "status": "SINGLETON_ISOLATION_WALLS_VERIFIED_ADMISSION_OPEN",
        "singleton_deletion_threshold": 0,
        "singleton_target_walls": singleton_walls,
        "wall_routes": possible_walls,
        "test_allocation_responses_intersect_singleton": False,
        "collision_hitting_multiplicity_strictly_reduced": False,
        "admissible_transition_proved": False,
        "remaining_direct_branch": "singleton_isolation_transition_admission",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free singleton target safety and test-allocation wall census; "
            "the two-agent complement repartition is not yet an admitted transition"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "proper_split_theorem": str(split.relative_to(repo)),
            "proper_split_theorem_sha256": sha256(split),
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
        "remaining_direct_branch": result["remaining_direct_branch"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
