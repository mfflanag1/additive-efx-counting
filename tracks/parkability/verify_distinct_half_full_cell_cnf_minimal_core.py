#!/usr/bin/env python3
"""Verify a deletion-minimal threshold-CNF partition core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.solvers import Solver

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .run_distinct_half_full_cell_cegar import full_hall_cells
    from .run_generic_partition_cegar import supported_partitions
    from .terminal_cnf import decode_values
    from .terminal_distinct_half_full_cell_cnf import build
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from run_distinct_half_full_cell_cegar import full_hall_cells
    from run_generic_partition_cegar import supported_partitions
    from terminal_cnf import decode_values
    from terminal_distinct_half_full_cell_cnf import build


SCHEMA = "distinct-half-full-cell-threshold-cnf-minimal-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_partitions(payload):
    return tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in payload["core_partitions"]
    )


def run(parent_path: Path, candidate_path: Path, output: Path, cap: int):
    parent = json.loads(parent_path.read_text())
    candidate = json.loads(candidate_path.read_text())
    parent_partitions = set(decode_partitions(parent))
    candidate_partitions = decode_partitions(candidate)
    if (
        parent.get("cap") != cap
        or candidate.get("cap") != cap
        or len(candidate_partitions) != len(set(candidate_partitions))
        or not set(candidate_partitions) <= parent_partitions
    ):
        raise ValueError("candidate is not a valid subset of the parent core")

    source = {
        "core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in candidate_partitions
        ]
    }
    encoder, partitions, full_cell_encoding = build(
        source, cap, partition_assumptions=True
    )
    guards = encoder.partition_guards
    removal_boundaries = []
    with Solver(name="cadical195", bootstrap_with=encoder.cnf.clauses) as solver:
        if solver.solve(assumptions=guards):
            raise AssertionError("candidate core is satisfiable")
        for removed_position, removed_guard in enumerate(guards):
            assumptions = [
                guard for guard in guards if guard != removed_guard
            ]
            if not solver.solve(assumptions=assumptions):
                raise AssertionError(
                    f"partition {removed_position} is not deletion-essential"
                )
            values = tuple(
                tuple(row)
                for row in decode_values(solver.get_model(), encoder.value_bits)
            )
            audit_branch(values)
            if full_hall_cells(values):
                raise AssertionError("deletion boundary has a full Hall cell")
            repairs = set(
                supported_partitions(values, list(candidate_partitions))
            )
            if candidate_partitions[removed_position] not in repairs or any(
                partition in repairs
                for position, partition in enumerate(candidate_partitions)
                if position != removed_position
            ):
                raise AssertionError("deletion boundary repair set changed")
            removal_boundaries.append(
                {
                    "removed_position": removed_position,
                    "removed_partition": [
                        list(bundle)
                        for bundle in candidate_partitions[removed_position]
                    ],
                    "values": [list(row) for row in values],
                }
            )

    result = {
        "schema": SCHEMA,
        "status": "DELETION_MINIMAL_UNSAT_CORE_VERIFIED",
        "solver": "CaDiCaL",
        "cap": cap,
        "parent": str(parent_path),
        "parent_sha256": sha256(parent_path),
        "parent_core_size": len(parent_partitions),
        "core_size": len(partitions),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in partitions
        ],
        "removal_boundaries": removal_boundaries,
        "variables": encoder.cnf.nv,
        "clauses": len(encoder.cnf.clauses),
        "full_cell_encoding": full_cell_encoding,
        "interpretation": (
            "All core partitions together are UNSAT. Removing any one "
            f"produces an exact branch-valid cap-{cap} profile with no full Hall "
            "cell, and the removed partition is its unique repair inside "
            "the core."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    args = parser.parse_args()
    result = run(args.parent, args.candidate, args.output, args.cap)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
