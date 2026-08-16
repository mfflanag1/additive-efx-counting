#!/usr/bin/env python3
"""Exact complete-EFX CEGAR for a parameterized fixed cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import defaultdict
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json, has_universal_min
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from anneal import atomic_json, has_universal_min
    from lra_master import ParkabilityLRAMaster


def shape(assignment: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            (assignment.count(agent) for agent in range(n)),
            reverse=True,
        )
    )


def select_diverse(
    assignments: list[tuple[int, ...]],
    n: int,
    limit: int,
) -> list[tuple[int, ...]]:
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for assignment in assignments:
        buckets[shape(assignment, n)].append(assignment)
    selected = []
    offset = 0
    ordered = sorted(buckets)
    while len(selected) < min(limit, len(assignments)):
        for allocation_shape in ordered:
            bucket = buckets[allocation_shape]
            if offset < len(bucket):
                selected.append(bucket[offset])
                if len(selected) == min(limit, len(assignments)):
                    break
        offset += 1
    return selected


def pool_document(
    n: int,
    m: int,
    allocations: list[tuple[int, ...]],
) -> dict:
    return {
        "schema": "generic-complete-efx-lra-pool-v1",
        "n": n,
        "m": m,
        "allocations": [list(assignment) for assignment in allocations],
    }


def load_pool(path: Path, n: int, m: int) -> list[tuple[int, ...]]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    if (
        raw.get("schema") != "generic-complete-efx-lra-pool-v1"
        or raw.get("n") != n
        or raw.get("m") != m
        or not isinstance(raw.get("allocations"), list)
    ):
        raise ValueError("pool metadata does not match the requested cell")
    allocations = [tuple(item) for item in raw["allocations"]]
    if len(allocations) != len(set(allocations)):
        raise ValueError("pool contains duplicate allocations")
    for allocation in allocations:
        if len(allocation) != m or any(
            type(owner) is not int or not 0 <= owner < n
            for owner in allocation
        ):
            raise ValueError("pool contains an invalid allocation")
    return allocations


def run(
    *,
    n: int,
    m: int,
    seed_paths: list[Path],
    pool_path: Path,
    result_path: Path,
    trace_path: Path,
    smt2_path: Path,
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
    symmetry: str,
    exclude_universal_min: bool,
    exclude_peelable: bool,
) -> dict:
    pool = load_pool(pool_path, n, m)
    pool_set = set(pool)
    for seed_path in seed_paths:
        raw = json.loads(seed_path.read_text())
        values = core.validate_values(
            raw["values"],
            expected_n=n,
            expected_m=m,
            lower=1,
        )
        for assignment in core.iter_efx0_assignments(values):
            if assignment not in pool_set:
                pool.append(assignment)
                pool_set.add(assignment)
    atomic_json(pool_path, pool_document(n, m, pool))

    master = ParkabilityLRAMaster(
        n,
        m,
        exclude_universal_min=exclude_universal_min,
        exclude_peelable=exclude_peelable,
        symmetry=symmetry,
    )
    for assignment in pool:
        master.add_complete_allocation(assignment)

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
        assignments = list(core.iter_efx0_assignments(values))
        survivors = [
            assignment
            for assignment in assignments
            if assignment not in pool_set
        ]
        if len(survivors) != len(assignments):
            raise AssertionError("model satisfies a pooled EFX allocation")
        counts = defaultdict(int)
        for assignment in assignments:
            counts["".join(map(str, shape(assignment, n)))] += 1
        record = {
            "iteration": iteration,
            "pool_size_before": len(pool),
            "complete_efx_count": len(assignments),
            "complete_efx_count_by_shape": dict(sorted(counts.items())),
            "values": [list(row) for row in values],
        }
        trace.append(record)
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"complete_efx={len(assignments)}",
            flush=True,
        )
        if not assignments:
            literal_count = independent.count_complete_efx0(values)
            if literal_count:
                raise AssertionError("independent verifier rejected zero EFX")
            status = "ZERO_COMPLETE_EFX"
            result_values = values
            break
        selected = select_diverse(survivors, n, add_per_iteration)
        for assignment in selected:
            master.add_complete_allocation(assignment)
            pool.append(assignment)
            pool_set.add(assignment)
        atomic_json(pool_path, pool_document(n, m, pool))

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": "generic-complete-efx-lra-result-v1",
        "status": status,
        "n": n,
        "m": m,
        "domain": "strictly_positive_reals_normalized_per_row",
        "symmetry": symmetry,
        "exclude_universal_min": exclude_universal_min,
        "exclude_peelable": exclude_peelable,
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
    atomic_json(trace_path, {"trace": trace})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=9)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--add", type=int, default=4096)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=900)
    parser.add_argument(
        "--symmetry",
        choices=("none", "double_lex"),
        default="none",
    )
    parser.add_argument("--exclude-universal-min", action="store_true")
    parser.add_argument("--exclude-peelable", action="store_true")
    args = parser.parse_args()
    if (
        args.n < 2
        or args.m < 1
        or args.add < 1
        or args.max_iterations < 1
        or args.time_limit < 0
    ):
        parser.error("invalid cell or search limits")
    result = run(
        n=args.n,
        m=args.m,
        seed_paths=args.seed,
        pool_path=args.pool,
        result_path=args.result,
        trace_path=args.trace,
        smt2_path=args.smt2,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        symmetry=args.symmetry,
        exclude_universal_min=args.exclude_universal_min,
        exclude_peelable=args.exclude_peelable,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
