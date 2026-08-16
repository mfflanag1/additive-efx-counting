#!/usr/bin/env python3
"""Split a four-agent Hall master by deficient-set size."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .partial_hall_factored_master import hall_witnesses_by_size
except ImportError:
    from anneal import atomic_json
    from partial_hall_factored_master import hall_witnesses_by_size


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source: Path, output_dir: Path, manifest: Path, partition: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    solver = z3.Solver()
    solver.from_file(str(source))
    edges = tuple(
        tuple(
            z3.Bool(f"edge_{partition}_{agent}_{bundle}")
            for bundle in range(4)
        )
        for agent in range(4)
    )
    groups = hall_witnesses_by_size(edges)
    type_formulas = tuple(z3.Or(*group) for group in groups)
    branches = []
    previous = []
    for index, formula in enumerate(type_formulas):
        solver.push()
        solver.add(*(z3.Not(item) for item in previous), formula)
        path = output_dir / f"deficiency_{index + 1}.smt2"
        path.write_text(solver.to_smt2())
        branches.append(
            {
                "deficient_agent_count": index + 1,
                "prior_type_exclusions": index,
                "hall_witness_count": len(groups[index]),
                "path": str(path),
                "sha256": sha256(path),
            }
        )
        solver.pop()
        previous.append(formula)
    artifact = {
        "schema": "partial-hall-deficiency-cover-v1",
        "status": "EXACT_DISJOINT_COVER",
        "meaning": (
            "The source asserts Hall failure for the selected partition. "
            "The four disjoint branches select the least deficient-agent-set "
            "size having a minimal Hall witness, so their disjunction is "
            "equivalent to the source."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "partition": partition,
        "branch_count": len(branches),
        "branches": branches,
    }
    atomic_json(manifest, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--partition", type=int, choices=range(91), default=0)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.source, args.output_dir, args.manifest, args.partition),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
