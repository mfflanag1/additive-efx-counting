#!/usr/bin/env python3
"""QF_LRA checks for captured-q anchored residual rotation."""

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
    tq, bq, u, k, tr, br, floater, ell, good = z3.Reals(
        "tq bq u k tr br floater ell good"
    )
    xr, dr = z3.Reals("xr dr")
    positive = [
        tq > 0, bq > 0, u > 0, k >= 0, tr > 0, br > 0,
        floater > 0, ell > 0, good > 0,
    ]
    records = [
        checked("q_evolved_target_strictly_improves", positive + [u + k > tq, bq + u + k <= bq + tq]),
        checked("root_desired_core_strictly_improves", positive + [dr > xr, dr <= xr]),
        checked("charity_is_contained_in_deleted_root_bundle", positive + [
            u + k <= tr,
            ell <= u + k,
            tr - u - k + br > tr + br - ell,
        ]),
        checked("nonempty_extension_strictly_grows_support", positive + [k > 0, u + k <= u]),
        checked("relative_minimality_marks_each_new_good", positive + [
            u + k > tq,
            u + k - good <= tq,
            good < u + k - tq,
        ]),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md"
    return {
        "schema": "captured-q-margin-anchored-residual-rotation-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of the anchored residual-rotation payments and support "
            "growth; response/Hall termination is outside scope"
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
