#!/usr/bin/env python3
"""QF_LRA checks for the root-sourced evolved-target dichotomy."""

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
    tq, bq, ell, floater, a, dr, w, xq, delta = z3.Reals(
        "tq bq ell floater a dr w xq delta"
    )
    k, j, l_minus_j = z3.Reals("k j l_minus_j")
    tr, br, charity, least = z3.Reals("tr br charity least")
    positive = [
        tq > 0,
        bq > 0,
        ell > 0,
        floater > 0,
        a > 0,
        k >= 0,
        j >= 0,
        l_minus_j >= 0,
        tr > 0,
        br > 0,
        least > 0,
    ]
    identities = [
        dr == tq + floater,
        w == bq + ell,
        xq == tq + bq,
        delta == w - xq,
        delta == ell - tq,
        a == k + j,
        ell == j + l_minus_j,
    ]
    records = [
        checked(
            "anchor_return_gain_identity",
            positive
            + identities
            + [(w - a + dr) - xq != delta + dr - a],
        ),
        checked(
            "strict_gap_pays_q",
            positive
            + identities
            + [delta > 0, a - dr < delta, w - a + dr <= xq],
        ),
        checked(
            "failed_return_forces_capture_cancellation",
            positive
            + identities
            + [w - a + dr <= xq, a < ell + floater],
        ),
        checked(
            "capture_packet_is_nonempty",
            positive
            + identities
            + [a > ell + floater, k <= 0],
        ),
        checked(
            "packet_capture_identity",
            positive
            + identities
            + [a > ell + floater, k <= l_minus_j + floater],
        ),
        checked(
            "charity_containment",
            positive
            + [ell <= tr, charity == tr - ell + br, charity > tr + br - least, least <= ell],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_SOURCED_EVOLVED_TARGET_RETURN_OR_CAPTURE_LEMMA_20260811.md"
    return {
        "schema": "root-sourced-evolved-target-return-or-capture-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of the root anchor-return payment and strict capture "
            "alternative; compensation-chain termination is outside scope"
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
