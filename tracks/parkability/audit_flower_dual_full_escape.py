#!/usr/bin/env python3
"""QF_LRA checks for the flower dual-full-capture escape lemma."""

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
    tq, tr, retained, residual, bq, floater = z3.Reals(
        "tq tr retained residual bq floater"
    )
    positive = [
        tq > 0,
        tr > 0,
        retained > 0,
        residual > 0,
        bq > 0,
        floater > 0,
    ]
    records = [
        checked(
            "failed_bottom_packet_replacement_forces_dual_rotation_payment",
            positive + [tr + floater > tq + bq, floater <= bq, tr <= tq],
        ),
        checked(
            "dual_full_capture_has_no_residual_target_wall",
            positive + [tr + bq > tq + bq, tr <= tq],
        ),
        checked(
            "failed_retained_top_payment_makes_residual_payment_critical",
            positive
            + [tr == retained + residual, tr > tq, retained <= tq,
               residual <= tq - retained],
        ),
    ]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-dual-full-capture-escape-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit of the payment dichotomy; common safety, "
            "charity dominance by packet containment, and the residual desired-set "
            "edge are verified analytically in the accompanying cap-free lemma"
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
