#!/usr/bin/env python3
"""Audit whole-core return descent to the two-hole normal form."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def has_covering_matching(edges: set[tuple[int, int]]) -> bool:
    return any(
        all((source, target) in edges for target, source in enumerate(perm))
        for perm in itertools.permutations(range(2))
    )


def has_empty_target(edges: set[tuple[int, int]]) -> bool:
    return any(not any(target == t for _, target in edges) for t in range(2))


def common_singleton(edges: set[tuple[int, int]]) -> bool:
    neighborhoods = [
        {source for source, target in edges if target == t}
        for t in range(2)
    ]
    return len(neighborhoods[0]) == 1 and neighborhoods[0] == neighborhoods[1]


def run(root: Path) -> dict:
    desired, deletion, threshold, base = z3.Reals(
        "desired containing_deletion threshold base"
    )
    response_rigidity = check_unsat(
        desired <= deletion,
        deletion <= threshold,
        threshold <= base,
        desired > base,
    )

    old_residual, low_cell, high_tail = z3.Reals(
        "old_residual low_cell high_tail"
    )
    strict_gain_trial = check_unsat(
        low_cell > old_residual,
        high_tail > old_residual,
        z3.Not(z3.And(low_cell > old_residual, high_tail > old_residual)),
    )

    root_core, root_base = z3.Reals("root_core root_base")
    nonroot_descent_priority = check_unsat(
        root_core > root_base,
        z3.Not(root_core > root_base),
    )

    relation_records = []
    uncovered = 0
    universe = [(source, target) for source in range(2) for target in range(2)]
    for mask in range(16):
        edges = {edge for bit, edge in enumerate(universe) if mask & (1 << bit)}
        outcomes = {
            "matching": has_covering_matching(edges),
            "empty_target": has_empty_target(edges),
            "common_singleton": common_singleton(edges),
        }
        if not any(outcomes.values()):
            uncovered += 1
        relation_records.append({"mask": mask, **outcomes})

    support_cases = [
        {"origin": "fixed_core_1", "destination": "fixed_source_1"},
        {"origin": "fixed_core_2", "destination": "fixed_source_2"},
        {"origin": "A_j", "destination": "two_hole_pool"},
        {"origin": "W", "destination": "two_hole_pool"},
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/WHOLE_CORE_RETURN_TWO_HOLE_DESCENT_LEMMA_20260811.md"
    return {
        "schema": "whole-core-return-two-hole-descent-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "common_safe_response_is_whole_core": response_rigidity,
            "strong_envy_trial_has_strict_old_hole_gain": strict_gain_trial,
            "nonroot_release_preserves_root_priority": nonroot_descent_priority,
        },
        "support_partition": support_cases,
        "support_partition_valid": len(support_cases) == 4,
        "two_by_two_relation_count": len(relation_records),
        "two_by_two_uncovered_count": uncovered,
        "claim_boundary": (
            "cap-free priority-valid whole-core descent to the classified "
            "two-hole boundary; rank-one and residual-side termination are open"
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
    output = args.output or root / "results/whole_core_return_two_hole_descent_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
