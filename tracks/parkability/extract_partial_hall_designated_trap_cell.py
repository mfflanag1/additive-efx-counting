#!/usr/bin/env python3
"""Extract one exact designated pair-trap cell from a factored Hall master."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_designated_pair_trap import designated_bundle
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_designated_pair_trap import designated_bundle
    from decide_partial_hall_radius_one import candidate_partitions


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source: Path, output: Path, artifact_output: Path, partition_index: int, pair):
    if tuple(pair) not in itertools.combinations(range(4), 2):
        raise ValueError("pair must contain two increasing distinct agents")
    solver = z3.Solver()
    solver.from_file(str(source))
    moves = list(
        candidate_partitions(((6, 7), (1, 2, 3), (0, 4), (5,)), 8)
    )
    move = moves[partition_index]
    designated = designated_bundle(move)
    solver.add(
        *(
            z3.Bool(f"edge_{partition_index}_{agent}_{designated}")
            for agent in pair
        ),
        *(
            z3.Not(z3.Bool(f"edge_{partition_index}_{agent}_{bundle}"))
            for agent in pair
            for bundle in range(4)
            if bundle != designated
        ),
    )
    output.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-designated-trap-cell-v1",
        "status": "EXACT_CELL",
        "meaning": (
            "Exact factored Hall master restricted to the stated designated "
            "pair trap. A solver SAT or UNSAT verdict on the SMT-LIB output is "
            "respectively a countermodel or an exclusion for this cell only."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "partition_index": partition_index,
        "deficient_agents": list(pair),
        "designated_bundle": designated,
        "output": str(output),
        "output_sha256": sha256(output),
    }
    atomic_json(artifact_output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifact-output", type=Path, required=True)
    parser.add_argument("--partition-index", type=int, required=True)
    parser.add_argument("--pair", type=int, nargs=2, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.source,
                args.output,
                args.artifact_output,
                args.partition_index,
                tuple(args.pair),
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
