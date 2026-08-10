#!/usr/bin/env python3
"""Replay scalar implications in the early-r dual-base reduction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Real, Solver, sat


def prove_unsat(name: str, assumptions: list, negated_claim) -> dict:
    solver = Solver()
    solver.add(*assumptions, negated_claim)
    status = solver.check()
    if status == sat:
        raise AssertionError(f"{name} is SAT: {solver.model()}")
    return {"name": name, "negated_status": str(status).upper()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/length_three_early_r_dual_base_scalar_audit.json"),
    )
    args = parser.parse_args()

    tr, br, tq = Real("tr"), Real("br"), Real("tq")
    r_minus, a_r, base_r = Real("r_minus"), Real("a_r"), Real("base_r")
    q_j, q_bq, q_missing = Real("q_j"), Real("q_bq"), Real("q_missing")
    r_j, r_bq = Real("r_j"), Real("r_bq")

    checks = [
        prove_unsat(
            "critical_pool_strictly_exceeds_r_base",
            [tr >= 0, br >= 0, tq > tr],
            br + tq <= br + tr,
        ),
        prove_unsat(
            "unsafe_boundary_is_below_r_base",
            [a_r >= 0, a_r <= r_minus, r_minus < base_r],
            a_r >= base_r,
        ),
        prove_unsat(
            "q_source_foreign_bottom_exceeds_own_bottom",
            [q_bq >= 0, q_missing >= 0, q_j > q_bq + q_missing],
            q_j <= q_bq,
        ),
        prove_unsat(
            "profitable_bottom_replacement_raises_r",
            [r_j >= 0, r_bq > r_j],
            base_r - r_j + r_bq <= base_r,
        ),
    ]

    payload = {
        "schema": "length-three-early-r-dual-base-scalar-audit-v1",
        "status": "ALL_NEGATED_IMPLICATIONS_UNSAT",
        "checks": checks,
        "claim_boundary": (
            "Checks only the four displayed additive implications in the "
            "early-r reduction. Desired-set extraction and PI routing remain "
            "analytic; the p/q cross-packet walls remain open."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
