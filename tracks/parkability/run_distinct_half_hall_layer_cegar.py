#!/usr/bin/env python3
"""CEGAR for bounded Hall-witness layers in the distinct-half EFX gate."""

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
    from .decide_distinct_half_hall_layers import (
        M,
        N,
        add_branch,
        hall_witnesses,
        minimum_hall_witness_size,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_universal_threshold_balanced_cegar import audit_threshold_failure
except ImportError:
    import core
    from anneal import atomic_json
    from decide_distinct_half_hall_layers import (
        M,
        N,
        add_branch,
        hall_witnesses,
        minimum_hall_witness_size,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_universal_threshold_balanced_cegar import audit_threshold_failure


SCHEMA = "distinct-half-hall-layer-cegar-result-v1"


def run(
    result_path,
    smt2_path,
    maximum_size,
    time_limit,
    add_per_iteration,
    max_iterations,
    rank_branch,
):
    universe = favorite_pair_balanced_universe()
    master = ParkabilityLRAMaster(N, M)
    add_branch(master, rank_branch)
    pool = set()
    trace = []
    status = "ITERATION_LIMIT"
    reason_unknown = None
    solver_status = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
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
        audit_threshold_failure(values)
        survivors = tuple(
            partition
            for partition in universe
            if partition not in pool
            and (
                minimum_hall_witness_size(values, partition) is None
                or minimum_hall_witness_size(values, partition) > maximum_size
            )
        )
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(pool),
            "surviving_partition_count": len(survivors),
            "values": [list(row) for row in values],
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "ZERO_LAYER_ESCAPE"
            break
        for partition in survivors[:add_per_iteration]:
            master.solver.add(
                z3.Or(
                    *hall_witnesses(master, partition, maximum_size)
                )
            )
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
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "rank_disjunct_branch": rank_branch,
        "maximum_allowed_hall_witness_size": maximum_size,
        "target_partition_count": len(universe),
        "pool_size": len(pool),
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE means some favorite-pair balanced partition "
            "escapes every Hall witness up to the stated size. Only size "
            "four is the full EFX target."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--maximum-size", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--add", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--rank-branch")
    args = parser.parse_args()
    if (
        args.time_limit < 0
        or args.add < 1
        or args.max_iterations < 1
        or (
            args.rank_branch is not None
            and (
                len(args.rank_branch) != N
                or set(args.rank_branch) - {"B", "C"}
            )
        )
    ):
        parser.error("invalid search parameters")
    result = run(
        args.result,
        args.smt2,
        args.maximum_size,
        args.time_limit,
        args.add,
        args.max_iterations,
        args.rank_branch,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
