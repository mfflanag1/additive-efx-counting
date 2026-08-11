#!/usr/bin/env python3
"""QF_LRA checks for the captured-bottom compensation chain."""

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


def run(root: Path) -> dict:
    p, aa, c, b = z3.Reals("p aa c b")
    tr, br, h, bq, xc, xs, xr = z3.Reals(
        "tr br h bq xc xs xr"
    )
    va_aa, va_xa, va_c, va_bq, va_k = z3.Reals(
        "va_aa va_xa va_c va_bq va_k"
    )
    vq_dq, vq_xq, vq_k, vq_bq, vq_br, vq_c = z3.Reals(
        "vq_dq vq_xq vq_k vq_bq vq_br vq_c"
    )
    positive = [
        p > 0,
        aa > 0,
        c > 0,
        b >= 0,
        tr > 0,
        br > 0,
        h > 0,
        bq > 0,
        xc > 0,
        xs > 0,
        xr > 0,
        va_aa > va_xa,
        va_c > 0,
        va_bq > 0,
        va_k > 0,
        vq_dq > vq_xq,
        vq_k >= 0,
        vq_bq > 0,
        vq_br > 0,
        vq_c >= 0,
    ]

    records = [
        checked(
            "exchange_targets_conserve_support",
            positive + [p + c - b + aa - c + b != p + aa],
        ),
        checked(
            "c_exhaustion_cancels_to_root_top_concentration",
            positive
            + [
                p == br - h + bq + xc + xs,
                xr == tr + br,
                p + h - b < xr,
                tr <= bq - b + xc + xs,
                bq >= b,
                br >= h,
            ],
        ),
        checked(
            "b_exhaustion_captures_external_margin",
            positive
            + [va_aa - va_c + va_bq <= va_xa, va_c - va_bq < va_aa - va_xa],
        ),
        checked(
            "live_q_order_reverses_external_capture",
            positive + [vq_bq > vq_br, vq_br >= vq_c, vq_bq <= vq_c],
        ),
        checked(
            "same_source_switch_prefers_root_top",
            positive
            + [
                va_k + va_bq > va_xa,
                va_aa - va_c + va_bq <= va_xa,
                va_k <= va_aa - va_c,
            ],
        ),
        checked(
            "q_switch_failure_captures_margin",
            positive + [vq_dq - vq_k <= vq_xq, vq_k < vq_dq - vq_xq],
        ),
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/CAPTURED_BOTTOM_EXTERNAL_COMPENSATION_CHAIN_LEMMA_20260811.md"
    return {
        "schema": "captured-bottom-external-compensation-chain-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of the finite bottom-transfer chain endpoints; "
            "it does not terminate the resulting top-switch or source-capture handoff"
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
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
