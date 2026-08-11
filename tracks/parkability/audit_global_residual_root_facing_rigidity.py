#!/usr/bin/env python3
"""Composition audit for global-residual root-facing rigidity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


DEPENDENCIES = (
    ("FIXED_U_ARBITRARY_HOLE_RESIDUAL_SELECTOR_LEMMA_20260811.md", "fixed_u_arbitrary_hole_residual_selector_audit.json"),
    ("ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md", "root_preserving_two_hole_selector_audit.json"),
    ("ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md", "root_critical_compensator_dichotomy_audit.json"),
    ("ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md", "root_critical_alternating_frontier_audit.json"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    records = []
    for theorem_name, audit_name in DEPENDENCIES:
        theorem = root / "results" / theorem_name
        audit = root / "results" / audit_name
        payload = json.loads(audit.read_text())
        records.append({
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "audit": str(audit.relative_to(root)),
            "audit_sha256": sha256(audit),
            "audit_status": payload["status"],
        })

    root_core, residual, root_base = z3.Reals("root_core residual root_base")
    solver = z3.Solver()
    solver.add(root_core > residual, root_core > root_base)
    solver.add(z3.Or(root_core < root_base, root_core < residual))
    assert solver.check() == z3.unsat
    old, selected = z3.Reals("old selected")
    solver = z3.Solver()
    solver.add(selected >= old, selected != old, z3.Not(selected > old))
    assert solver.check() == z3.unsat

    accepted = {"ALL_FORCED", "DEPENDENCIES_REPLAYABLE"}
    verified = all(record["audit_status"] in accepted for record in records)
    theorem = root / "results/GLOBAL_RESIDUAL_ROOT_FACING_RIGIDITY_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "global-residual-root-facing-rigidity-audit-v1",
        "status": "DEPENDENCIES_REPLAYABLE" if verified else "OPEN",
        "dependency_count": len(records),
        "records": records,
        "symbolic_checks": {
            "old_partition_root_feasible": "unsat",
            "distinct_nondegenerate_selected_residual_strictly_improves": "unsat",
        },
        "terminal_supports": ["top packet", "f-only captured bottom"],
        "claim_boundary": (
            "composition audit for rigidity of common-safe root-facing "
            "partitions; top/captured-bottom fork closure and GG remain open"
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "dependency_count": result["dependency_count"]}, indent=2))


if __name__ == "__main__":
    main()
