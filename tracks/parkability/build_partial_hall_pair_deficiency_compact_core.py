#!/usr/bin/env python3
"""Build a compact standalone replay of a pair-deficiency core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import candidate_partitions, eligible_constraints
    from .partial_hall_factored_master import (
        adjacency_constraints,
        hall_witnesses_by_size,
    )
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import candidate_partitions, eligible_constraints
    from partial_hall_factored_master import (
        adjacency_constraints,
        hall_witnesses_by_size,
    )


def run(source: Path, output: Path, smt2: Path) -> dict:
    document = json.loads(source.read_text())
    records = document["bounded_deletion_unsat_core"]
    n, m = 4, 9
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    floater = 8
    values = [[z3.Real(f"v_{agent}_{good}") for good in range(m)] for agent in range(n)]
    base_constraints = eligible_constraints(values, base, floater)
    partitions = list(candidate_partitions(base, floater))
    solver = z3.Solver()
    selected_partitions = {}

    for record in records:
        kind = record["kind"]
        if kind == "row_nonnegativity":
            solver.add(*(entry >= 0 for entry in values[record["agent"]]))
        elif kind == "row_normalization":
            solver.add(z3.Sum(*values[record["agent"]]) == 1)
        elif kind == "base_eligibility":
            solver.add(base_constraints[record["constraint_index"]])
        elif kind in {"hall_failure", "no_pair_deficiency"}:
            selected_partitions.setdefault(record["partition_index"], set()).add(kind)
        else:
            raise ValueError(f"unsupported core record: {kind}")

    for partition_index, kinds in selected_partitions.items():
        move = partitions[partition_index]
        edges = []
        for agent in range(n):
            row = []
            for bundle in range(n):
                edge = z3.Bool(f"edge_{partition_index}_{agent}_{bundle}")
                solver.add(
                    edge
                    == z3.And(
                        *adjacency_constraints(values[agent], move["partition"], bundle)
                    )
                )
                row.append(edge)
            edges.append(tuple(row))
        groups = hall_witnesses_by_size(tuple(edges))
        if "hall_failure" in kinds:
            solver.add(z3.Or(*(item for group in groups[1:] for item in group)))
        if "no_pair_deficiency" in kinds:
            solver.add(z3.Not(z3.Or(*groups[1])))

    verdict = solver.check()
    if verdict != z3.unsat:
        raise RuntimeError(f"compact core did not replay UNSAT: {verdict}")
    smt2.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-pair-deficiency-compact-core-v1",
        "status": "UNSAT",
        "meaning": (
            "Compact exact replay of the bounded pair-deficiency core, with "
            "only the selected base inequalities and candidate partitions."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "core_record_count": len(records),
        "selected_partition_count": len(selected_partitions),
        "selected_partition_indices": sorted(selected_partitions),
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
        "solver_verdict": str(verdict),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output, args.smt2), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
