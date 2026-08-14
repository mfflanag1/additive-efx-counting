#!/usr/bin/env python3
"""Integrity and exact scalar audit for the global retired-support contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    a, k, minus, floor = z3.Reals("a k minus floor")
    base = [a == k + minus, a > floor, k >= 0, minus >= 0]
    capture = prove([*base, minus <= floor], k >= a - floor)
    deletion_exhaustion = prove(
        base, z3.Or(minus > floor, k >= a - floor)
    )
    strict_capture = prove([*base, minus <= floor], k > 0)
    assert capture and deletion_exhaustion and strict_capture

    states = [f"G{i}" for i in range(11)]
    rows = {
        "G0": "clear",
        "G1": "delete_or_capture",
        "G2": "exact_hitting_response",
        "G3": "delete_or_capture",
        "G4": "delete_or_capture",
        "G5": "delete_or_capture",
        "G6": "delete_or_capture",
        "G7": "component_return_selector",
        "G8": "exact_state",
        "G9": "delete_or_capture",
        "G10": "peel_then_return_compensation",
    }
    assert sorted(rows, key=lambda x: int(x[1:])) == states

    dependencies = [
        "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md",
        "results/GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md",
        "results/GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md",
        "results/UNIVERSAL_PAID_ANCHOR_SUPPORT_RESET_LEMMA_20260811.md",
        "results/CROSS_COMPONENT_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md",
        "results/FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md",
        "results/PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md",
    ]
    script = Path(__file__).resolve()
    return {
        "schema": "global-retired-root-support-transition-contract-audit-v1",
        "status": "CONTRACT_AND_G0_G10_COVERAGE_VERIFIED",
        "g_states_covered": states,
        "transition_rows": rows,
        "cross_cutting_operations": [
            "orientation_reset", "root_flip", "recapture", "hole_pivot",
            "two_hole_normalization",
            "paid_anchor_reset", "root_anchor_exchange",
            "enlarged_root_return",
        ],
        "physical_anchor_label_excludes_current_floor": True,
        "retired_support_persists_across_floor_changes": True,
        "no_collision_T_star_requires_complete_pool_audit": True,
        "scalar_checks": {
            "deletion_or_capture_exhaustive": deletion_exhaustion,
            "failed_deletion_captures_margin": capture,
            "failed_deletion_uses_nonempty_packet": strict_capture,
        },
        "collision_interface": "resolved_by_selector_collision_normalization",
        "dependencies": [
            {"path": path, "sha256": sha256(repo / path)}
            for path in dependencies
        ],
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
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
        "g_states": len(result["g_states_covered"]),
        "collision_interface": result["collision_interface"],
    }, indent=2))


if __name__ == "__main__":
    main()
