#!/usr/bin/env python3
"""QF_LRA audit of the bilateral item-swap obstruction signs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tau(core, minimum, item):
    return core + z3.If(item >= minimum, item - minimum, 0)


def forced(name, constraints, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    solver.add(z3.Not(conclusion))
    return {"case": name, "status": "FORCED" if solver.check() == z3.unsat else "FAILED"}


def run() -> dict:
    core, minimum_value, h, b, own, old_target = z3.Reals(
        "core minimum_value h b own old_target"
    )
    positive = (
        core >= 0, minimum_value > 0, h > 0, b > 0,
        own > 0, old_target >= 0,
    )
    records = [
        forced(
            "strict_target_increase_forces_b_above_h",
            positive + (tau(core, minimum_value, b) > tau(core, minimum_value, h),),
            b > h,
        ),
        forced(
            "strict_reverse_target_increase_forces_h_above_b",
            positive + (tau(core, minimum_value, h) > tau(core, minimum_value, b),),
            h > b,
        ),
        forced(
            "improving_r_cannot_fail_against_changed_q_target",
            positive + (
                b > h,
                own >= tau(core, minimum_value, b),
                own - h + b < tau(core, minimum_value, h),
            ),
            z3.BoolVal(False),
        ),
        forced(
            "nonlosing_q_cannot_fail_against_changed_r_target",
            positive + (
                h >= b,
                own >= tau(core, minimum_value, h),
                own - b + h < tau(core, minimum_value, b),
            ),
            z3.BoolVal(False),
        ),
    ]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "bilateral-swap-obstruction-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "records": records,
        "claim_boundary": "QF_LRA replay of threshold monotonicity and the two owner-safety implications used by the analytic lemma",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
