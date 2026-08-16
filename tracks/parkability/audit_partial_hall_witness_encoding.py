#!/usr/bin/env python3
"""Audit the four-by-four Hall-witness obstruction encoding."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .partial_hall_factored_master import minimal_hall_witnesses
except ImportError:
    from anneal import atomic_json
    from partial_hall_factored_master import minimal_hall_witnesses


def run(output: Path, smt2: Path) -> dict:
    edges = tuple(
        tuple(z3.Bool(f"edge_{agent}_{bundle}") for bundle in range(4))
        for agent in range(4)
    )
    matching_obstruction = z3.And(
        *(
            z3.Or(
                *(z3.Not(edges[agent][matching[agent]]) for agent in range(4))
            )
            for matching in itertools.permutations(range(4))
        )
    )
    witnesses = minimal_hall_witnesses(edges)
    hall_obstruction = z3.Or(*witnesses)
    solver = z3.Solver()
    solver.add(matching_obstruction != hall_obstruction)
    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-witness-encoding-audit-v1",
        "status": "EXACT_EQUIVALENCE" if verdict == z3.unsat else str(verdict).upper(),
        "meaning": (
            "UNSAT proves that failure of all 24 perfect matchings in an "
            "arbitrary 4-by-4 graph is equivalent to one of the minimal "
            "Hall deficient-set witnesses."
        ),
        "matching_count": 24,
        "hall_witness_count": len(witnesses),
        "solver_verdict": str(verdict),
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.smt2), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
