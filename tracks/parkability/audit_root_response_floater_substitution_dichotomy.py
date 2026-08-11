#!/usr/bin/env python3
"""QF_LRA checks for root-response floater substitution."""

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
    tq, bq, tr, ell, j, omitted, floater = z3.Reals(
        "tq bq tr ell j omitted floater"
    )
    kq, kr, ar, xr, mu = z3.Reals("kq kr ar xr mu")
    zr, zq, pool = z3.Reals("zr zq pool")
    positive = [
        tq > 0,
        bq > 0,
        tr > 0,
        ell > 0,
        j >= 0,
        omitted >= 0,
        floater > 0,
        kq > 0,
        kr > 0,
    ]
    identities = [
        ell == j + omitted,
        ar == kr + j,
        mu == ar - xr,
        zr == j + floater,
        zq == tq + bq + omitted,
        pool == (tq + floater) + (bq + ell),
    ]
    records = [
        checked(
            "substitution_conserves_support",
            positive + identities + [zr + zq != pool],
        ),
        checked(
            "proper_omission_strictly_improves_q",
            positive + identities + [omitted > 0, zq <= tq + bq],
        ),
        checked(
            "root_failure_forces_margin_capture",
            positive
            + identities
            + [ar > xr, zr < xr, kr <= floater + mu],
        ),
        checked(
            "q_capture_is_preserved",
            positive + identities + [kq > omitted + floater, kq <= omitted + floater],
        ),
        checked(
            "root_capture_is_strict",
            positive
            + identities
            + [ar > xr, zr < xr, kr - floater <= ar - xr],
        ),
        checked(
            "root_target_is_contained_in_mutual_core",
            positive + identities + [ell <= tr, j + floater > tr + floater],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_RESPONSE_FLOATER_SUBSTITUTION_DICHOTOMY_LEMMA_20260811.md"
    return {
        "schema": "root-response-floater-substitution-dichotomy-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of floater substitution and the joint packet capture; "
            "external-core hitting-set termination is outside scope"
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
