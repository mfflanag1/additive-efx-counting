#!/usr/bin/env python3
"""Extract an assumption core from a cross-pair CEGAR UNSAT candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_two_pair_bottom_cross_conversion import (
        FIRST_AGENTS,
        FIRST_LOWS,
        add_bottom_orders,
        cells,
        conversions,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
    )
    from .run_two_pair_bottom_cross_cegar import (
        reconstruct_trace_pool,
        target_universe,
    )
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
    )
except ImportError:
    from anneal import atomic_json
    from decide_two_pair_bottom_cross_conversion import (
        FIRST_AGENTS,
        FIRST_LOWS,
        add_bottom_orders,
        cells,
        conversions,
    )
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
    )
    from run_two_pair_bottom_cross_cegar import (
        reconstruct_trace_pool,
        target_universe,
    )
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
    )


SCHEMA = "two-pair-bottom-cross-assumption-core-v1"
N = 4
M = 9
FAVORITE = 0


def build_base(pattern, orbit_index, threshold_encoding):
    first_matching, second_lows, second_agents, second_matching, orbit_count = (
        cells(pattern, orbit_index)
    )
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    if threshold_encoding == "cardinal":
        add_universal_threshold_failure_cardinal(master)
    elif threshold_encoding == "sorting":
        add_universal_threshold_failure(master)
    else:
        raise ValueError("unknown threshold encoding")
    add_bottom_orders(master, FIRST_LOWS, FIRST_AGENTS)
    add_bottom_orders(master, second_lows, second_agents)
    first_residual = tuple(
        good for good in range(1, M) if good not in FIRST_LOWS
    )
    second_residual = tuple(
        good for good in range(1, M) if good not in second_lows
    )
    first_accept = add_acceptance_literals(
        master, FIRST_LOWS, first_residual
    )
    second_accept = add_acceptance_literals(
        master, second_lows, second_residual
    )
    master.solver.add(hall_failure(first_accept, first_matching))
    master.solver.add(hall_failure(second_accept, second_matching))
    return (
        master,
        first_matching,
        second_lows,
        second_matching,
        orbit_count,
    )


def run(
    source_path: Path,
    result_path: Path,
    formula_path: Path,
    time_limit: float,
):
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    if source.get("status") != "UNSAT_CANDIDATE" or source.get("seed_sources"):
        raise ValueError("source must be an unseeded UNSAT CEGAR candidate")
    pattern = source["pattern"]
    orbit_index = source["matching_orbit_index"]
    partition_family = source.get("partition_family", "all")
    threshold_encoding = source.get("threshold_encoding", "cardinal")
    (
        master,
        first_matching,
        second_lows,
        second_matching,
        orbit_count,
    ) = build_base(pattern, orbit_index, threshold_encoding)
    universe = target_universe(pattern, second_lows, partition_family)
    local_conversions = tuple(
        dict.fromkeys(
            (
                *conversions(FIRST_LOWS, first_matching),
                *conversions(second_lows, second_matching),
            )
        )
    )
    universe_set = set(universe)
    initial_pool = tuple(
        partition
        for partition in local_conversions
        if partition in universe_set
    )
    pool = tuple(
        sorted(reconstruct_trace_pool(source, universe, initial_pool))
    )

    activations = []
    activation_to_partition = {}
    for index, partition in enumerate(pool):
        activation = z3.Bool(f"cross_core_activation_{index}")
        master.add_partition_obstruction(partition, activation=activation)
        activations.append(activation)
        activation_to_partition[activation.decl().name()] = partition
    master.solver.set(timeout=round(time_limit * 1000), unsat_core=True)
    started = time.time()
    assumption_status = master.solver.check(*activations)
    assumption_seconds = time.time() - started
    core = (
        tuple(
            activation_to_partition[item.decl().name()]
            for item in master.solver.unsat_core()
        )
        if assumption_status == z3.unsat
        else ()
    )

    replay, _, _, _, _ = build_base(
        pattern, orbit_index, threshold_encoding
    )
    for partition in core:
        replay.add_partition_obstruction(partition)
    replay_started = time.time()
    replay_result = (
        replay.solve(time_limit_s=time_limit) if core else None
    )
    replay_seconds = time.time() - replay_started
    formula = replay.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "CORE_REPLAY_UNSAT"
            if replay_result is not None and replay_result.status == "UNSAT"
            else "CORE_CANDIDATE"
            if core
            else "ASSUMPTION_UNKNOWN"
        ),
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "pattern": pattern,
        "matching_orbit_index": orbit_index,
        "matching_orbit_count": orbit_count,
        "partition_family": partition_family,
        "threshold_encoding": threshold_encoding,
        "pool_size": len(pool),
        "assumption_status": str(assumption_status),
        "assumption_seconds": assumption_seconds,
        "core_size": len(core),
        "core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in core
        ],
        "replay_status": (
            replay_result.raw_status if replay_result is not None else None
        ),
        "replay_reason_unknown": (
            replay_result.reason_unknown if replay_result is not None else None
        ),
        "replay_seconds": replay_seconds,
        "time_limit_seconds_per_solve": time_limit,
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "An UNSAT replay establishes only this fixed matching orbit and "
            "still requires independent proof checking."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    print(
        json.dumps(
            run(args.source, args.result, args.formula, args.time_limit),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
