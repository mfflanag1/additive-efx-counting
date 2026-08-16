#!/usr/bin/env python3
"""Extract a singleton-obstruction core for a repeated-resident bridge cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import ortools
from ortools.sat.python import cp_model

try:
    from .anneal import atomic_json
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
    )
    from .decide_common_favorite_rank1_triple_conversion_cpsat import (
        add_cell_symmetry,
        add_rank_one_premise,
    )
    from .integer_partition_master import IntegerPartitionMaster
    from .optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        repair_partitions,
    )
except ImportError:
    from anneal import atomic_json
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
    )
    from decide_common_favorite_rank1_triple_conversion_cpsat import (
        add_cell_symmetry,
        add_rank_one_premise,
    )
    from integer_partition_master import IntegerPartitionMaster
    from optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        repair_partitions,
    )


SCHEMA = "common-favorite-rank1-extended-bridge-collision-core-v1"
SOURCE_SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_partition(raw_partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in raw_partition))


def make_solver(time_limit, workers, random_seed):
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    solver.parameters.core_minimization_level = 2
    solver.parameters.find_multiple_cores = True
    return solver


def run(
    source_path,
    upper,
    resident_equality_pair,
    obstruction_encoding,
    time_limit,
    workers,
    random_seed,
    output_path,
    proto_path,
):
    if (
        upper < 1
        or resident_equality_pair not in {"12", "23"}
        or obstruction_encoding
        not in {"duplicate_matching_clauses", "duplicate_hall_selectors"}
        or time_limit <= 0
        or workers < 1
        or output_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("valid bounds and new output paths are required")
    source = json.loads(source_path.read_text())
    if source.get("schema") == SOURCE_SCHEMA:
        source_valid = (
            source.get("status")
            == "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
            and source.get("solver_status") == "INFEASIBLE"
            and source.get("conversion_scope") == "radius2_extended_bridge"
        )
        pool_field = "singleton_obstruction_partitions"
    elif source.get("schema") == SCHEMA:
        source_valid = (
            source.get("status") == "SINGLETON_ASSUMPTION_CORE_EXTRACTED"
            and source.get("replay_solver_status") == "INFEASIBLE"
        )
        pool_field = "singleton_obstruction_core_partitions"
    else:
        source_valid = False
        pool_field = "singleton_obstruction_partitions"
    if (
        not source_valid
        or source.get("upper") != upper
        or source.get("resident_equality_pair") != resident_equality_pair
        or source.get("obstruction_encoding") != obstruction_encoding
    ):
        raise ValueError("source metadata does not match the requested core cell")
    singleton_pool = tuple(
        normalized_partition(partition)
        for partition in source[pool_field]
    )
    if not singleton_pool or len(set(singleton_pool)) != len(singleton_pool):
        raise ValueError("source singleton pool is empty or contains duplicates")

    master = IntegerPartitionMaster(N, M, upper)
    add_cell_symmetry(master)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    favorite = master.values[OWNER][FAVORITE]
    for bundle in RESIDUAL:
        for removed in bundle:
            master.model.Add(
                favorite
                >= sum(
                    master.values[OWNER][good]
                    for good in bundle
                    if good != removed
                )
            )
    add_rank_one_premise(master)
    first = int(resident_equality_pair[0])
    second = int(resident_equality_pair[1])
    for good in range(M):
        master.model.Add(master.values[first][good] == master.values[second][good])

    duplicate_observers = (first, second)
    for partition in repair_partitions("bridge45"):
        master.add_duplicate_row_partition_obstruction(
            partition,
            duplicate_observers,
            encoding=obstruction_encoding,
        )

    selectors = []
    selector_by_index = {}
    for partition_index, partition in enumerate(singleton_pool):
        selector = master.model.NewBoolVar(
            f"activate_singleton_partition_{partition_index}"
        )
        selectors.append(selector)
        selector_by_index[selector.Index()] = partition_index
        master.add_duplicate_row_partition_obstruction(
            partition,
            duplicate_observers,
            encoding=obstruction_encoding,
            activation=selector,
        )
    master.model.AddAssumptions(selectors)

    started = time.time()
    solver = make_solver(time_limit, workers, random_seed)
    status_code = solver.Solve(master.model)
    raw_status = solver.StatusName(status_code)
    core_indices = []
    if status_code == cp_model.INFEASIBLE:
        core_literals = solver.SufficientAssumptionsForInfeasibility()
        if any(literal not in selector_by_index for literal in core_literals):
            raise AssertionError("solver returned an unexpected assumption literal")
        core_indices = sorted(selector_by_index[literal] for literal in core_literals)
        if not core_indices:
            raise AssertionError("infeasible assumed model returned an empty core")

    master.model.ClearAssumptions()
    if core_indices:
        master.model.AddAssumptions([selectors[index] for index in core_indices])
        replay_solver = make_solver(time_limit, workers, random_seed + 1)
        replay_status_code = replay_solver.Solve(master.model)
        replay_status = replay_solver.StatusName(replay_status_code)
        if replay_status_code in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise AssertionError("solver returned an invalid singleton core")
    else:
        replay_solver = None
        replay_status = None

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT core model export failed")
    proto = proto_path.read_bytes()
    core_partitions = tuple(singleton_pool[index] for index in core_indices)
    result = {
        "schema": SCHEMA,
        "status": (
            "SINGLETON_ASSUMPTION_CORE_EXTRACTED"
            if core_indices and replay_status == "INFEASIBLE"
            else "SINGLETON_ASSUMPTION_CORE_REPLAY_UNKNOWN"
            if core_indices
            else "CORE_EXTRACTION_UNKNOWN"
        ),
        "n": N,
        "m": M,
        "upper": upper,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "source_singleton_field": pool_field,
        "resident_equality_pair": resident_equality_pair,
        "obstruction_encoding": obstruction_encoding,
        "repair_partition_count": 45,
        "source_singleton_obstruction_pool_size": len(singleton_pool),
        "singleton_obstruction_core_size": len(core_partitions),
        "singleton_obstruction_core_indices": core_indices,
        "singleton_obstruction_core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in core_partitions
        ],
        "solver_status": raw_status,
        "solver_wall_seconds": solver.WallTime(),
        "solver_conflicts": solver.NumConflicts(),
        "solver_branches": solver.NumBranches(),
        "replay_solver_status": replay_status,
        "replay_solver_wall_seconds": (
            replay_solver.WallTime() if replay_solver is not None else None
        ),
        "comparison_variables": len(master._comparison_variables),
        "matching_clauses": master.matching_clauses,
        "hall_selectors": master.hall_selectors,
        "hall_edge_clauses": master.hall_edge_clauses,
        "time_limit_seconds_per_solve": time_limit,
        "workers": workers,
        "random_seed": random_seed,
        "elapsed_seconds": time.time() - started,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "This is a sufficient singleton-obstruction core for one bounded "
            "repeated-resident cell. It need not be deletion-minimal and does "
            "not extend the theorem above the recorded cap."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--upper", type=int, required=True)
    parser.add_argument("--resident-equality-pair", choices=("12", "23"), required=True)
    parser.add_argument(
        "--obstruction-encoding",
        choices=("duplicate_matching_clauses", "duplicate_hall_selectors"),
        required=True,
    )
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.source,
        args.upper,
        args.resident_equality_pair,
        args.obstruction_encoding,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.output,
        args.proto,
    )


if __name__ == "__main__":
    main()
