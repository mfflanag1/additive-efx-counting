#!/usr/bin/env python3
"""Audit the scalar implications in the top-core residual-reset lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    (
        r_tq_rest,
        r_kt,
        r_tr_rest,
        r_payment,
        r_f,
        r_br,
        q_tq,
        q_tr,
        q_f,
        q_bq,
    ) = z3.Reals(
        "r_tq_rest r_kt r_tr_rest r_payment r_f r_br "
        "q_tq q_tr q_f q_bq"
    )
    positive = [
        value > 0
        for value in (
            r_tq_rest,
            r_kt,
            r_tr_rest,
            r_payment,
            r_f,
            r_br,
            q_tq,
            q_tr,
            q_f,
            q_bq,
        )
    ]

    r_complement = z3.SolverFor("QF_LRA")
    r_complement.add(
        *positive,
        r_tq_rest + r_kt + r_f > r_tr_rest + r_payment + r_br,
        r_br >= r_f,
        r_payment > r_kt,
        r_tq_rest <= r_tr_rest,
    )
    r_status = str(r_complement.check())
    assert r_status == "unsat"

    q_rotation = z3.SolverFor("QF_LRA")
    q_rotation.add(
        *positive,
        q_tr + q_f > q_tq + q_bq,
        q_bq > q_f,
        q_tr <= q_tq,
    )
    q_status = str(q_rotation.check())
    assert q_status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "top-core-residual-reset-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "reverse_top_core_forces_strict_complement_order",
                "status": r_status,
            },
            {
                "claim": "live_bottom_polarity_forces_residual_rotation_payment",
                "status": q_status,
            },
        ],
        "claim_boundary": (
            "QF_LRA audit of the two strict scalar implications only; "
            "minimal packet selection, EFX-with-charity reduction, and "
            "response-Hall composition are analytic"
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
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
