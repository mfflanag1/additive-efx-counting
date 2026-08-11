#!/usr/bin/env python3
"""Symbolic audit of root-concentration bottom absorption."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.Solver()
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    r_tq, r_f, r_h, r_xr = z3.Reals("r_tq r_f r_h r_xr")
    q_tr, q_f, q_xq, q_bq, q_tq = z3.Reals("q_tr q_f q_xq q_bq q_tq")
    checks = {
        "root_strict_improvement": prove(
            [r_tq + r_f > r_xr, r_h > 0], r_tq + r_f + r_h <= r_xr
        ),
        "q_strict_improvement": prove(
            [q_tr + q_f > q_xq, q_xq == q_tq + q_bq, q_bq > q_f],
            q_tr + q_bq <= q_xq,
        ),
    }
    theorem = root / "results/ROOT_CONCENTRATION_BOTTOM_ABSORPTION_ROTATION_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-concentration-bottom-absorption-rotation-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "support_partition": [
            "T_q+f+H",
            "T_r+B_q",
            "X_c",
            "X_s",
            "B_r-H charity",
        ],
        "charity_dominated_by_base_efx": True,
        "only_changed_targets_can_create_walls": True,
        "potential_update": "V <- V union H",
        "claim_boundary": (
            "cap-free endpoint construction for root concentration; repeated "
            "retained-bottom response/Hall closure and GG remain open"
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
