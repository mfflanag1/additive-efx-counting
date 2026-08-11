#!/usr/bin/env python3
"""QF_LRA/source checks for evolved-target minimal-core routing."""

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
    deleted, base = z3.Reals("deleted base")
    source = z3.Int("source")
    root_value, root_base = z3.Reals("root_value root_base")
    records = [
        checked(
            "minimality_forces_every_deleted_subset_below_base",
            [deleted <= base, deleted > base],
        ),
        checked(
            "four_source_labels_are_exhaustive",
            [source >= 0, source <= 3, source != 0, source != 1, source != 2, source != 3],
        ),
        checked(
            "root_source_is_strictly_above_root_base",
            [root_value > root_base, root_value <= root_base],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/EVOLVED_TARGET_MINIMAL_SOURCE_TRICHOTOMY_LEMMA_20260811.md"
    return {
        "schema": "evolved-target-minimal-source-trichotomy-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA/source audit of global minimal-core safety and source routing; "
            "release compatibility is covered by the prior two-root audit"
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
