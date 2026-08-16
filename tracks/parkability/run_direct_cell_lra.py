#!/usr/bin/env python3
"""One-shot direct-allocation LRA solve for a strict ranking cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import z3

try:
    from . import independent
    from .lra_master import ParkabilityLRAMaster
    from .run_efx_lra_cegar import load_allocation_import
    from .run_lra_cegar import atomic_json, atomic_write, canonical_sha256
except ImportError:
    import independent
    from lra_master import ParkabilityLRAMaster
    from run_efx_lra_cegar import load_allocation_import
    from run_lra_cegar import atomic_json, atomic_write, canonical_sha256


SCHEMA = "direct-ranking-cell-lra-result-v1"
N = 4
M = 8


def run(
    *,
    pool_path: Path,
    favorite_pattern: tuple[int, ...],
    second_favorite_pattern: tuple[int, ...] | None,
    pattern_stabilizer: bool,
    time_limit_s: float,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if (
        len(favorite_pattern) != N
        or any(not 0 <= good < M for good in favorite_pattern)
        or time_limit_s < 0
        or result_path.exists()
        or smt2_path.exists()
        or result_path.resolve() == smt2_path.resolve()
    ):
        raise ValueError("invalid pattern, timeout, or output paths")
    assignments = load_allocation_import(pool_path)
    if len(assignments) != 40_824:
        raise ValueError("direct terminal cell requires all 40,824 onto allocations")
    started = time.time()
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
    )
    if second_favorite_pattern is None:
        master.add_strict_favorite_pattern(favorite_pattern)
        if pattern_stabilizer:
            master.add_favorite_pattern_stabilizer(favorite_pattern)
        ranking_prefixes = None
    else:
        if (
            len(second_favorite_pattern) != N
            or any(not 0 <= good < M for good in second_favorite_pattern)
            or any(
                first == second
                for first, second in zip(
                    favorite_pattern,
                    second_favorite_pattern,
                )
            )
        ):
            raise ValueError("invalid second-favorite pattern")
        ranking_prefixes = tuple(
            zip(favorite_pattern, second_favorite_pattern)
        )
        master.add_strict_ranking_prefixes(ranking_prefixes)
        if pattern_stabilizer:
            master.add_ranking_prefix_stabilizer(ranking_prefixes)
    for assignment in assignments:
        master.add_complete_allocation(assignment)
    build_seconds = time.time() - started
    solve_started = time.time()
    solved = master.solve(time_limit_s=time_limit_s)
    solve_seconds = time.time() - solve_started
    atomic_write(smt2_path, master.to_smt2())
    status = (
        "UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "MASTER_UNKNOWN"
        if solved.status == "UNKNOWN"
        else "SAT_CANDIDATE"
    )
    extra = {}
    if solved.status == "SAT":
        assert solved.values is not None
        exact_count = independent.count_complete_efx0(solved.values)
        extra = {
            "values": [list(row) for row in solved.values],
            "values_sha256": canonical_sha256(solved.values),
            "independent_complete_efx0_count": exact_count,
        }
        if exact_count == 0:
            status = "ZERO_COMPLETE_EFX0"
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": "independent direct-allocation encoding; proof check required",
        "n": N,
        "m": M,
        "favorite_pattern": list(favorite_pattern),
        "second_favorite_pattern": (
            list(second_favorite_pattern)
            if second_favorite_pattern is not None
            else None
        ),
        "pattern_stabilizer": pattern_stabilizer,
        "allocation_count": len(assignments),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "formula_build_seconds": round(build_seconds, 6),
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
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--favorite-pattern", required=True)
    parser.add_argument("--second-favorite-pattern")
    parser.add_argument("--pattern-stabilizer", action="store_true")
    parser.add_argument("--time-limit", type=float, default=7200)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        pool_path=args.pool,
        favorite_pattern=tuple(map(int, args.favorite_pattern.split(","))),
        second_favorite_pattern=(
            tuple(map(int, args.second_favorite_pattern.split(",")))
            if args.second_favorite_pattern is not None
            else None
        ),
        pattern_stabilizer=args.pattern_stabilizer,
        time_limit_s=args.time_limit,
        result_path=args.result,
        smt2_path=args.smt2,
    )


if __name__ == "__main__":
    main()
