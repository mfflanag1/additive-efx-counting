#!/usr/bin/env python3
"""Split an exported minimum-slot QF_LRA master into an exact cube cover."""

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


SCHEMA = "minimum-slot-literal-cube-cover-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, output_dir, manifest, depth, timeout_seconds):
    if not source.is_file() or manifest.exists() or output_dir.exists():
        raise ValueError("an existing source and new output paths are required")
    output_dir.mkdir(parents=True)
    solver = z3.SolverFor("QF_LRA")
    solver.set(timeout=timeout_seconds * 1000)
    solver.from_file(str(source))
    valuation_vars = [
        z3.Real(f"v_{agent}_{good}")
        for agent in range(4)
        for good in range(9)
    ]
    leaves = []

    def persist(path, cube_status_hint=None):
        index = len(leaves)
        branch_path = output_dir / f"branch_{index:03d}.smt2"
        branch_path.write_text(solver.to_smt2())
        leaves.append(
            {
                "branch": index,
                "path": str(branch_path),
                "sha256": sha256(branch_path),
                "cube": [str(literal) for literal in path],
                "cube_status_hint": cube_status_hint,
            }
        )

    def recurse(remaining, path):
        if remaining == 0:
            persist(path)
            return
        cubes = list(solver.cube(valuation_vars))
        if not cubes:
            verdict = solver.check()
            persist(
                path,
                str(verdict) if verdict != z3.unknown else solver.reason_unknown(),
            )
            return
        if len(cubes) == 1 and not cubes[0]:
            persist(path, "terminal")
            return
        for cube in cubes:
            solver.push()
            solver.add(*cube)
            recurse(remaining - 1, path + tuple(cube))
            solver.pop()

    recurse(depth, ())
    result = {
        "schema": SCHEMA,
        "status": "EXACT_CUBE_COVER",
        "meaning": (
            "Z3 cube literals form an exact disjunctive cover of the source. "
            "SAT of any branch is SAT of the source; UNSAT of every branch is "
            "UNSAT of the source."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "depth": depth,
        "branch_count": len(leaves),
        "cube_timeout_seconds": timeout_seconds,
        "branches": leaves,
    }
    atomic_json(manifest, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()
    result = run(
        args.source,
        args.output_dir,
        args.manifest,
        args.depth,
        args.timeout_seconds,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
