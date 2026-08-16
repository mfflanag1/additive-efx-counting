#!/usr/bin/env python3
"""Sparse CEGAR for the rank-one triple conversion dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        N,
        build_master,
        resident_graph,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        N,
        build_master,
        resident_graph,
    )


SCHEMA = "common-favorite-rank1-triple-conversion-cegar-v1"


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def run(
    result_path,
    formula_path,
    time_limit,
    max_iterations,
    add_per_iteration,
    conversion_scope,
    seed_paths,
):
    if (
        time_limit <= 0
        or max_iterations < 1
        or add_per_iteration < 1
        or result_path.exists()
        or formula_path.exists()
    ):
        raise ValueError("valid bounds and new output paths are required")
    master, conversions, singleton_partitions = build_master(
        "matching_clauses",
        add_all_singletons=False,
        conversion_scope=conversion_scope,
    )
    learned = set()
    seed_imports = []
    for seed_path in seed_paths:
        raw = json.loads(seed_path.read_text())
        candidates = []
        if raw.get("values") is not None:
            candidates.append(raw["values"])
        candidates.extend(
            record["values"]
            for record in raw.get("trace", [])
            if record.get("values") is not None
        )
        imported = 0
        for candidate in candidates:
            values = tuple(tuple(row) for row in candidate)
            if (
                matching_rank(resident_graph(values)) != 1
                or any(
                    matching_rank(feasible_graph(values, partition)) == N
                    for partition in conversions
                )
            ):
                raise AssertionError("seed left the requested decision cell")
            for partition in singleton_partitions:
                key = canonical(partition)
                if (
                    key not in learned
                    and matching_rank(feasible_graph(values, partition)) == N
                ):
                    master.add_partition_obstruction(partition)
                    learned.add(key)
                    imported += 1
        seed_imports.append({
            "source": str(seed_path),
            "source_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
            "model_count": len(candidates),
            "new_singleton_count": imported,
        })
    trace = []
    candidate = None
    solved = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
        if solved.status != "SAT":
            break
        values = solved.values
        assert values is not None
        if matching_rank(resident_graph(values)) != 1:
            raise AssertionError("CEGAR model left the rank-one premise")
        if any(
            matching_rank(feasible_graph(values, partition)) == N
            for partition in conversions
        ):
            raise AssertionError("CEGAR model gained a local conversion")
        survivors = [
            partition
            for partition in singleton_partitions
            if canonical(partition) not in learned
            and matching_rank(feasible_graph(values, partition)) == N
        ]
        trace.append({
            "iteration": iteration,
            "learned_singleton_count_before": len(learned),
            "supported_unlearned_singleton_count": len(survivors),
            "solver_status": solved.raw_status,
            "values": [list(row) for row in values],
        })
        if not survivors:
            candidate = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            learned.add(canonical(partition))
    if solved is None:
        raise AssertionError("CEGAR performed no solve")

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    status = (
        "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
        if candidate is not None
        else "RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "MASTER_UNKNOWN"
        if solved.status != "SAT"
        else "ITERATION_LIMIT"
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "n": 4,
        "m": 9,
        "domain": "strictly positive reals normalized per row",
        "obstruction_encoding": "matching_clauses",
        "conversion_scope": conversion_scope,
        "iterations": len(trace),
        "trace": trace,
        "seed_imports": seed_imports,
        "learned_singleton_count": len(learned),
        "values": [list(row) for row in candidate] if candidate else None,
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds_per_iteration": time_limit,
        "max_iterations": max_iterations,
        "add_per_iteration": add_per_iteration,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "formula_bytes": len(formula.encode()),
        "claim_boundary": (
            "A counterexample refutes only the local conversion-or-singleton "
            "dichotomy. UNSAT requires independent replay. UNKNOWN and an "
            "iteration limit decide neither direction."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--max-iterations", type=int, default=2)
    parser.add_argument("--add-per-iteration", type=int, default=256)
    parser.add_argument(
        "--conversion-scope",
        choices=("first", "all"),
        default="all",
    )
    parser.add_argument("--seed", type=Path, action="append", default=[])
    args = parser.parse_args()
    run(
        args.result,
        args.formula,
        args.time_limit,
        args.max_iterations,
        args.add_per_iteration,
        args.conversion_scope,
        args.seed,
    )


if __name__ == "__main__":
    main()
