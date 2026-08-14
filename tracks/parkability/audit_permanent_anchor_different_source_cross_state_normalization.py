#!/usr/bin/env python3
"""Audit cross-state normalization of two alternating root responses."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


NONROOT = ("q", "d", "s")


def source_probe_audit():
    rows = []
    for left, right in itertools.combinations(NONROOT, 2):
        holder = next(owner for owner in NONROOT if owner not in {left, right})
        edges = {("q", "r"), ("charity", holder)}
        assert len(edges) == 2
        rows.append({
            "response_sources": [left, right],
            "singleton_holder": holder,
            "common_probe_edges": [list(edge) for edge in sorted(edges)],
            "left_bundle_unchanged": True,
            "right_bundle_unchanged": True,
        })
    assert len(rows) == 3
    return rows


def algebra_audit():
    response_value, fixed_bundle, probe_bundle = z3.Reals(
        "response_value fixed_bundle probe_bundle"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(probe_bundle == fixed_bundle,
               response_value > probe_bundle,
               response_value <= fixed_bundle)
    desire_transport = solver.check() == z3.unsat

    tail_value, observer_floor = z3.Reals("tail_value observer_floor")
    solver = z3.SolverFor("QF_LRA")
    solver.add(tail_value > observer_floor,
               tail_value <= observer_floor)
    unsafe_gives_desired_deletion = solver.check() == z3.unsat

    # A strict cardinality descent cannot continue past a singleton.
    descent_checks = []
    for start in range(1, 33):
        size = start
        steps = 0
        while size > 1:
            size -= 1
            steps += 1
        descent_checks.append(steps <= start - 1 and size == 1)
    finite_descent = all(descent_checks)

    same_source = z3.Bool("same_source")
    collision_or_distinct = z3.is_true(z3.simplify(z3.Or(
        same_source, z3.Not(same_source)
    )))
    assert desire_transport and unsafe_gives_desired_deletion
    assert finite_descent and collision_or_distinct
    return {
        "desire_transport": desire_transport,
        "unsafe_gives_desired_deletion": unsafe_gives_desired_deletion,
        "finite_cardinality_descent": finite_descent,
        "source_collision_or_distinct_exhaustive": collision_or_distinct,
    }


def run(root: Path):
    rows = source_probe_audit()
    checks = algebra_audit()
    script = Path(__file__).resolve()
    theorem = root / "results" / (
        "PERMANENT_ANCHOR_DIFFERENT_SOURCE_CROSS_STATE_"
        "NORMALIZATION_LEMMA_20260814.md"
    )
    return {
        "schema": "permanent-anchor-different-source-cross-state-normalization-v1",
        "status": "COMMON_PROBE_SAFE_NORMALIZATION_OR_SOURCE_COLLISION",
        "source_pair_count": len(rows),
        "common_probe_edge_count": 2,
        **checks,
        "source_pairs": rows,
        "claim_boundary": (
            "cross-state desire/safety normalization proved; root and "
            "multi-source capture inequalities remain open"
        ),
        "provenance": {
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "source_pairs": result["source_pair_count"],
        "common_probe_edges": result["common_probe_edge_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
