#!/usr/bin/env python3
"""Exact QF_LRA search through EFX-feasible partition matchings."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from . import core, independent
    from .lra_master import ParkabilityLRAMaster
    from .run_efx_lra_cegar import (
        has_favorite_good_matching,
        has_peelable_good,
        has_repeated_normalized_rows,
    )
    from .run_lra_cegar import (
        atomic_json,
        atomic_write,
        canonical_sha256,
        has_universal_min,
    )
except ImportError:
    import core
    import independent
    from lra_master import ParkabilityLRAMaster
    from run_efx_lra_cegar import (
        has_favorite_good_matching,
        has_peelable_good,
        has_repeated_normalized_rows,
    )
    from run_lra_cegar import (
        atomic_json,
        atomic_write,
        canonical_sha256,
        has_universal_min,
    )


SCHEMA = "partition-matching-lra-result-v1"
N = 4
M = 8


def run(
    *,
    time_limit_s: float,
    symmetry: str,
    exclude_peelable: bool,
    require_pairwise_distinct_rows: bool,
    require_favorite_hall_deficiency: bool,
    strict_favorite_pattern: tuple[int, ...] | None,
    favorite_pattern_stabilizer: bool,
    strict_second_favorite_pattern: tuple[int, ...] | None,
    ranking_prefix_stabilizer: bool,
    obstruction_encoding: str,
    selected_shapes: tuple[str, ...] | None,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if (
        time_limit_s < 0
        or symmetry not in {"none", "double_lex"}
        or obstruction_encoding not in {"matching_clauses", "hall_selectors"}
    ):
        raise ValueError("invalid timeout or symmetry")
    if (
        result_path.resolve() == smt2_path.resolve()
        or result_path.exists()
        or smt2_path.exists()
    ):
        raise ValueError("result and SMT2 paths must be distinct and new")

    started = time.time()
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_favorite_hall_deficiency=require_favorite_hall_deficiency,
        symmetry=symmetry,
    )
    if strict_favorite_pattern is not None:
        if len(strict_favorite_pattern) != N or any(
            not 0 <= good < M for good in strict_favorite_pattern
        ):
            raise ValueError("strict favorite pattern must contain four goods")
        master.add_strict_favorite_pattern(strict_favorite_pattern)
        if favorite_pattern_stabilizer:
            master.add_favorite_pattern_stabilizer(strict_favorite_pattern)
    elif favorite_pattern_stabilizer:
        raise ValueError("favorite-pattern stabilizer requires a favorite pattern")
    ranking_prefixes = None
    if strict_second_favorite_pattern is not None:
        if (
            strict_favorite_pattern is None
            or len(strict_second_favorite_pattern) != N
            or any(not 0 <= good < M for good in strict_second_favorite_pattern)
            or any(
                favorite == second
                for favorite, second in zip(
                    strict_favorite_pattern,
                    strict_second_favorite_pattern,
                )
            )
        ):
            raise ValueError("second-favorite pattern requires distinct favorite goods")
        ranking_prefixes = tuple(
            (favorite, second)
            for favorite, second in zip(
                strict_favorite_pattern,
                strict_second_favorite_pattern,
            )
        )
        master.add_strict_ranking_prefixes(ranking_prefixes)
        if ranking_prefix_stabilizer:
            master.add_ranking_prefix_stabilizer(ranking_prefixes)
    elif ranking_prefix_stabilizer:
        raise ValueError("ranking-prefix stabilizer requires a second pattern")
    shape_counts = Counter()
    partition_count = 0
    selected_shape_set = (
        set(selected_shapes)
        if selected_shapes is not None
        else {"5111", "4211", "3311", "3221", "2222"}
    )
    for partition in core.iter_unlabeled_nonempty_partitions(N, M):
        partition_shape = "".join(
            map(str, sorted(map(len, partition), reverse=True))
        )
        if partition_shape not in selected_shape_set:
            continue
        if not master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
        ):
            raise AssertionError("partition generator emitted a duplicate")
        shape_counts[partition_shape] += 1
        partition_count += 1
    if selected_shapes is None and partition_count != 1701:
        raise AssertionError("unexpected (4,8) partition count")

    formula = master.to_smt2()
    atomic_write(smt2_path, formula)
    formula_seconds = time.time() - started
    solve_started = time.time()
    solved = master.solve(time_limit_s=time_limit_s)
    solve_seconds = time.time() - solve_started
    status = (
        "UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "SAT_CANDIDATE"
        if solved.status == "SAT"
        else "MASTER_UNKNOWN"
    )
    extra = {}
    if solved.status == "SAT":
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        if has_universal_min(values):
            raise AssertionError("partition model violated the universal-minimum cut")
        if exclude_peelable and has_peelable_good(values):
            raise AssertionError("partition model violated the peeling cut")
        if (
            require_pairwise_distinct_rows
            and has_repeated_normalized_rows(values)
        ):
            raise AssertionError("partition model violated the row-type cut")
        if (
            require_favorite_hall_deficiency
            and has_favorite_good_matching(values)
        ):
            raise AssertionError("partition model violated the favorite-Hall cut")
        if strict_favorite_pattern is not None and any(
            max(range(M), key=values[observer].__getitem__) != favorite
            or values[observer].count(values[observer][favorite]) != 1
            for observer, favorite in enumerate(strict_favorite_pattern)
        ):
            raise AssertionError("partition model violated the strict favorite pattern")
        if ranking_prefixes is not None and any(
            tuple(
                sorted(range(M), key=values[observer].__getitem__, reverse=True)[:2]
            )
            != ranking
            for observer, ranking in enumerate(ranking_prefixes)
        ):
            raise AssertionError("partition model violated the strict ranking prefix")
        assignments = list(core.iter_efx0_assignments(values))
        surviving_shapes = Counter(
            "".join(
                map(
                    str,
                    sorted(
                        (
                            assignment.count(agent)
                            for agent in range(N)
                        ),
                        reverse=True,
                    ),
                )
            )
            for assignment in assignments
        )
        if any(surviving_shapes[shape] for shape in selected_shape_set):
            raise AssertionError("partition candidate survived a selected shape")
        literal_count = independent.count_complete_efx0(values)
        if literal_count != len(assignments):
            raise AssertionError("partition candidate count failed literal audit")
        full_universe = len(selected_shape_set) == 5
        if full_universe:
            base_first = independent.enumerate_base_first(values)
            completion_first = independent.enumerate_completion_first(values)
            if assignments or base_first or completion_first:
                raise AssertionError("partition zero candidate failed independent audit")
            status = "ZERO_COMPLETE_EFX0"
            base_first_count = len(base_first)
            completion_first_count = len(completion_first)
        else:
            base_first_count = None
            completion_first_count = None
        extra = {
            "values": [list(row) for row in values],
            "values_sha256": canonical_sha256(values),
            "independent_audit": {
                "complete_efx0_count": literal_count,
                "complete_efx0_count_by_shape": dict(
                    sorted(surviving_shapes.items())
                ),
                "base_first_parkable_triples": base_first_count,
                "completion_first_parkable_triples": completion_first_count,
            },
            "meaning": (
                "positive-rational additive-EFX counterexample, also "
                "zero-parkability by threshold-cycle equivalence"
                if full_universe
                else "exact rational candidate avoiding every selected shape"
            ),
        }
    elif solved.status == "UNSAT":
        extra["meaning"] = (
            "exact-LRA closure of every selected bundle partition in the "
            "stated residual cases; independent proof required"
        )
    else:
        extra["meaning"] = "inconclusive exact-LRA partition master solve"

    result = {
        "schema": SCHEMA,
        "status": status,
        "n": N,
        "m": M,
        "domain": "strictly_positive_reals_normalized_per_row",
        "case_cut": "no_universal_minimum_good",
        "exclude_peelable": exclude_peelable,
        "require_pairwise_distinct_rows": require_pairwise_distinct_rows,
        "require_favorite_hall_deficiency": require_favorite_hall_deficiency,
        "strict_favorite_pattern": (
            list(strict_favorite_pattern)
            if strict_favorite_pattern is not None
            else None
        ),
        "favorite_pattern_stabilizer": favorite_pattern_stabilizer,
        "strict_second_favorite_pattern": (
            list(strict_second_favorite_pattern)
            if strict_second_favorite_pattern is not None
            else None
        ),
        "ranking_prefix_stabilizer": ranking_prefix_stabilizer,
        "symmetry": symmetry,
        "obstruction_encoding": obstruction_encoding,
        "selected_shapes": sorted(selected_shape_set),
        "partition_count": partition_count,
        "partition_count_by_shape": dict(sorted(shape_counts.items())),
        "feasibility_edge_variables": partition_count * N * N,
        "edge_comparison_references": partition_count * N * (N * M - M),
        "perfect_matching_obstruction_clauses": partition_count
        * math.factorial(N)
        if obstruction_encoding == "matching_clauses"
        else 0,
        "hall_selector_variables": partition_count * ((1 << N) - N - 1)
        if obstruction_encoding == "hall_selectors"
        else 0,
        "formula_build_seconds": round(formula_seconds, 6),
        "solver_wall_seconds": round(solve_seconds, 6),
        "elapsed_seconds": round(time.time() - started, 6),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
        **extra,
    }
    atomic_json(result_path, result)
    print(
        f"{status} partitions={partition_count} "
        f"build={formula_seconds:.3f}s solve={solve_seconds:.3f}s",
        flush=True,
    )
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-limit", type=float, default=7200)
    parser.add_argument(
        "--symmetry",
        choices=("none", "double_lex"),
        default="none",
    )
    parser.add_argument("--exclude-peelable", action="store_true")
    parser.add_argument("--require-pairwise-distinct-rows", action="store_true")
    parser.add_argument("--require-favorite-hall-deficiency", action="store_true")
    parser.add_argument(
        "--favorite-pattern",
        help="comma-separated strict favorite good for each of the four agents",
    )
    parser.add_argument("--favorite-pattern-stabilizer", action="store_true")
    parser.add_argument(
        "--second-favorite-pattern",
        help="comma-separated strict second-favorite good for each agent",
    )
    parser.add_argument("--ranking-prefix-stabilizer", action="store_true")
    parser.add_argument(
        "--obstruction-encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument(
        "--shape",
        action="append",
        choices=("5111", "4211", "3311", "3221", "2222"),
    )
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    strict_favorite_pattern = (
        tuple(map(int, args.favorite_pattern.split(",")))
        if args.favorite_pattern is not None
        else None
    )
    strict_second_favorite_pattern = (
        tuple(map(int, args.second_favorite_pattern.split(",")))
        if args.second_favorite_pattern is not None
        else None
    )
    run(
        time_limit_s=args.time_limit,
        symmetry=args.symmetry,
        exclude_peelable=args.exclude_peelable,
        require_pairwise_distinct_rows=args.require_pairwise_distinct_rows,
        require_favorite_hall_deficiency=args.require_favorite_hall_deficiency,
        strict_favorite_pattern=strict_favorite_pattern,
        favorite_pattern_stabilizer=args.favorite_pattern_stabilizer,
        strict_second_favorite_pattern=strict_second_favorite_pattern,
        ranking_prefix_stabilizer=args.ranking_prefix_stabilizer,
        obstruction_encoding=args.obstruction_encoding,
        selected_shapes=tuple(args.shape) if args.shape is not None else None,
        result_path=args.result,
        smt2_path=args.smt2,
    )


if __name__ == "__main__":
    main()
