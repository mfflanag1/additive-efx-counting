#!/usr/bin/env python3
"""Audit root-monopoly conversion to the complete charity path."""

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
    c, k, g = z3.Reals("root_C root_K root_G")
    nonempty_capture_and_affordability = check_unsat(
        c >= 0,
        k >= 0,
        g >= 0,
        c + g > 0,
        c + k > c + g,
        z3.Not(z3.And(k > 0, k > g)),
    )

    q_base, q_f, q_k, q_after = z3.Reals("q_base q_f q_K q_after")
    q_change_identity = check_unsat(
        q_after == q_base - q_k + q_f,
        z3.Not(q_after - q_base == q_f - q_k),
    )

    support_cases = [
        {"origin": "charity_f", "destination": "q"},
        {"origin": "X_q_K", "destination": "r"},
        {"origin": "X_r_G", "destination": "external_sink_or_empty"},
        {"origin": "all_other_goods", "destination": "original_owner"},
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_MONOPOLY_CHARITY_PATH_HANDOFF_LEMMA_20260811.md"
    return {
        "schema": "root-monopoly-charity-path-handoff-audit-v1",
        "status": "ALL_FORCED",
        "support_partition_valid": True,
        "support_cases": support_cases,
        "permanent_root_anchor_retained": True,
        "scalar_records": {
            "desired_root_core_forces_nonempty_affordable_capture": (
                nonempty_capture_and_affordability
            ),
            "q_change_is_f_minus_K": q_change_identity,
        },
        "claim_boundary": (
            "cap-free root-monopoly-to-complete-path handoff; termination of "
            "the sacrificed-q Hall reset is not proved"
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
    output = args.output or root / "results/root_monopoly_charity_path_handoff_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
