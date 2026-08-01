#!/usr/bin/env python3
"""CEGAR for the conditional two-bottom-pair Hall selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from . import core, independent
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
        favorite_pair_universe,
        hall_failure,
        pairing_has_hall_matching,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    import core
    import independent
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
        favorite_pair_universe,
        hall_failure,
        pairing_has_hall_matching,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "two-pair-bottom-cross-cegar-v1"
N = 4
M = 9
FAVORITE = 0


def target_universe(pattern, second_lows, partition_family):
    universe = tuple(favorite_pair_universe("all"))
    if partition_family == "all":
        return universe
    if partition_family not in ("shared_low_triple", "shared_low_active"):
        raise ValueError("unknown cross-pair partition family")
    shared = set(FIRST_LOWS).intersection(second_lows)
    if pattern != "overlap" or len(shared) != 1:
        raise ValueError("the shared-low-triple family requires overlap")
    shared_good = next(iter(shared))
    return tuple(
        partition
        for partition in universe
        if any(
            (
                len(bundle) == 3
                or (
                    partition_family == "shared_low_active"
                    and FAVORITE in bundle
                )
            )
            and shared_good in bundle
            for bundle in partition
        )
    )


def reconstruct_trace_pool(resumed, universe, initial_pool):
    pool = set(initial_pool)
    prior_add = resumed["add_per_iteration"]
    for record in resumed.get("trace", []):
        values = core.validate_values(
            record["values"], expected_n=N, expected_m=M, lower=1
        )
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if len(survivors) != record["favorite_pair_efx_survivors"]:
            raise AssertionError("resume trace survivor count changed")
        pool.update(survivors[:prior_add])
    if len(pool) != resumed["pool_size"]:
        raise AssertionError("resume pool reconstruction changed")
    return pool


def run(
    result_path: Path,
    formula_path: Path,
    pattern: str,
    orbit_index: int,
    time_limit: float,
    max_iterations: int,
    add_per_iteration: int,
    seed_paths: tuple[Path, ...] = (),
    partition_family: str = "all",
    resume_path: Path | None = None,
    threshold_encoding: str = "cardinal",
):
    (
        first_matching,
        second_lows,
        second_agents,
        second_matching,
        orbit_count,
    ) = cells(pattern, orbit_index)
    first_residual = tuple(
        good for good in range(1, M) if good not in FIRST_LOWS
    )
    second_residual = tuple(
        good for good in range(1, M) if good not in second_lows
    )
    all_local_conversions = tuple(
        dict.fromkeys(
            (
                *conversions(FIRST_LOWS, first_matching),
                *conversions(second_lows, second_matching),
            )
        )
    )
    universe = target_universe(pattern, second_lows, partition_family)
    universe_set = set(universe)
    local_conversions = tuple(
        partition
        for partition in all_local_conversions
        if partition in universe_set
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
    first_accept = add_acceptance_literals(
        master, FIRST_LOWS, first_residual
    )
    second_accept = add_acceptance_literals(
        master, second_lows, second_residual
    )
    master.solver.add(hall_failure(first_accept, first_matching))
    master.solver.add(hall_failure(second_accept, second_matching))

    pool = set(local_conversions)
    resume_source = None
    if resume_path is not None:
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("pattern") != pattern
            or resumed.get("matching_orbit_index") != orbit_index
            or resumed.get("partition_family", "all") != partition_family
            or resumed.get("seed_sources")
        ):
            raise ValueError("incompatible or seeded cross-CEGAR resume")
        pool = reconstruct_trace_pool(resumed, universe, pool)
        resume_source = {
            "path": str(resume_path),
            "sha256": hashlib.sha256(resume_path.read_bytes()).hexdigest(),
            "reconstructed_pool_size": len(pool),
        }
    seed_sources = []
    for seed_path in seed_paths:
        payload = json.loads(seed_path.read_text())
        values = core.validate_values(
            payload["values"], expected_n=N, expected_m=M, lower=1
        )
        pool.update(supported_partitions(values, list(universe)))
        seed_sources.append(
            {
                "path": str(seed_path),
                "sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
            }
        )
    for partition in sorted(pool):
        master.add_partition_obstruction(partition)

    trace = []
    status = "ITERATION_LIMIT"
    raw_status = None
    reason_unknown = None
    terminal_values = None
    started = time.time()
    iteration = 0
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
        raw_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break

        values = core.validate_values(
            solved.values, expected_n=N, expected_m=M, lower=1
        )
        audit_threshold_failure(values)
        for lows, agents in (
            (FIRST_LOWS, FIRST_AGENTS),
            (second_lows, second_agents),
        ):
            residual = tuple(
                good for good in range(1, M) if good not in lows
            )
            if any(
                values[agent][low] > values[agent][good]
                for agent in agents
                for low in lows
                for good in residual
            ):
                raise AssertionError("model lost a bottom-order condition")
        if pairing_has_hall_matching(values, FIRST_LOWS, first_matching):
            raise AssertionError("first matching is no longer Hall-failed")
        if pairing_has_hall_matching(values, second_lows, second_matching):
            raise AssertionError("second matching is no longer Hall-failed")

        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "favorite_pair_efx_survivors": len(survivors),
                "values": [list(row) for row in values],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "TWO_CELL_SELECTOR_COUNTEREXAMPLE"
            terminal_values = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            pool.add(partition)

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": raw_status,
        "reason_unknown": reason_unknown,
        "pattern": pattern,
        "matching_orbit_index": orbit_index,
        "matching_orbit_count": orbit_count,
        "first_cell": {
            "bottom_pair": list(FIRST_LOWS),
            "bottom_agents": list(FIRST_AGENTS),
            "matching": [list(edge) for edge in first_matching],
        },
        "second_cell": {
            "bottom_pair": list(second_lows),
            "bottom_agents": list(second_agents),
            "matching": [list(edge) for edge in second_matching],
        },
        "favorite_pair_partition_count": len(universe),
        "partition_family": partition_family,
        "threshold_encoding": threshold_encoding,
        "initial_local_conversion_count": len(local_conversions),
        "seed_sources": seed_sources,
        "resume_source": resume_source,
        "seeded_pool_size": len(pool) if not trace else trace[0]["pool_size_before"],
        "pool_size": len(pool),
        "add_per_iteration": add_per_iteration,
        "max_iterations": max_iterations,
        "iterations": iteration,
        "time_limit_seconds_per_solve": time_limit,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in terminal_values]
            if terminal_values is not None
            else None
        ),
        "literal_complete_efx_count": (
            independent.count_complete_efx0(terminal_values)
            if terminal_values is not None
            else None
        ),
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT in every relative matching orbit would establish the "
            "conditional two-cell selector only after independent replay. "
            "A terminal SAT model would refute that selector, not complete "
            "EFX."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--pattern", choices=("disjoint", "overlap"), required=True)
    parser.add_argument("--orbit-index", type=int, default=0)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--add", type=int, default=32)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="cardinal",
    )
    parser.add_argument(
        "--partition-family",
        choices=("all", "shared_low_triple", "shared_low_active"),
        default="all",
    )
    args = parser.parse_args()
    if (
        args.time_limit <= 0
        or args.max_iterations < 1
        or args.add < 1
    ):
        parser.error("invalid search limits")
    result = run(
        args.result,
        args.formula,
        args.pattern,
        args.orbit_index,
        args.time_limit,
        args.max_iterations,
        args.add,
        tuple(args.seed),
        args.partition_family,
        args.resume,
        args.threshold_encoding,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
