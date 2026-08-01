#!/usr/bin/env python3
"""Exact partition CEGAR driven by a pinned external SMT solver."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json, has_universal_min
    from .audit_matching_augmentation import feasible_graph
    from .decode_cvc5_values import decode
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write, normalize
    from .run_external_smt import run as run_external
    from .run_generic_partition_cegar import (
        load_pool,
        pool_document,
        supported_partitions,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json, has_universal_min
    from audit_matching_augmentation import feasible_graph
    from decode_cvc5_values import decode
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write, normalize
    from run_external_smt import run as run_external
    from run_generic_partition_cegar import (
        load_pool,
        pool_document,
        supported_partitions,
    )


Partition = tuple[tuple[int, ...], ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seed_values(path: Path, n: int, m: int) -> list[tuple[tuple[int, ...], ...]]:
    raw = json.loads(path.read_text())
    candidates = []
    if raw.get("values") is not None:
        candidates.append(raw["values"])
    candidates.extend(
        record["values"]
        for record in raw.get("trace", [])
        if record.get("values") is not None
    )
    return [
        core.validate_values(candidate, expected_n=n, expected_m=m, lower=1)
        for candidate in candidates
    ]


def build_master(
    *,
    n: int,
    m: int,
    partitions: list[Partition],
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
) -> ParkabilityLRAMaster:
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
    master = ParkabilityLRAMaster(
        n,
        m,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_distinct_item_values=require_distinct_item_values,
        symmetry=symmetry,
    )
    if favorite_pattern is not None:
        master.add_strict_favorite_pattern(favorite_pattern)
        if favorite_pattern_stabilizer:
            master.add_favorite_pattern_stabilizer(favorite_pattern)
    if second_favorite_pattern is not None:
        ranking_prefixes = tuple(zip(favorite_pattern, second_favorite_pattern))
        master.add_strict_ranking_prefixes(ranking_prefixes)
        if ranking_prefix_stabilizer:
            master.add_ranking_prefix_stabilizer(ranking_prefixes)
    for partition in partitions:
        master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
        )
    return master


def run(
    *,
    n: int,
    m: int,
    seed_paths: list[Path],
    pool_path: Path,
    result_path: Path,
    artifact_prefix: Path,
    solver_path: Path,
    solver_args: tuple[str, ...],
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
) -> dict:
    if result_path.exists():
        raise ValueError("result path must be new")
    universe = list(core.iter_unlabeled_nonempty_partitions(n, m))
    pool = load_pool(pool_path, n, m)
    pool_set = set(pool)
    imported = []
    for seed_path in seed_paths:
        for values in seed_values(seed_path, n, m):
            survivors = supported_partitions(values, universe)
            added = 0
            for partition in survivors:
                if partition not in pool_set:
                    pool.append(partition)
                    pool_set.add(partition)
                    added += 1
            imported.append({
                "path": str(seed_path.resolve()),
                "sha256": sha256(seed_path),
                "supported_partition_count": len(survivors),
                "new_partition_count": added,
            })
    atomic_json(pool_path, pool_document(n, m, pool))

    master = build_master(
        n=n,
        m=m,
        partitions=pool,
        symmetry=symmetry,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_distinct_item_values=require_distinct_item_values,
        obstruction_encoding=obstruction_encoding,
        favorite_pattern=favorite_pattern,
        favorite_pattern_stabilizer=favorite_pattern_stabilizer,
        second_favorite_pattern=second_favorite_pattern,
        ranking_prefix_stabilizer=ranking_prefix_stabilizer,
    )
    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    for iteration in range(1, max_iterations + 1):
        source_path = Path(f"{artifact_prefix}.iteration{iteration}.smt2")
        normalized_path = Path(f"{artifact_prefix}.iteration{iteration}.cvc5.smt2")
        solver_result_path = Path(
            f"{artifact_prefix}.iteration{iteration}.cvc5.json"
        )
        for path in (source_path, normalized_path, solver_result_path):
            if path.exists():
                raise ValueError(f"artifact path must be new: {path}")
        source = master.to_smt2()
        atomic_write(source_path, source.encode())
        normalized, replacement_count = normalize(source)
        atomic_write(normalized_path, normalized.encode())
        solved = run_external(
            solver_path=solver_path,
            formula_path=normalized_path,
            result_path=solver_result_path,
            time_limit_s=time_limit_s,
            solver_args=("--produce-models", "--dump-models", *solver_args),
            expected=None,
            interface="cvc5",
            quiet=True,
        )
        record = {
            "iteration": iteration,
            "pool_size_before": len(pool),
            "source_path": str(source_path.resolve()),
            "source_sha256": sha256(source_path),
            "normalized_path": str(normalized_path.resolve()),
            "normalized_sha256": sha256(normalized_path),
            "unary_sum_replacements": replacement_count,
            "solver_result_path": str(solver_result_path.resolve()),
            "solver_result_sha256": sha256(solver_result_path),
            "solver_verdict": solved["verdict"],
            "solver_elapsed_seconds": solved["elapsed_seconds"],
        }
        if solved["verdict"] == "unsat":
            status = "UNSAT_CANDIDATE"
            trace.append(record)
            break
        if solved["verdict"] != "sat":
            status = "MASTER_UNKNOWN"
            trace.append(record)
            break

        values = core.validate_values(
            decode(solved["stdout"], n, m),
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
            raise AssertionError("external model satisfies a pooled partition")
        literal_count = independent.count_complete_efx0(values)
        matching_count = sum(
            all(graph[agent][matching[agent]] for agent in range(n))
            for partition in survivors
            for graph in [feasible_graph(values, partition)]
            for matching in itertools.permutations(range(n))
        )
        if literal_count != matching_count:
            raise AssertionError("partition and literal enumerators disagree")
        model_path = Path(f"{artifact_prefix}.iteration{iteration}.values.json")
        atomic_json(model_path, {
            "schema": "external-partition-cegar-model-v1",
            "n": n,
            "m": m,
            "source": str(solver_result_path.resolve()),
            "source_sha256": sha256(solver_result_path),
            "values": [list(row) for row in values],
            "supported_partition_count": len(survivors),
            "complete_efx0_count": literal_count,
            "matching_complete_efx0_count": matching_count,
        })
        record.update({
            "model_path": str(model_path.resolve()),
            "model_sha256": sha256(model_path),
            "supported_partition_count": len(survivors),
            "complete_efx0_count": literal_count,
            "matching_complete_efx0_count": matching_count,
        })
        if not survivors:
            status = "ZERO_COMPLETE_EFX"
            result_values = values
            trace.append(record)
            break
        added = 0
        for partition in survivors[:add_per_iteration]:
            if partition in pool_set:
                continue
            master.add_partition_obstruction(
                partition,
                encoding=obstruction_encoding,
            )
            pool.append(partition)
            pool_set.add(partition)
            added += 1
        record["new_partition_count"] = added
        trace.append(record)
        atomic_json(pool_path, pool_document(n, m, pool))
        print(
            f"iteration={iteration} verdict=sat pool={len(pool)} "
            f"partitions={len(survivors)} allocations={literal_count}",
            flush=True,
        )

    result = {
        "schema": "external-partition-cegar-result-v1",
        "status": status,
        "n": n,
        "m": m,
        "partition_universe_size": len(universe),
        "domain": "strictly_positive_reals_normalized_per_row",
        "solver": str(solver_path.resolve()),
        "solver_sha256": sha256(solver_path),
        "solver_args": list(solver_args),
        "time_limit_seconds_per_iteration": time_limit_s,
        "symmetry": symmetry,
        "exclude_universal_min": exclude_universal_min,
        "exclude_peelable": exclude_peelable,
        "require_pairwise_distinct_rows": require_pairwise_distinct_rows,
        "require_distinct_item_values": require_distinct_item_values,
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
        "seed_imports": imported,
        "iterations": len(trace),
        "pool_size": len(pool),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": sha256(pool_path),
        "elapsed_seconds": time.time() - started,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "trace": trace,
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def parse_pattern(
    parser: argparse.ArgumentParser,
    raw: str | None,
    n: int,
    m: int,
    label: str,
) -> tuple[int, ...] | None:
    if raw is None:
        return None
    pattern = tuple(map(int, raw.split(",")))
    if len(pattern) != n or any(not 0 <= good < m for good in pattern):
        parser.error(f"{label} must specify one valid good per agent")
    return pattern


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=9)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--artifact-prefix", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--solver-arg", action="append", default=[])
    parser.add_argument("--add", type=int, default=512)
    parser.add_argument("--max-iterations", type=int, default=20)
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
        or args.time_limit <= 0
    ):
        parser.error("invalid cell or search limits")
    favorite_pattern = parse_pattern(
        parser,
        args.favorite_pattern,
        args.n,
        args.m,
        "favorite pattern",
    )
    second_favorite_pattern = parse_pattern(
        parser,
        args.second_favorite_pattern,
        args.n,
        args.m,
        "second-favorite pattern",
    )
    if args.favorite_pattern_stabilizer and favorite_pattern is None:
        parser.error("favorite stabilizer requires a favorite pattern")
    if second_favorite_pattern is not None and (
        favorite_pattern is None
        or any(
            first == second
            for first, second in zip(favorite_pattern, second_favorite_pattern)
        )
    ):
        parser.error("second favorites must differ from favorites")
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
    run(
        n=args.n,
        m=args.m,
        seed_paths=args.seed,
        pool_path=args.pool,
        result_path=args.result,
        artifact_prefix=args.artifact_prefix,
        solver_path=args.solver,
        solver_args=tuple(args.solver_arg),
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
    )


if __name__ == "__main__":
    main()
