#!/usr/bin/env python3
"""QF_LRA checks for the full-capture singleton-replacement selector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run() -> dict:
    tq, tr, bq, br, floater = z3.Reals("tq tr bq br floater")
    payment_ar, payment_xr, payment_xc = z3.Reals(
        "payment_ar payment_xr payment_xc"
    )
    tail_dr, tail_ar, tail_xc = z3.Reals("tail_dr tail_ar tail_xc")

    records = [
        checked(
            "no_single_replacement_and_dual_desire_force_xr_over_dr_tail",
            [
                tq > 0,
                tr > 0,
                bq > 0,
                br > 0,
                floater > 0,
                bq >= floater,
                tr + floater > tq + bq,
                tail_dr == tq,
                payment_xr == tr + br,
                payment_xr <= tail_dr,
            ],
        ),
        checked(
            "three_q_unpaid_cover_walls_are_inconsistent",
            [
                payment_xr > tail_dr,
                tail_xc < payment_xc,
                tail_ar < payment_ar,
                z3.Or(payment_ar < tail_dr, payment_ar < tail_xc),
                z3.Or(payment_xr < tail_dr, payment_xr < tail_xc),
                z3.Or(payment_xc < tail_dr, payment_xc < tail_ar),
            ],
        ),
    ]

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "full-capture-single-replacement-selector-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit: if q has no improving single-good "
            "packet-for-charity replacement, D_q desire puts X_r above the D_r "
            "tail, making the three remaining q-unpaid cover walls inconsistent; "
            "wall-to-component routing after selecting the good is separate"
        ),
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
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
