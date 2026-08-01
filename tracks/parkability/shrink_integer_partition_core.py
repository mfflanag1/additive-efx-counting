#!/usr/bin/env python3
"""Deletion-shrink a bounded CP-SAT partition core."""

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
    from .integer_partition_master import IntegerPartitionMaster
    from .run_generic_partition_cegar import load_pool, pool_document
except ImportError:
    from anneal import atomic_json
    from integer_partition_master import IntegerPartitionMaster
    from run_generic_partition_cegar import load_pool, pool_document


SCHEMA = "integer-partition-cp-sat-minimal-core-v1"


def run(
    *,
    n: int,
    m: int,
    upper: int,
    pool_path: Path,
    core_pool_path: Path,
    result_path: Path,
    proto_path: Path,
    time_limit_s: float,
    workers: int,
    random_seed: int,
    exclude_universal_min: bool,
    exclude_peelable: bool,
    require_pairwise_distinct_rows: bool,
    require_distinct_item_values: bool,
    obstruction_encoding: str,
    favorite_pattern: tuple[int, ...] | None,
    favorite_pattern_stabilizer: bool,
) -> dict:
    if (
        time_limit_s <= 0
        or workers < 1
        or result_path.exists()
        or core_pool_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("invalid timeout, workers, or existing output path")
    pool = load_pool(pool_path, n, m)
    if not pool:
        raise ValueError("core shrinking requires a nonempty partition pool")
    master = IntegerPartitionMaster(
        n,
        m,
        upper,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_distinct_item_values=require_distinct_item_values,
    )
    if favorite_pattern is not None:
        master.add_strict_favorite_pattern(favorite_pattern)
        if favorite_pattern_stabilizer:
            master.add_favorite_pattern_stabilizer(favorite_pattern)

    selectors = []
    selector_by_literal = {}
    for index, partition in enumerate(pool):
        selector = master.model.NewBoolVar(f"activate_partition_{index}")
        selectors.append(selector)
        selector_by_literal[selector.Index()] = index
        master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
            activation=selector,
        )

    def solve(indices: list[int]) -> tuple[cp_model.CpSolver, int, list[int]]:
        master.model.ClearAssumptions()
        master.model.AddAssumptions([selectors[index] for index in indices])
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_s
        solver.parameters.num_search_workers = workers
        solver.parameters.random_seed = random_seed
        solver.parameters.core_minimization_level = 2
        solver.parameters.find_multiple_cores = True
        status = solver.Solve(master.model)
        reduced = []
        if status == cp_model.INFEASIBLE:
            literals = solver.SufficientAssumptionsForInfeasibility()
            if any(literal not in selector_by_literal for literal in literals):
                raise AssertionError("solver returned an unknown core assumption")
            reduced = sorted(selector_by_literal[literal] for literal in literals)
            if not reduced or not set(reduced).issubset(indices):
                raise AssertionError("solver returned an invalid assumption core")
        return solver, status, reduced

    started = time.time()
    initial_solver, initial_status, current = solve(list(range(len(pool))))
    if initial_status != cp_model.INFEASIBLE:
        raise RuntimeError(
            f"source core did not replay as infeasible: "
            f"{initial_solver.StatusName(initial_status)}"
        )
    trace = [{
        "step": "initial_core",
        "source_size": len(pool),
        "core_size": len(current),
        "wall_time_seconds": initial_solver.WallTime(),
        "conflicts": initial_solver.NumConflicts(),
        "branches": initial_solver.NumBranches(),
    }]
    essential = []
    unknown = []
    for candidate in list(current):
        if candidate not in current:
            continue
        trial = [index for index in current if index != candidate]
        solver, status, reduced = solve(trial)
        record = {
            "step": "delete",
            "candidate_index": candidate,
            "size_before": len(current),
            "solver_status": solver.StatusName(status),
            "wall_time_seconds": solver.WallTime(),
            "conflicts": solver.NumConflicts(),
            "branches": solver.NumBranches(),
        }
        if status == cp_model.INFEASIBLE:
            current = reduced
            record["outcome"] = "deleted"
            record["size_after"] = len(current)
        elif status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            essential.append(candidate)
            record["outcome"] = "essential"
            record["size_after"] = len(current)
        else:
            unknown.append(candidate)
            record["outcome"] = "unknown_kept"
            record["size_after"] = len(current)
        trace.append(record)
        print(
            f"candidate={candidate} outcome={record['outcome']} "
            f"core={len(current)} seconds={solver.WallTime():.3f}",
            flush=True,
        )

    final_solver, final_status, final_core = solve(current)
    if final_status != cp_model.INFEASIBLE:
        raise AssertionError("final shrunken core failed infeasibility replay")
    current = final_core
    master.model.ClearAssumptions()
    master.model.AddAssumptions([selectors[index] for index in current])
    atomic_json(
        core_pool_path,
        pool_document(n, m, [pool[index] for index in current]),
    )
    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT minimal-core model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "DELETION_MINIMAL_UNSAT_CORE"
            if not unknown
            else "SHRUNK_UNSAT_CORE_WITH_UNKNOWNS"
        ),
        "n": n,
        "m": m,
        "upper": upper,
        "source_pool_path": str(pool_path.resolve()),
        "source_pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "source_pool_size": len(pool),
        "core_pool_path": str(core_pool_path.resolve()),
        "core_pool_sha256": hashlib.sha256(
            core_pool_path.read_bytes()
        ).hexdigest(),
        "core_size": len(current),
        "core_indices": current,
        "essential_indices": sorted(set(essential) & set(current)),
        "unknown_indices": sorted(set(unknown) & set(current)),
        "proto_path": str(proto_path.resolve()),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "exclude_universal_min": exclude_universal_min,
        "exclude_peelable": exclude_peelable,
        "require_pairwise_distinct_rows": require_pairwise_distinct_rows,
        "require_distinct_item_values": require_distinct_item_values,
        "obstruction_encoding": obstruction_encoding,
        "favorite_pattern": (
            list(favorite_pattern) if favorite_pattern is not None else None
        ),
        "favorite_pattern_stabilizer": favorite_pattern_stabilizer,
        "comparison_variables": master.comparison_variable_count,
        "matching_clauses": master.matching_clauses,
        "hall_selectors": master.hall_selectors,
        "hall_edge_clauses": master.hall_edge_clauses,
        "final_solver_status": final_solver.StatusName(final_status),
        "final_wall_time_seconds": final_solver.WallTime(),
        "trace": trace,
        "elapsed_seconds": round(time.time() - started, 6),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--m", type=int, required=True)
    parser.add_argument("--upper", type=int, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--core-pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--exclude-universal-min", action="store_true")
    parser.add_argument("--exclude-peelable", action="store_true")
    parser.add_argument("--require-pairwise-distinct-rows", action="store_true")
    parser.add_argument("--require-distinct-item-values", action="store_true")
    parser.add_argument(
        "--obstruction-encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--favorite-pattern")
    parser.add_argument("--favorite-pattern-stabilizer", action="store_true")
    args = parser.parse_args()
    favorite_pattern = (
        tuple(map(int, args.favorite_pattern.split(",")))
        if args.favorite_pattern
        else None
    )
    run(
        n=args.n,
        m=args.m,
        upper=args.upper,
        pool_path=args.pool,
        core_pool_path=args.core_pool,
        result_path=args.result,
        proto_path=args.proto,
        time_limit_s=args.time_limit,
        workers=args.workers,
        random_seed=args.random_seed,
        exclude_universal_min=args.exclude_universal_min,
        exclude_peelable=args.exclude_peelable,
        require_pairwise_distinct_rows=args.require_pairwise_distinct_rows,
        require_distinct_item_values=args.require_distinct_item_values,
        obstruction_encoding=args.obstruction_encoding,
        favorite_pattern=favorite_pattern,
        favorite_pattern_stabilizer=args.favorite_pattern_stabilizer,
    )


if __name__ == "__main__":
    main()
