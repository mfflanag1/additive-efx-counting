#!/usr/bin/env python3
"""Bounded CP-SAT CEGAR for the conditional two-core/Tutte target."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .decide_distinct_half_two_core_cpsat import add_two_core_obstructions
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_two_core_cegar import two_core_witnesses
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from decide_distinct_half_two_core_cpsat import add_two_core_obstructions
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_two_core_cegar import two_core_witnesses
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-two-core-cpsat-cegar-v1"
N = 4
M = 9


def run(
    output,
    proto_output,
    seed_paths,
    seed_mode,
    cap,
    time_limit,
    max_iterations,
    add_per_iteration,
    workers,
    random_seed,
    resume_path,
    two_core_scope,
):
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{observer}_{good}")
            for good in range(M)
        )
        for observer in range(N)
    )
    add_branch(model, values)
    two_core_candidate_count = add_two_core_obstructions(
        model, values, cap, two_core_scope
    )

    # Valid residual symmetries: simultaneously permute agents/representatives,
    # then permute the four nonrepresentative residual goods.
    for observer in range(N - 1):
        model.Add(values[observer][0] >= values[observer + 1][0])
    for good in range(5, M - 1):
        model.Add(values[0][good] >= values[0][good + 1])

    universe = tuple(favorite_pair_balanced_universe())
    universe_position = {partition: position for position, partition in enumerate(universe)}
    seed_supported = set()
    seed_sources = []
    for path in seed_paths:
        seed_supported.update(supported_partitions(load_values(path), list(universe)))
        seed_sources.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    seeded = (
        seed_supported
        if seed_mode == "union"
        else set(universe).difference(seed_supported)
    )
    pool = set()
    for partition in universe:
        if partition in seeded:
            add_favorite_pair_obstruction(
                model, values, partition, universe_position[partition]
            )
            pool.add(partition)

    trace = []
    resume_source = None
    resume_source_sha256 = None
    if resume_path is not None:
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("schema") != SCHEMA
            or resumed.get("cap") != cap
            or resumed.get("seed_mode") != seed_mode
            or resumed.get("add_per_iteration") != add_per_iteration
            or resumed.get("two_core_scope", "all") != two_core_scope
        ):
            raise ValueError("resume record is incompatible")
        for record in resumed["trace"]:
            decoded = tuple(tuple(row) for row in record["values"])
            audit_branch(decoded)
            if two_core_witnesses(decoded, two_core_scope):
                raise AssertionError("resumed model has a two-core witness")
            survivors = tuple(
                partition
                for partition in supported_partitions(decoded, list(universe))
                if partition not in pool
            )
            if (
                record["pool_size_before"] != len(pool)
                or record["favorite_pair_efx_survivors"] != len(survivors)
            ):
                raise AssertionError("resume trace replay changed")
            trace.append(record)
            for partition in survivors[:add_per_iteration]:
                add_favorite_pair_obstruction(
                    model, values, partition, universe_position[partition]
                )
                pool.add(partition)
        resume_source = str(resume_path)
        resume_source_sha256 = hashlib.sha256(resume_path.read_bytes()).hexdigest()

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status_code = cp_model.UNKNOWN
    status = "ITERATION_LIMIT"
    result_values = None
    started = time.time()
    iteration = len(trace)
    for iteration in range(len(trace) + 1, max_iterations + 1):
        status_code = solver.Solve(model)
        if status_code == cp_model.INFEASIBLE:
            status = "FINITE_CAP_UNSAT_CANDIDATE"
            break
        if status_code not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            status = "CP_SAT_UNKNOWN"
            break
        decoded = tuple(
            tuple(solver.Value(values[observer][good]) for good in range(M))
            for observer in range(N)
        )
        audit_branch(decoded)
        if two_core_witnesses(decoded, two_core_scope):
            raise AssertionError("decoded model violates no-two-core encoding")
        survivors = tuple(
            partition
            for partition in supported_partitions(decoded, list(universe))
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "favorite_pair_efx_survivors": len(survivors),
                "values": [list(row) for row in decoded],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "TWO_CORE_SELECTION_COUNTEREXAMPLE"
            result_values = decoded
            break
        for partition in survivors[:add_per_iteration]:
            add_favorite_pair_obstruction(
                model, values, partition, universe_position[partition]
            )
            pool.add(partition)

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "symmetry_breaking": [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ],
        "favorite_pair_partition_count": len(universe),
        "two_core_candidate_count": two_core_candidate_count,
        "two_core_scope": two_core_scope,
        "seed_mode": seed_mode,
        "seed_sources": seed_sources,
        "seed_supported_union_size": len(seed_supported),
        "pool_size": len(pool),
        "iterations": iteration,
        "add_per_iteration": add_per_iteration,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": time.time() - started,
        "workers": workers,
        "random_seed": random_seed,
        "resume_source": resume_source,
        "resume_source_sha256": resume_source_sha256,
        "trace": trace,
        "values": [list(row) for row in result_values] if result_values else None,
        "literal_complete_efx_count": (
            independent.count_complete_efx0(result_values)
            if result_values is not None
            else None
        ),
        "proto_path": str(proto_output),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "warning": (
            "UNSAT is finite-cap only and needs independent replay. A SAT "
            "terminal model refutes only the conditional two-core target "
            "unless literal complete-EFX enumeration is also zero."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--seed-mode", choices=("union", "complement"), default="complement")
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--add", type=int, default=64)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--two-core-scope", choices=("all", "canonical"), default="all"
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.max_iterations < 1
        or args.add < 1
        or args.workers < 1
    ):
        parser.error("invalid bounded CEGAR parameters")
    result = run(
        args.output,
        args.proto,
        tuple(args.seed),
        args.seed_mode,
        args.cap,
        args.time_limit,
        args.max_iterations,
        args.add,
        args.workers,
        args.random_seed,
        args.resume,
        args.two_core_scope,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
