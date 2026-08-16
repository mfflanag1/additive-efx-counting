#!/usr/bin/env python3
"""Exact bounded-integer CEGAR over EFX-feasible bundle partitions."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import ortools

try:
    from . import core, independent
    from .anneal import atomic_json, has_universal_min
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .integer_partition_master import IntegerPartitionMaster, Partition
    from .run_generic_partition_cegar import load_pool, pool_document
except ImportError:
    import core
    import independent
    from anneal import atomic_json, has_universal_min
    from audit_matching_augmentation import feasible_graph, matching_rank
    from integer_partition_master import IntegerPartitionMaster, Partition
    from run_generic_partition_cegar import load_pool, pool_document


SCHEMA = "integer-partition-cp-sat-result-v1"


def supported_partitions(
    values: tuple[tuple[int, ...], ...],
    universe: list[Partition],
) -> list[Partition]:
    n = len(values)
    return [
        partition
        for partition in universe
        if matching_rank(feasible_graph(values, partition)) == n
    ]


def run(
    *,
    n: int,
    m: int,
    upper: int,
    pool_path: Path,
    result_path: Path,
    proto_path: Path,
    seed_pool_paths: list[Path] | None = None,
    add_per_iteration: int = 64,
    max_iterations: int = 10,
    time_limit_s: float = 600,
    workers: int = 1,
    random_seed: int = 1,
    symmetry: str = "none",
    exclude_universal_min: bool = False,
    exclude_peelable: bool = False,
    require_pairwise_distinct_rows: bool = False,
    require_distinct_item_values: bool = False,
    require_upper_used: bool = False,
    obstruction_encoding: str = "matching_clauses",
    favorite_pattern: tuple[int, ...] | None = None,
    favorite_pattern_stabilizer: bool = False,
    second_favorite_pattern: tuple[int, ...] | None = None,
    ranking_prefix_stabilizer: bool = False,
    half_favorite_representatives: tuple[int, ...] | None = None,
    half_favorite_representative_stabilizer: bool = False,
    require_singleton_threshold_failure_good: int | None = None,
    require_singleton_threshold_failure_envelope_good: int | None = None,
    partition_shape: tuple[int, ...] | None = None,
    partition_shapes: tuple[tuple[int, ...], ...] = (),
    partition_singleton_good: int | None = None,
    partition_singleton_goods: tuple[int, ...] = (),
) -> dict:
    if (
        type(add_per_iteration) is not int
        or add_per_iteration < 1
        or type(max_iterations) is not int
        or max_iterations < 1
        or time_limit_s <= 0
        or result_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("invalid batch, iteration, timeout, or output path")
    if second_favorite_pattern is not None:
        if (
            favorite_pattern is None
            or len(second_favorite_pattern) != n
            or any(
                type(good) is not int or not 0 <= good < m
                for good in second_favorite_pattern
            )
            or any(
                favorite == second
                for favorite, second in zip(
                    favorite_pattern,
                    second_favorite_pattern,
                )
            )
        ):
            raise ValueError("second favorites require valid distinct favorites")
        if favorite_pattern_stabilizer and any(
            favorite_pattern[left] == favorite_pattern[right]
            and second_favorite_pattern[left] != second_favorite_pattern[right]
            for left in range(n)
            for right in range(left + 1, n)
        ):
            raise ValueError(
                "favorite-pattern stabilizer is unsafe when equal-favorite "
                "agents have different second favorites"
            )
    elif ranking_prefix_stabilizer:
        raise ValueError("ranking stabilizer requires second favorites")
    if half_favorite_representatives is not None:
        if (
            favorite_pattern is None
            or len(half_favorite_representatives) != n
            or len(set(half_favorite_representatives)) != n
            or any(
                type(good) is not int or not 0 <= good < m
                for good in half_favorite_representatives
            )
            or any(
                favorite == representative
                for favorite, representative in zip(
                    favorite_pattern,
                    half_favorite_representatives,
                )
            )
        ):
            raise ValueError("half-favorite representatives must be distinct")
        if favorite_pattern_stabilizer:
            raise ValueError(
                "favorite-pattern stabilizer does not preserve fixed "
                "half-favorite representatives"
            )
    elif half_favorite_representative_stabilizer:
        raise ValueError(
            "representative stabilizer requires half-favorite representatives"
        )
    if (
        require_singleton_threshold_failure_good is not None
        and (
            type(require_singleton_threshold_failure_good) is not int
            or not 0 <= require_singleton_threshold_failure_good < m
        )
    ):
        raise ValueError("threshold-failure singleton good is invalid")
    if (
        require_singleton_threshold_failure_envelope_good is not None
        and (
            type(require_singleton_threshold_failure_envelope_good) is not int
            or not 0 <= require_singleton_threshold_failure_envelope_good < m
        )
    ):
        raise ValueError("threshold-envelope singleton good is invalid")
    if (
        require_singleton_threshold_failure_good is not None
        and require_singleton_threshold_failure_envelope_good is not None
    ):
        raise ValueError("select only one owner-threshold encoding")
    if (
        require_singleton_threshold_failure_envelope_good is not None
        and (
            n != 4
            or m != 9
            or favorite_pattern
            != (require_singleton_threshold_failure_envelope_good,) * n
        )
    ):
        raise ValueError(
            "the threshold envelope requires a 4x9 strict common-favorite cell"
        )
    if not isinstance(partition_shapes, tuple):
        raise ValueError("partition shapes must be a tuple")
    shape_set = set(partition_shapes)
    if partition_shape is not None:
        shape_set.add(partition_shape)
    if any(
        len(shape) != n
        or tuple(sorted(shape, reverse=True)) != shape
        or any(size < 1 for size in shape)
        or sum(shape) != m
        for shape in shape_set
    ):
        raise ValueError("partition shapes must be descending compositions of m")
    if partition_singleton_good is not None and (
        type(partition_singleton_good) is not int
        or not 0 <= partition_singleton_good < m
    ):
        raise ValueError("partition singleton good is outside the goods range")
    if (
        not isinstance(partition_singleton_goods, tuple)
        or any(
            type(good) is not int or not 0 <= good < m
            for good in partition_singleton_goods
        )
        or len(set(partition_singleton_goods)) != len(partition_singleton_goods)
    ):
        raise ValueError("partition singleton goods are invalid")
    singleton_goods = set(partition_singleton_goods)
    if partition_singleton_good is not None:
        singleton_goods.add(partition_singleton_good)
    universe = [
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(n, m)
        if (
            not shape_set
            and not singleton_goods
        )
        or (
            shape_set
            and tuple(sorted(map(len, partition), reverse=True)) in shape_set
        )
        or (
            singleton_goods
            and any((good,) in partition for good in singleton_goods)
        )
    ]
    pool = load_pool(pool_path, n, m)
    if any(partition not in universe for partition in pool):
        raise ValueError("existing pool contains a partition outside the target shape")
    pool_set = set(pool)
    seed_pool_paths = [] if seed_pool_paths is None else seed_pool_paths
    for seed_pool_path in seed_pool_paths:
        for partition in load_pool(seed_pool_path, n, m):
            if partition not in universe:
                continue
            if partition not in pool_set:
                pool.append(partition)
                pool_set.add(partition)
    atomic_json(pool_path, pool_document(n, m, pool))

    master = IntegerPartitionMaster(
        n,
        m,
        upper,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_distinct_item_values=require_distinct_item_values,
        require_upper_used=require_upper_used,
        symmetry=symmetry,
    )
    if favorite_pattern is not None:
        master.add_strict_favorite_pattern(favorite_pattern)
        if favorite_pattern_stabilizer:
            master.add_favorite_pattern_stabilizer(favorite_pattern)
    if second_favorite_pattern is not None:
        ranking_prefixes = tuple(
            zip(favorite_pattern, second_favorite_pattern)
        )
        master.add_strict_ranking_prefixes(ranking_prefixes)
        if ranking_prefix_stabilizer:
            master.add_ranking_prefix_stabilizer(ranking_prefixes)
    if half_favorite_representatives is not None:
        master.add_half_favorite_representatives(
            favorite_pattern,
            half_favorite_representatives,
        )
        if half_favorite_representative_stabilizer:
            master.add_half_favorite_representative_stabilizer(
                favorite_pattern,
                half_favorite_representatives,
            )
    residual_partition_count = 0
    if require_singleton_threshold_failure_good is not None:
        singleton_good = require_singleton_threshold_failure_good
        residual_goods = tuple(good for good in range(m) if good != singleton_good)
        residual_partitions = tuple(
            tuple(
                tuple(residual_goods[index] for index in bundle)
                for bundle in partition
            )
            for partition in core.iter_unlabeled_nonempty_partitions(n - 1, m - 1)
        )
        residual_partition_count = len(residual_partitions)
        for observer in range(n):
            for partition in residual_partitions:
                master.add_owner_threshold_obstruction(
                    observer,
                    singleton_good,
                    partition,
                )
    if require_singleton_threshold_failure_envelope_good is not None:
        singleton_good = require_singleton_threshold_failure_envelope_good
        for observer in range(n):
            master.add_owner_threshold_shape_envelope(
                observer,
                singleton_good,
            )
    for partition in pool:
        master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
        )

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    solver_status = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(
            time_limit_s=time_limit_s,
            workers=workers,
            random_seed=random_seed,
        )
        solver_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_BOUNDED_CELL_CANDIDATE"
            trace.append({
                "iteration": iteration,
                "pool_size": len(pool),
                "solver_status": solved.raw_status,
                "wall_time_seconds": solved.wall_time_seconds,
                "deterministic_time": solved.deterministic_time,
                "conflicts": solved.conflicts,
                "branches": solved.branches,
            })
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            trace.append({
                "iteration": iteration,
                "pool_size": len(pool),
                "solver_status": solved.raw_status,
                "wall_time_seconds": solved.wall_time_seconds,
                "deterministic_time": solved.deterministic_time,
                "conflicts": solved.conflicts,
                "branches": solved.branches,
            })
            break
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
            upper=upper,
        )
        if exclude_universal_min and has_universal_min(
            [list(row) for row in values]
        ):
            raise AssertionError("model violated the universal-minimum cut")
        if favorite_pattern is not None and any(
            any(
                values[observer][favorite] <= values[observer][other]
                for other in range(m)
                if other != favorite
            )
            for observer, favorite in enumerate(favorite_pattern)
        ):
            raise AssertionError("model violated the strict favorite pattern")
        if second_favorite_pattern is not None and any(
            any(
                values[observer][second] <= values[observer][other]
                for other in range(m)
                if other not in (favorite, second)
            )
            for observer, (favorite, second) in enumerate(
                zip(favorite_pattern, second_favorite_pattern)
            )
        ):
            raise AssertionError("model violated the strict second-favorite pattern")
        survivors = supported_partitions(values, universe)
        if any(partition in pool_set for partition in survivors):
            raise AssertionError("model satisfies a pooled partition")
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(pool),
            "supported_partition_count": len(survivors),
            "values": [list(row) for row in values],
            "solver_status": solved.raw_status,
            "wall_time_seconds": solved.wall_time_seconds,
            "deterministic_time": solved.deterministic_time,
            "conflicts": solved.conflicts,
            "branches": solved.branches,
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"supported_partitions={len(survivors)} "
            f"solver_seconds={solved.wall_time_seconds:.3f}",
            flush=True,
        )
        if not survivors:
            if not shape_set and not singleton_goods:
                literal_count = independent.count_complete_efx0(values)
                if literal_count:
                    raise AssertionError("independent verifier rejected zero EFX")
                status = "ZERO_COMPLETE_EFX"
            else:
                status = "ZERO_SUPPORTED_PARTITIONS"
            result_values = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(
                partition,
                encoding=obstruction_encoding,
            )
            pool.append(partition)
            pool_set.add(partition)
        atomic_json(pool_path, pool_document(n, m, pool))

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_scope": (
            "bounded integer favorite-pattern cell; an UNSAT result requires "
            "independent solver replay before theorem status"
        ),
        "n": n,
        "m": m,
        "upper": upper,
        "partition_universe_size": len(universe),
        "partition_shape": (
            list(partition_shape) if partition_shape is not None else None
        ),
        "partition_shapes": [
            list(shape) for shape in sorted(shape_set, reverse=True)
        ],
        "partition_singleton_good": partition_singleton_good,
        "partition_singleton_goods": sorted(singleton_goods),
        "pool_size": len(pool),
        "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "proto_path": str(proto_path.resolve()),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "seed_pools": [
            {
                "path": str(path.resolve()),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in seed_pool_paths
        ],
        "symmetry": symmetry,
        "exclude_universal_min": exclude_universal_min,
        "exclude_peelable": exclude_peelable,
        "require_pairwise_distinct_rows": require_pairwise_distinct_rows,
        "require_distinct_item_values": require_distinct_item_values,
        "require_upper_used": require_upper_used,
        "obstruction_encoding": obstruction_encoding,
        "favorite_pattern": (
            list(favorite_pattern) if favorite_pattern is not None else None
        ),
        "favorite_pattern_stabilizer": favorite_pattern_stabilizer,
        "second_favorite_pattern": (
            list(second_favorite_pattern)
            if second_favorite_pattern is not None
            else None
        ),
        "ranking_prefix_stabilizer": ranking_prefix_stabilizer,
        "half_favorite_representatives": (
            list(half_favorite_representatives)
            if half_favorite_representatives is not None
            else None
        ),
        "half_favorite_representative_stabilizer": (
            half_favorite_representative_stabilizer
        ),
        "require_singleton_threshold_failure_good": (
            require_singleton_threshold_failure_good
        ),
        "require_singleton_threshold_failure_envelope_good": (
            require_singleton_threshold_failure_envelope_good
        ),
        "owner_threshold_residual_partition_count": residual_partition_count,
        "owner_threshold_clauses": master.owner_threshold_clauses,
        "owner_threshold_envelope_rows": (
            master.owner_threshold_envelope_rows
        ),
        "comparison_variables": master.comparison_variable_count,
        "matching_clauses": master.matching_clauses,
        "hall_selectors": master.hall_selectors,
        "hall_edge_clauses": master.hall_edge_clauses,
        "solver_status": solver_status,
        "trace": trace,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
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
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--seed-pool", type=Path, action="append", default=[])
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--symmetry", choices=("none", "double_lex"), default="none")
    parser.add_argument("--exclude-universal-min", action="store_true")
    parser.add_argument("--exclude-peelable", action="store_true")
    parser.add_argument("--require-pairwise-distinct-rows", action="store_true")
    parser.add_argument("--require-distinct-item-values", action="store_true")
    parser.add_argument("--require-upper-used", action="store_true")
    parser.add_argument(
        "--obstruction-encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--favorite-pattern")
    parser.add_argument("--favorite-pattern-stabilizer", action="store_true")
    parser.add_argument("--second-favorite-pattern")
    parser.add_argument("--ranking-prefix-stabilizer", action="store_true")
    parser.add_argument("--half-favorite-representatives")
    parser.add_argument(
        "--half-favorite-representative-stabilizer",
        action="store_true",
    )
    parser.add_argument("--require-singleton-threshold-failure-good", type=int)
    parser.add_argument(
        "--require-singleton-threshold-failure-envelope-good",
        type=int,
    )
    parser.add_argument("--partition-shape", action="append", default=[])
    parser.add_argument(
        "--partition-singleton-good",
        type=int,
        action="append",
        default=[],
    )
    args = parser.parse_args()
    favorite_pattern = (
        tuple(map(int, args.favorite_pattern.split(",")))
        if args.favorite_pattern
        else None
    )
    second_favorite_pattern = (
        tuple(map(int, args.second_favorite_pattern.split(",")))
        if args.second_favorite_pattern
        else None
    )
    half_favorite_representatives = (
        tuple(map(int, args.half_favorite_representatives.split(",")))
        if args.half_favorite_representatives
        else None
    )
    partition_shapes = tuple(
        tuple(map(int, raw.split(",")))
        for raw in args.partition_shape
    )
    run(
        n=args.n,
        m=args.m,
        upper=args.upper,
        pool_path=args.pool,
        result_path=args.result,
        proto_path=args.proto,
        seed_pool_paths=args.seed_pool,
        add_per_iteration=args.add_per_iteration,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        workers=args.workers,
        random_seed=args.random_seed,
        symmetry=args.symmetry,
        exclude_universal_min=args.exclude_universal_min,
        exclude_peelable=args.exclude_peelable,
        require_pairwise_distinct_rows=args.require_pairwise_distinct_rows,
        require_distinct_item_values=args.require_distinct_item_values,
        require_upper_used=args.require_upper_used,
        obstruction_encoding=args.obstruction_encoding,
        favorite_pattern=favorite_pattern,
        favorite_pattern_stabilizer=args.favorite_pattern_stabilizer,
        second_favorite_pattern=second_favorite_pattern,
        ranking_prefix_stabilizer=args.ranking_prefix_stabilizer,
        half_favorite_representatives=half_favorite_representatives,
        half_favorite_representative_stabilizer=(
            args.half_favorite_representative_stabilizer
        ),
        require_singleton_threshold_failure_good=(
            args.require_singleton_threshold_failure_good
        ),
        require_singleton_threshold_failure_envelope_good=(
            args.require_singleton_threshold_failure_envelope_good
        ),
        partition_shape=(
            partition_shapes[0] if len(partition_shapes) == 1 else None
        ),
        partition_shapes=(
            partition_shapes if len(partition_shapes) > 1 else ()
        ),
        partition_singleton_goods=tuple(args.partition_singleton_good),
    )


if __name__ == "__main__":
    main()
