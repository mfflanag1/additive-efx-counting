#!/usr/bin/env python3
"""QF_LRA checks for minimal dual-core extraction."""

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
    p, xr, c, g, outside = z3.Reals("p xr c g outside")
    dq, xq, cq = z3.Reals("dq xq cq")
    aa, xa, ca = z3.Reals("aa xa ca")
    tr, h, bq, xc, xs, br_rest = z3.Reals(
        "tr h bq xc xs br_rest"
    )
    positive = [
        p > 0,
        xr > 0,
        c > 0,
        g > 0,
        outside > 0,
        dq > xq,
        aa > xa,
        cq >= 0,
        ca >= 0,
        tr > 0,
        h > 0,
        bq > 0,
        xc > 0,
        xs > 0,
        br_rest >= 0,
    ]
    delta = xr - p

    records = [
        checked(
            "full_dual_union_always_pays_root",
            positive
            + [p + dq + aa == xr + outside, p + dq + aa <= xr],
        ),
        checked(
            "minimal_extraction_is_nonempty",
            positive + [p < xr, c == 0, p + c >= xr],
        ),
        checked(
            "minimal_good_is_root_critical",
            positive + [p + c >= xr, p + c - g < xr, g <= c - delta],
        ),
        checked(
            "root_threshold_rewrite",
            positive + [p + c >= xr, c < delta],
        ),
        checked(
            "q_source_failure_captures_margin",
            positive + [dq - cq <= xq, cq < dq - xq],
        ),
        checked(
            "external_source_failure_captures_margin",
            positive + [aa - ca <= xa, ca < aa - xa],
        ),
        checked(
            "full_capture_deficit_cancellation",
            positive
            + [
                p == br_rest + bq + xc + xs,
                xr == tr + br_rest + h,
                p < xr,
                tr + h <= bq + xc + xs,
            ],
        ),
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/DUAL_POOL_MINIMAL_CORE_EXTRACTION_LEMMA_20260811.md"
    return {
        "schema": "dual-pool-minimal-core-extraction-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of minimal root-payment extraction and source-margin "
            "capture; it does not compensate a displaced source"
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
