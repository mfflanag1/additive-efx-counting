#!/usr/bin/env python3
"""Symbolic and combinatorial audit of residual-essential path top-up."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .audit_paid_response_path_core_rotation import classify
except ImportError:
    from audit_paid_response_path_core_rotation import classify


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    e_a, j, a, r_k, z_k = z3.Reals("e_a j a r_k z_k")
    y_l, b_l = z3.Reals("y_l b_l")
    symbolic = {
        "mixed_response_pays_source": prove(
            [e_a >= 0, j >= 0, a >= e_a, r_k >= 0, e_a + j > z_k],
            a + j + r_k > z_k,
        ),
        "failed_target_payment_captures_surplus": prove(
            [j >= 0, y_l >= b_l, y_l - j < b_l],
            j > y_l - b_l,
        ),
        "empty_residual_part_reduces_to_core_case": prove(
            [e_a > z_k, a >= e_a, r_k >= 0, j == 0],
            a + j + r_k > z_k,
        ),
    }
    assert all(symbolic.values())
    orders = [classify(k, l) for k in range(1, 4) for l in range(1, 4) if k != l]
    assert len(orders) == 6
    script = Path(__file__).resolve()
    theorem = root / "results/RESIDUAL_ESSENTIAL_PATH_CORE_TOPUP_LEMMA_20260813.md"
    return {
        "schema": "residual-essential-path-core-topup-audit-v1",
        "status": "ALL_RESPONSES_REDUCED_TO_TARGET_COMPENSATION_OR_CORE_ROTATION",
        "symbolic_checks": symbolic,
        "order_outcomes_after_target_payment": {
            outcome: sum(record["outcome"] == outcome for record in orders)
            for outcome in sorted({record["outcome"] for record in orders})
        },
        "surviving_separator": (
            "the minimal residual part J needed by the response source exceeds "
            "the restored target owner's complete protected surplus"
        ),
        "endpoint_joint_gate": (
            "jointly compensate target-1 residual top-up J and exchange a "
            "desired middle core against the returned hole packet P"
        ),
        "claim_boundary": (
            "source payment and target-surplus cancellation only; no universal "
            "compensation theorem or GG closure"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "separator": result["surviving_separator"]}, indent=2))


if __name__ == "__main__":
    main()
