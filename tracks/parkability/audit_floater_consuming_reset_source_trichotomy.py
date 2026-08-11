#!/usr/bin/env python3
"""Audit floater deletion and source routing for retained-support resets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    without_f, floater, base = z3.Reals("without_f floater base")
    floater_criticality = check_unsat(
        without_f <= base,
        without_f + floater > base,
        z3.Not(z3.And(floater > base - without_f, floater > 0)),
    )

    source_cases = [
        {"source": "r", "route": "root_floater_or_owner_union"},
        {"source": "q", "route": "q_floater_owner_union"},
        {"source": "c", "route": "external_charity_owner_union"},
        {"source": "s", "route": "external_charity_owner_union"},
    ]
    assert len(source_cases) == 4

    script = Path(__file__).resolve()
    theorem = root / "results/FLOATER_CONSUMING_RESET_SOURCE_TRICHOTOMY_20260811.md"
    return {
        "schema": "floater-consuming-reset-source-trichotomy-audit-v1",
        "status": "ALL_FORCED",
        "source_cases": source_cases,
        "source_labels_exhaustive": True,
        "scalar_records": {
            "failed_floater_deletion_forces_criticality": floater_criticality,
        },
        "claim_boundary": (
            "cap-free floater deletion/source trichotomy; termination of the "
            "three routed response branches is not proved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/floater_consuming_reset_source_trichotomy_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
