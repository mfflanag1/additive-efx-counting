#!/usr/bin/env python3
"""CEGAR for balanced EFX under universal favorite-threshold failure."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_favorite_singleton_hall_boundaries import residual_partitions
    from .lra_master import ParkabilityLRAMaster
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_favorite_singleton_hall_boundaries import residual_partitions
    from lra_master import ParkabilityLRAMaster
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "universal-threshold-balanced-lra-result-v1"
N = 4
M = 9
FAVORITE = 0


def balanced_universe():
    return tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    )


def sorted_descending(expressions):
    ordered = list(expressions)
    for upper in range(len(ordered) - 1, 0, -1):
        for index in range(upper):
            left = ordered[index]
            right = ordered[index + 1]
            ordered[index] = z3.If(left >= right, left, right)
            ordered[index + 1] = z3.If(left >= right, right, left)
    return tuple(ordered)


def add_universal_threshold_failure(master: ParkabilityLRAMaster) -> None:
    for observer in range(N):
        favorite = master.values[observer][FAVORITE]
        ordered = sorted_descending(master.values[observer][1:])
        master.solver.add(
            ordered[4] + ordered[5] + ordered[6] > favorite,
            z3.Or(
                ordered[2] + ordered[6] > favorite,
                ordered[3] + ordered[4] > favorite,
            ),
        )


def add_universal_threshold_failure_cardinal(master: ParkabilityLRAMaster) -> None:
    """Equivalent envelope encoding without arithmetic sorting networks."""
    residual = tuple(range(1, M))
    for observer in range(N):
        favorite = master.values[observer][FAVORITE]
        for four_set in itertools.combinations(residual, 4):
            master.solver.add(
                z3.Or(
                    *(
                        master._sum(
                            observer,
                            tuple(good for good in four_set if good != removed),
                        )
                        > favorite
                        for removed in four_set
                    )
                )
            )
        pair_edges = {}
        for left, right in itertools.combinations(residual, 2):
            edge = z3.Bool(
                f"threshold_pair_agent_{observer}_goods_{left}_{right}"
            )
            master.solver.add(
                edge
                == (
                    master.values[observer][left]
                    + master.values[observer][right]
                    > favorite
                )
            )
            pair_edges[left, right] = edge

        degree_at_least_six = []
        degree_at_least_four = []
        for good in residual:
            incident = tuple(
                pair_edges[tuple(sorted((good, other)))]
                for other in residual
                if other != good
            )
            degree_at_least_six.append(z3.PbGe(tuple((edge, 1) for edge in incident), 6))
            degree_at_least_four.append(z3.PbGe(tuple((edge, 1) for edge in incident), 4))
        master.solver.add(
            z3.Or(
                z3.PbGe(tuple((edge, 1) for edge in degree_at_least_six), 3),
                z3.PbGe(tuple((edge, 1) for edge in degree_at_least_four), 4),
            )
        )


def audit_threshold_failure(values: tuple[tuple[int, ...], ...]) -> None:
    for observer, row in enumerate(values):
        if any(row[FAVORITE] <= row[good] for good in range(1, M)):
            raise AssertionError("model lost its strict common favorite")
        for partition in residual_partitions():
            threshold = max(
                sum(row[good] for good in bundle)
                - min(row[good] for good in bundle)
                for bundle in partition
            )
            if threshold <= row[FAVORITE]:
                raise AssertionError((observer, partition, threshold))


def run(
    *,
    result_path: Path,
    smt2_path: Path,
    time_limit_s: float,
    add_per_iteration: int,
    max_iterations: int,
    encoding: str,
    seed_value_paths: tuple[Path, ...],
    fixed_half_representatives: bool,
) -> dict:
    universe = balanced_universe()
    if len(universe) != 1260:
        raise AssertionError("balanced partition universe changed")
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    if fixed_half_representatives:
        for observer in range(N):
            master.solver.add(
                2 * master.values[observer][observer + 1]
                > master.values[observer][FAVORITE]
            )
    else:
        master.add_favorite_pattern_stabilizer((FAVORITE,) * N)
    add_universal_threshold_failure(master)

    pool = set()
    for seed_path in seed_value_paths:
        source = json.loads(seed_path.read_text())
        raw_values = source.get("values")
        if raw_values is None:
            raw_values = source["trace"][0]["values"]
        seed_values = core.validate_values(
            raw_values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        for partition in supported_partitions(seed_values, list(universe)):
            if partition not in pool:
                master.add_partition_obstruction(partition, encoding=encoding)
                pool.add(partition)
    trace = []
    started = time.time()
    status = "ITERATION_LIMIT"
    reason_unknown = None
    solver_status = None
    result_values = None
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
        audit_threshold_failure(solved.values)
        survivors = tuple(
            partition
            for partition in supported_partitions(solved.values, list(universe))
            if partition not in pool
        )
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(pool),
            "supported_partition_count": len(survivors),
            "values": [list(row) for row in solved.values],
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"supported_partitions={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "ZERO_BALANCED_EFX"
            result_values = solved.values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition, encoding=encoding)
            pool.add(partition)

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    literal_count = None
    if result_values is not None:
        literal_count = independent.count_complete_efx0(result_values)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solver_status,
        "reason_unknown": reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "favorite_pattern": [FAVORITE] * N,
        "universal_threshold_failure": True,
        "threshold_encoding": "exact 3+3+2 / 4+2+2 sorted shape envelope",
        "fixed_half_representatives": fixed_half_representatives,
        "residual_partitions_per_owner": len(residual_partitions()),
        "target_shape": [3, 2, 2, 2],
        "target_partition_count": len(universe),
        "obstruction_encoding": encoding,
        "pool_size": len(pool),
        "seed_values": [str(path.resolve()) for path in seed_value_paths],
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "literal_complete_efx_count": literal_count,
        "trace": trace,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE would prove, subject to independent replay, "
            "that universal owner-threshold failure forces balanced EFX in "
            "the strict common-favorite 4x9 cell. ZERO_BALANCED_EFX would "
            "refute only that structural implication, not general EFX."
        ),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--add", type=int, default=16)
    parser.add_argument("--max-iterations", type=int, default=50)
    parser.add_argument("--seed-values", type=Path, action="append", default=[])
    parser.add_argument("--fixed-half-representatives", action="store_true")
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "inline_matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    args = parser.parse_args()
    if args.time_limit < 0 or args.add < 1 or args.max_iterations < 1:
        parser.error("invalid search limits")
    result = run(
        result_path=args.result,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        encoding=args.encoding,
        seed_value_paths=tuple(args.seed_values),
        fixed_half_representatives=args.fixed_half_representatives,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
