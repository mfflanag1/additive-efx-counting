#!/usr/bin/env python3
"""Exact CEGAR over EFX-feasible unlabeled bundle partitions."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json, has_universal_min
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from anneal import atomic_json, has_universal_min
    from audit_matching_augmentation import feasible_graph, matching_rank
    from lra_master import ParkabilityLRAMaster


Partition = tuple[tuple[int, ...], ...]


def pool_document(n: int, m: int, partitions: list[Partition]) -> dict:
    return {
        "schema": "generic-partition-lra-pool-v1",
        "n": n,
        "m": m,
        "partitions": [
            [list(bundle) for bundle in partition]
            for partition in partitions
        ],
    }


def load_pool(path: Path, n: int, m: int) -> list[Partition]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    if (
        raw.get("schema") != "generic-partition-lra-pool-v1"
        or raw.get("n") != n
        or raw.get("m") != m
        or not isinstance(raw.get("partitions"), list)
    ):
        raise ValueError("partition pool metadata does not match the cell")
    partitions = [
        tuple(tuple(bundle) for bundle in raw_partition)
        for raw_partition in raw["partitions"]
    ]
    if len(partitions) != len(set(partitions)):
        raise ValueError("partition pool contains duplicates")
    return partitions


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
    seed_paths: list[Path],
    pool_path: Path,
    result_path: Path,
    smt2_path: Path,
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
    symmetry: str,
    exclude_universal_min: bool,
    exclude_peelable: bool,
    require_pairwise_distinct_rows: bool,
    require_distinct_item_values: bool,
    obstruction_encoding: str,
    favorite_pattern: tuple[int, ...] | None,
    favorite_pattern_stabilizer: bool,
    second_favorite_pattern: tuple[int, ...] | None,
    ranking_prefix_stabilizer: bool,
    integer_upper: int | None = None,
    seed_pool_paths: list[Path] | None = None,
    partition_shape: tuple[int, ...] | None = None,
    additional_partition_shapes: tuple[tuple[int, ...], ...] = (),
    partition_singleton_goods: tuple[int, ...] = (),
) -> dict:
    if (
        favorite_pattern_stabilizer
        and second_favorite_pattern is not None
        and any(
            favorite_pattern[left] == favorite_pattern[right]
            and second_favorite_pattern[left] != second_favorite_pattern[right]
            for left in range(n)
            for right in range(left + 1, n)
        )
    ):
        raise ValueError("favorite stabilizer does not preserve the ranking cell")
    partition_shapes = (
        (() if partition_shape is None else (partition_shape,))
        + additional_partition_shapes
    )
    if (
        len(set(partition_shapes)) != len(partition_shapes)
        or any(
            len(shape) != n
            or tuple(sorted(shape, reverse=True)) != shape
            or any(size < 1 for size in shape)
            or sum(shape) != m
            for shape in partition_shapes
        )
    ):
        raise ValueError(
            "partition shapes must be distinct descending compositions of m"
        )
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
    universe = [
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(n, m)
        if (
            not partition_shapes
            and not singleton_goods
        )
        or (
            tuple(sorted(map(len, partition), reverse=True)) in partition_shapes
        )
        or (
            singleton_goods
            and any((good,) in partition for good in singleton_goods)
        )
    ]
    pool = load_pool(pool_path, n, m)
    if any(partition not in universe for partition in pool):
        raise ValueError("existing pool contains a partition outside the target scope")
    pool_set = set(pool)
    seed_pool_paths = [] if seed_pool_paths is None else seed_pool_paths
    for seed_pool_path in seed_pool_paths:
        for partition in load_pool(seed_pool_path, n, m):
            if partition not in pool_set:
                pool.append(partition)
                pool_set.add(partition)
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
        for candidate in candidates:
            values = core.validate_values(
                candidate,
                expected_n=n,
                expected_m=m,
                lower=1,
            )
            for partition in supported_partitions(values, universe):
                if partition not in pool_set:
                    pool.append(partition)
                    pool_set.add(partition)
    atomic_json(pool_path, pool_document(n, m, pool))

    master = ParkabilityLRAMaster(
        n,
        m,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_distinct_item_values=require_distinct_item_values,
        symmetry=symmetry,
        integer_upper=integer_upper,
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
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit_s)
        solver_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
        )
        if exclude_universal_min and has_universal_min(
            [list(row) for row in values]
        ):
            raise AssertionError("model violated the universal-minimum cut")
        survivors = supported_partitions(values, universe)
        if any(partition in pool_set for partition in survivors):
            raise AssertionError("model satisfies a pooled partition")
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(pool),
            "supported_partition_count": len(survivors),
            "values": [list(row) for row in values],
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"supported_partitions={len(survivors)}",
            flush=True,
        )
        if not survivors:
            if partition_shapes or singleton_goods:
                status = "ZERO_SUPPORTED_PARTITIONS"
                result_values = values
                break
            literal_count = independent.count_complete_efx0(values)
            if literal_count:
                raise AssertionError("independent verifier rejected zero EFX")
            status = "ZERO_COMPLETE_EFX"
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

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": "generic-partition-lra-result-v1",
        "status": status,
        "n": n,
        "m": m,
        "partition_universe_size": len(universe),
        "partition_shape": (
            list(partition_shape) if partition_shape is not None else None
        ),
        "additional_partition_shapes": [
            list(shape) for shape in additional_partition_shapes
        ],
        "partition_singleton_goods": sorted(singleton_goods),
        "domain": (
            f"positive integers in [1,{integer_upper}]"
            if integer_upper is not None
            else "strictly positive reals normalized per row"
        ),
        "integer_upper": integer_upper,
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
        "obstruction_encoding": obstruction_encoding,
        "favorite_pattern": (
            list(favorite_pattern)
            if favorite_pattern is not None
            else None
        ),
        "favorite_pattern_stabilizer": favorite_pattern_stabilizer,
        "second_favorite_pattern": (
            list(second_favorite_pattern)
            if second_favorite_pattern is not None
            else None
        ),
        "ranking_prefix_stabilizer": ranking_prefix_stabilizer,
        "iterations": iteration,
        "pool_size": len(pool),
        "elapsed_seconds": time.time() - started,
        "solver_status": solver_status,
        "reason_unknown": reason_unknown,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "trace": trace,
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=9)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--add", type=int, default=512)
    parser.add_argument("--max-iterations", type=int, default=50)
    parser.add_argument("--time-limit", type=float, default=900)
    parser.add_argument(
        "--symmetry",
        choices=("none", "double_lex"),
        default="none",
    )
    parser.add_argument("--exclude-universal-min", action="store_true")
    parser.add_argument("--exclude-peelable", action="store_true")
    parser.add_argument("--require-pairwise-distinct-rows", action="store_true")
    parser.add_argument("--require-distinct-item-values", action="store_true")
    parser.add_argument("--favorite-pattern")
    parser.add_argument("--favorite-pattern-stabilizer", action="store_true")
    parser.add_argument("--second-favorite-pattern")
    parser.add_argument("--ranking-prefix-stabilizer", action="store_true")
    parser.add_argument("--integer-upper", type=int)
    parser.add_argument("--seed-pool", type=Path, action="append", default=[])
    parser.add_argument("--partition-shape")
    parser.add_argument(
        "--additional-partition-shape",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--partition-singleton-good",
        type=int,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--obstruction-encoding",
        choices=(
            "matching_clauses",
            "inline_matching_clauses",
            "hall_selectors",
        ),
        default="matching_clauses",
    )
    args = parser.parse_args()
    if (
        args.n < 2
        or args.m < args.n
        or args.add < 1
        or args.max_iterations < 1
        or args.time_limit < 0
        or (args.integer_upper is not None and args.integer_upper < 1)
    ):
        parser.error("invalid cell or search limits")
    favorite_pattern = (
        tuple(map(int, args.favorite_pattern.split(",")))
        if args.favorite_pattern is not None
        else None
    )
    if favorite_pattern is not None and (
        len(favorite_pattern) != args.n
        or any(not 0 <= good < args.m for good in favorite_pattern)
    ):
        parser.error("favorite pattern must specify one good per agent")
    if args.favorite_pattern_stabilizer and favorite_pattern is None:
        parser.error("favorite stabilizer requires a favorite pattern")
    second_favorite_pattern = (
        tuple(map(int, args.second_favorite_pattern.split(",")))
        if args.second_favorite_pattern is not None
        else None
    )
    if second_favorite_pattern is not None and (
        favorite_pattern is None
        or len(second_favorite_pattern) != args.n
        or any(not 0 <= good < args.m for good in second_favorite_pattern)
        or any(
            favorite == second
            for favorite, second in zip(
                favorite_pattern,
                second_favorite_pattern,
            )
        )
    ):
        parser.error("second favorites must be valid and differ from favorites")
    if args.ranking_prefix_stabilizer and second_favorite_pattern is None:
        parser.error("ranking stabilizer requires second favorites")
    if (
        args.favorite_pattern_stabilizer
        and second_favorite_pattern is not None
        and any(
            favorite_pattern[left] == favorite_pattern[right]
            and second_favorite_pattern[left] != second_favorite_pattern[right]
            for left in range(args.n)
            for right in range(left + 1, args.n)
        )
    ):
        parser.error(
            "favorite stabilizer is unsound when equal-favorite agents "
            "have different fixed second favorites"
        )
    partition_shape = (
        tuple(map(int, args.partition_shape.split(",")))
        if args.partition_shape
        else None
    )
    additional_partition_shapes = tuple(
        tuple(map(int, raw.split(",")))
        for raw in args.additional_partition_shape
    )
    result = run(
        n=args.n,
        m=args.m,
        seed_paths=args.seed,
        pool_path=args.pool,
        result_path=args.result,
        smt2_path=args.smt2,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        symmetry=args.symmetry,
        exclude_universal_min=args.exclude_universal_min,
        exclude_peelable=args.exclude_peelable,
        require_pairwise_distinct_rows=args.require_pairwise_distinct_rows,
        require_distinct_item_values=args.require_distinct_item_values,
        obstruction_encoding=args.obstruction_encoding,
        favorite_pattern=favorite_pattern,
        favorite_pattern_stabilizer=args.favorite_pattern_stabilizer,
        second_favorite_pattern=second_favorite_pattern,
        ranking_prefix_stabilizer=args.ranking_prefix_stabilizer,
        integer_upper=args.integer_upper,
        seed_pool_paths=args.seed_pool,
        partition_shape=partition_shape,
        additional_partition_shapes=additional_partition_shapes,
        partition_singleton_goods=tuple(args.partition_singleton_good),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
