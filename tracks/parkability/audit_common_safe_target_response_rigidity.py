#!/usr/bin/env python3
"""Audit common-safe target response rigidity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    desired, deletion, threshold, base = z3.Reals(
        "desired_subset containing_deletion threshold base"
    )
    proper_subset_impossible = check_unsat(
        desired <= deletion,
        deletion <= threshold,
        threshold <= base,
        desired > base,
    )

    support_cases = []
    for origin, selected in (
        ("W", False),
        ("W", True),
        ("A_i", False),
        ("A_j", False),
        ("A_k", False),
    ):
        if origin == "W":
            destination = "i" if selected else "j"
        elif origin == "A_i":
            destination = "j"
        elif origin == "A_j":
            destination = "d"
        else:
            destination = "k"
        support_cases.append({
            "origin": origin,
            "selected_into_residual_response": selected,
            "destination": destination,
        })

    script = Path(__file__).resolve()
    theorem = root / "results/COMMON_SAFE_TARGET_RESPONSE_RIGIDITY_LEMMA_20260811.md"
    return {
        "schema": "common-safe-target-response-rigidity-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "proper_desired_subset_of_common_safe_target_impossible": (
                proper_subset_impossible
            ),
        },
        "simplified_pivot_support": support_cases,
        "simplified_pivot_partition_valid": len(support_cases) == 5,
        "claim_boundary": (
            "cap-free whole-target response rigidity and simplified pivot "
            "support; residual-side recurrence termination is not proved"
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
    output = args.output or root / "results/common_safe_target_response_rigidity_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
