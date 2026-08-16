#!/usr/bin/env python3
"""Split a factored Hall SMT-LIB master into an exact Z3 cube cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "smt2-cube-cover-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split(source, output_dir, depth, timeout_seconds, base_good_symmetry=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.from_file(str(source))
    symmetry_constraints = []
    if base_good_symmetry:
        for left, right in ((6, 7), (1, 2), (2, 3), (0, 4)):
            constraint = z3.Real(f"v_0_{left}") <= z3.Real(f"v_0_{right}")
            solver.add(constraint)
            symmetry_constraints.append(str(constraint))
    edge_vars = [
        z3.Bool(f"edge_{partition}_{agent}_{bundle}")
        for partition in range(91)
        for agent in range(4)
        for bundle in range(4)
    ]
    leaves = []

    def recurse(remaining, path):
        if remaining == 0:
            branch_index = len(leaves)
            branch_path = output_dir / f"branch_{branch_index:03d}.smt2"
            branch_path.write_text(solver.to_smt2())
            leaves.append(
                {
                    "branch": branch_index,
                    "path": str(branch_path),
                    "sha256": sha256(branch_path),
                    "cube": [str(literal) for literal in path],
                }
            )
            return
        cubes = list(solver.cube(edge_vars))
        if not cubes:
            raise RuntimeError("cube generation returned no branches")
        if len(cubes) == 1 and not cubes[0]:
            recurse(0, path)
            return
        for cube in cubes:
            solver.push()
            solver.add(*cube)
            recurse(remaining - 1, path + tuple(cube))
            solver.pop()

    recurse(depth, ())
    return {
        "schema": SCHEMA,
        "status": "EXACT_CUBE_COVER",
        "meaning": (
            "The disjunction of the listed branch cubes covers the source "
            "formula. SAT of any branch is SAT of the source; UNSAT of every "
            "branch is UNSAT of the source."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "depth": depth,
        "branch_count": len(leaves),
        "cube_timeout_seconds": timeout_seconds,
        "base_good_symmetry": base_good_symmetry,
        "base_good_symmetry_meaning": (
            "Orders agent 0's values within base bundles {6,7}, {1,2,3}, "
            "and {0,4}. Their S2 x S3 x S2 relabeling action preserves the "
            "fixed base, radius-one Hall candidates, and owner-distance rival "
            "family, so this is satisfiability preserving."
            if base_good_symmetry
            else None
        ),
        "base_good_stabilizer_order": 24 if base_good_symmetry else None,
        "symmetry_constraints": symmetry_constraints,
        "branches": leaves,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--base-good-symmetry", action="store_true")
    args = parser.parse_args()
    result = split(
        args.source,
        args.output_dir,
        args.depth,
        args.timeout_seconds,
        args.base_good_symmetry,
    )
    atomic_json(args.manifest, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
