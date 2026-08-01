#!/usr/bin/env python3
"""Test whether a canonical owner-floor state forces balanced EFX."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import balanced_state_universe
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import balanced_state_universe
    from lra_master import ParkabilityLRAMaster


SCHEMA = "floor-to-balanced-efx-lra-result-v1"
N = 4
M = 9
FAVORITE = 0
CANONICAL_ALLOCATION = (
    (1, 2, 3),
    (0, 4),
    (5, 6),
    (7, 8),
)


def supported_efx_partitions(values, universe):
    return tuple(
        partition
        for partition in universe
        if matching_rank(feasible_graph(values, partition)) == N
    )


def add_assumptions(master: ParkabilityLRAMaster) -> None:
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    for agent, bundle in enumerate(CANONICAL_ALLOCATION):
        master.solver.add(
            master._sum(agent, bundle) >= master.values[agent][FAVORITE]
        )


def audit(values) -> None:
    for agent, row in enumerate(values):
        if any(row[FAVORITE] <= row[good] for good in range(1, M)):
            raise AssertionError("strict common favorite was lost")
        if (
            sum(row[good] for good in CANONICAL_ALLOCATION[agent])
            < row[FAVORITE]
        ):
            raise AssertionError("canonical owner-floor state was lost")


def run(
    *,
    result_path: Path,
    smt2_path: Path,
    time_limit_s: float,
    add_per_iteration: int,
    max_iterations: int,
) -> dict:
    universe = balanced_state_universe()
    master = ParkabilityLRAMaster(N, M)
    add_assumptions(master)
    pool = set()
    trace = []
    status = "ITERATION_LIMIT"
    solver_status = None
    reason_unknown = None
    result_values = None
    started = time.time()
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
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        audit(values)
        survivors = tuple(
            partition
            for partition in supported_efx_partitions(values, universe)
            if partition not in pool
        )
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
            status = "ZERO_BALANCED_EFX"
            result_values = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            pool.add(partition)

    formula = master.to_smt2()
    smt2_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solver_status,
        "reason_unknown": reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "strict_common_favorite": FAVORITE,
        "canonical_owner_floor_allocation": [
            list(bundle) for bundle in CANONICAL_ALLOCATION
        ],
        "target_partition_count": len(universe),
        "pool_size": len(pool),
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "ZERO_BALANCED_EFX refutes the proposed implication from one "
            "balanced owner-floor allocation to a balanced EFX allocation. "
            "UNSAT_CANDIDATE would require independent replay before being "
            "treated as a computer-assisted theorem."
        ),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--add", type=int, default=128)
    parser.add_argument("--max-iterations", type=int, default=20)
    args = parser.parse_args()
    if args.time_limit < 0 or args.add < 1 or args.max_iterations < 1:
        parser.error("invalid search limits")
    result = run(
        result_path=args.result,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
