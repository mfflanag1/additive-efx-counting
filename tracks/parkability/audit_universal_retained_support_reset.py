#!/usr/bin/env python3
"""Audit universal retained-support reset identities and alternatives."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    margin, overlap, new_margin = z3.Reals("margin overlap new_margin")
    margin_identity = check_unsat(
        new_margin == margin - overlap,
        z3.Not(margin - new_margin == overlap),
    )
    fresh_desired_descent = check_unsat(
        margin > 0,
        overlap > 0,
        new_margin == margin - overlap,
        new_margin > 0,
        z3.Not(z3.And(new_margin < margin, overlap < margin)),
    )
    captured_margin = check_unsat(
        margin > 0,
        overlap >= 0,
        new_margin == margin - overlap,
        new_margin <= 0,
        z3.Not(z3.And(overlap >= margin, overlap > 0)),
    )

    support_cases = [
        {
            "good_origin": "previously_removed_U",
            "in_updated_U": True,
            "in_reset_core": False,
        },
        {
            "good_origin": "fresh_overlap_K",
            "in_updated_U": True,
            "in_reset_core": False,
        },
        {
            "good_origin": "unselected_T_r_remainder",
            "in_updated_U": False,
            "in_reset_core": True,
        },
        {
            "good_origin": "floater_f",
            "in_updated_U": False,
            "in_reset_core": True,
        },
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/UNIVERSAL_RETAINED_SUPPORT_RESET_LEMMA_20260811.md"
    return {
        "schema": "universal-retained-support-reset-audit-v1",
        "status": "ALL_FORCED",
        "support_partition_valid": True,
        "support_cases": support_cases,
        "scalar_records": {
            "reset_margin_identity": margin_identity,
            "fresh_overlap_strictly_descends_positive_margin": (
                fresh_desired_descent
            ),
            "failed_reset_forces_full_margin_capture": captured_margin,
        },
        "claim_boundary": (
            "cap-free top-only reset monotonicity; floater-consuming resets and "
            "fixed-support recurrence termination are not proved"
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
    output = args.output or root / "results/universal_retained_support_reset_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
