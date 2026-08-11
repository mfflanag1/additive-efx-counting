#!/usr/bin/env python3
"""QF_LRA checks for the reused-top canonical-core selector."""

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
    total, fixed, k, kp, pool, poolp, xr = z3.Reals(
        "total fixed k kp pool poolp xr"
    )
    records = [
        checked("complement_cancellation", [
            pool == total - fixed - k,
            poolp == total - fixed - kp,
            poolp - pool != k - kp,
        ]),
        checked("minimum_root_core_maximizes_complement", [
            pool == total - fixed - k,
            poolp == total - fixed - kp,
            k <= kp,
            pool < poolp,
        ]),
        checked("canonical_deficit_propagates_to_every_reused_core", [
            pool == total - fixed - k,
            poolp == total - fixed - kp,
            k <= kp,
            pool < xr,
            poolp >= xr,
        ]),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/REUSED_TOP_CANONICAL_CORE_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "reused-top-canonical-core-selector-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of root-pool maximization across all common-safe "
            "external responses disjoint from a fixed mutual core; unsafe and "
            "root-sourced responses are outside scope"
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
