#!/usr/bin/env python3
"""QF_LRA checks for the flower three-rotation polarity lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name, constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run():
    rtq, rbr, rbq, rf, rbase = z3.Reals("rtq rbr rbq rf rbase")
    qtq, qtr, qbq, qbr, qf = z3.Reals("qtq qtr qbq qbr qf")
    positive = [
        rtq > 0, rbr > 0, rbq > 0, rf > 0, rbase > 0,
        qtq > 0, qtr > 0, qbq > 0, qbr > 0, qf > 0,
    ]
    records = [
        checked(
            "failed_cross_rotation_forces_r_floater_over_bottom",
            positive + [rtq + rf > rbase, rtq + rbq < rbase, rf <= rbq],
        ),
        checked(
            "failed_charity_replacement_forces_q_top_orientation",
            positive + [qtr + qf > qtq + qbq, qf <= qbq, qtr <= qtq],
        ),
        checked(
            "failed_bundle_rotation_forces_q_bottom_orientation",
            positive + [qtr + qbr <= qtq + qbq, qtr > qtq, qbr >= qbq],
        ),
    ]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-three-rotation-polarity-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit of the three payment implications; common "
            "safety and charity dominance of the displayed rotations are analytic"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
