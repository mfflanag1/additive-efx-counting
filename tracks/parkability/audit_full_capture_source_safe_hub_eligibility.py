#!/usr/bin/env python3
"""QF_LRA checks for the source-safe full-capture hub-eligibility lemma."""

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
    status = str(solver.check())
    return {"claim": name, "status": status}


def run(root: Path | None = None) -> dict:
    tq, tr, bq, br, floater, mu, b, h = z3.Reals(
        "tq tr bq br floater mu b h"
    )
    positive = [
        tq > 0,
        tr > 0,
        bq > 0,
        br > 0,
        floater > 0,
        mu > 0,
        b > 0,
        h > 0,
    ]

    xr = tr + br
    dr_tail = tq + floater - mu

    payment_ar, payment_xr, payment_xc = z3.Reals(
        "payment_ar payment_xr payment_xc"
    )
    tail_dr, tail_ar, tail_xc = z3.Reals("tail_dr tail_ar tail_xc")

    records = [
        checked(
            "singleton_bottom_source_safe_pays_fourth_cover",
            positive + [bq == b, br >= h, h >= b, tq + br < tq + bq],
        ),
        checked(
            "cross_pair_no_eligibility_controls_reservoir_minimum",
            positive
            + [floater <= mu + b, br >= h, h >= b, br + mu < floater],
        ),
        checked(
            "floater_minimum_controls_reservoir_minimum",
            positive + [mu == floater, br + mu < floater],
        ),
        checked(
            "desired_dual_bundle_forces_xr_over_dr_tail",
            positive
            + [
                tr + floater > tq + bq,
                bq >= floater,
                br + mu >= floater,
                xr <= dr_tail,
            ],
        ),
        checked(
            "three_unpaid_cover_walls_are_inconsistent",
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
    if root is None:
        root = script.parents[2]
    theorem = root / "results/FULL_CAPTURE_SOURCE_SAFE_HUB_ELIGIBILITY_LEMMA_20260810.md"
    return {
        "schema": "full-capture-source-safe-hub-eligibility-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit of the source-safe full-capture dichotomy: "
            "a singleton B_q pays the fourth common-safe cover, while a nonsingleton "
            "B_q plus absence of q-hub eligibility forces X_r above the D_r tail and "
            "makes the three remaining q-unpaid cover walls inconsistent; availability "
            "of a source-safe improving bottom pair is a separate premise"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
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
