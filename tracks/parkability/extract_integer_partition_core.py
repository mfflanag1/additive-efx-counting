#!/usr/bin/env python3
"""Extract a CP-SAT assumption core from a bounded partition cell."""

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


SCHEMA = "integer-partition-cp-sat-core-v1"


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
        raise ValueError("core extraction requires a nonempty partition pool")
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
    selector_by_index = {}
    for index, partition in enumerate(pool):
        selector = master.model.NewBoolVar(f"activate_partition_{index}")
        selectors.append(selector)
        selector_by_index[selector.Index()] = index
        master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
            activation=selector,
        )
    master.model.AddAssumptions(selectors)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    solver.parameters.core_minimization_level = 2
    solver.parameters.find_multiple_cores = True
    started = time.time()
    status_code = solver.Solve(master.model)
    raw_status = solver.StatusName(status_code)
    core_indices = []
    if status_code == cp_model.INFEASIBLE:
        core_literals = solver.SufficientAssumptionsForInfeasibility()
        if any(literal not in selector_by_index for literal in core_literals):
            raise AssertionError("solver core contains an unknown or negated assumption")
        core_indices = sorted(selector_by_index[literal] for literal in core_literals)
        if not core_indices:
            raise AssertionError("infeasible assumed model returned an empty core")
        atomic_json(
            core_pool_path,
            pool_document(n, m, [pool[index] for index in core_indices]),
        )
        master.model.ClearAssumptions()
        master.model.AddAssumptions([selectors[index] for index in core_indices])
    else:
        atomic_json(core_pool_path, pool_document(n, m, []))

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT core model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_CORE_EXTRACTED"
            if status_code == cp_model.INFEASIBLE
            else "CORE_UNKNOWN"
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
        "core_size": len(core_indices),
        "core_indices": core_indices,
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
        "solver_status": raw_status,
        "wall_time_seconds": solver.WallTime(),
        "deterministic_time": solver.ResponseProto().deterministic_time,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
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
    parser.add_argument("--time-limit", type=float, default=600)
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
