#!/usr/bin/env python3
"""Extract a guarded partition core for a bottom-pattern conversion lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import (
        add_pattern_symmetry,
        conversion_closure,
        pattern_conversion_orbits,
        reconstruct_cegar_pool,
    )
    from .decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from .lra_master import ParkabilityLRAMaster
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
    from .run_distinct_half_full_cell_cegar import add_no_full_hall_cell
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
    )
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import (
        add_pattern_symmetry,
        conversion_closure,
        pattern_conversion_orbits,
        reconstruct_cegar_pool,
    )
    from decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from lra_master import ParkabilityLRAMaster
    from run_bottom_pair_pattern_selector_cegar import goods_pattern
    from run_distinct_half_full_cell_cegar import add_no_full_hall_cell
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
    )


SCHEMA = "bottom-pattern-conversion-core-lra-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_base(pattern_index, symmetry_breaking, threshold_encoding):
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    if threshold_encoding == "sorting":
        add_universal_threshold_failure(master)
    elif threshold_encoding == "cardinal":
        add_universal_threshold_failure_cardinal(master)
    else:
        raise ValueError("unknown threshold encoding")
    for agent, lows in enumerate(pattern):
        add_bottom_orders(master, lows, (agent,))
    symmetry_encoding = add_pattern_symmetry(
        master, pattern_index, symmetry_breaking
    )
    selected_cell_encoding = add_no_full_hall_cell(
        master, low_pairs=selected_pairs
    )
    return (
        master,
        selected_pairs,
        selected_cell_encoding,
        symmetry_encoding,
    )


def run(
    source_path,
    result_path,
    formula_path,
    time_limit,
    minimize_core,
    threshold_encoding,
):
    if result_path.exists() or formula_path.exists():
        raise ValueError("new output paths are required")
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != "bottom-pattern-conversion-selector-lra-v1"
        or source.get("status") != "UNSAT_CANDIDATE"
    ):
        raise ValueError("source is not an UNSAT conversion candidate")
    pattern_index = source["pattern_index"]
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    conversion_family, _ = conversion_closure(selected_pairs)
    conversion_orbit = source.get("conversion_orbit")
    if conversion_orbit is not None:
        conversion_family = pattern_conversion_orbits(
            pattern, conversion_family
        )[conversion_orbit]
    pool = (
        tuple(sorted(reconstruct_cegar_pool(source, conversion_family)))
        if source.get("cegar")
        else tuple(sorted(conversion_family))
    )
    symmetry_breaking = source.get("symmetry_breaking", "none")

    master, _, selected_cell_encoding, symmetry_encoding = build_base(
        pattern_index, symmetry_breaking, threshold_encoding
    )
    guards = []
    partition_by_guard = {}
    for position, partition in enumerate(pool):
        guard = z3.Bool(f"core_partition_{position}")
        master.add_partition_obstruction(partition, activation=guard)
        guards.append(guard)
        partition_by_guard[str(guard)] = partition
    master.solver.set(timeout=round(time_limit * 1000), unsat_core=True)
    if minimize_core:
        master.solver.set("core.minimize", True)
    started = time.time()
    status = master.solver.check(*guards)
    assumption_seconds = time.time() - started
    core = ()
    if status == z3.unsat:
        core = tuple(
            partition_by_guard[str(guard)]
            for guard in master.solver.unsat_core()
        )

    replay, _, _, _ = build_base(
        pattern_index, symmetry_breaking, threshold_encoding
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
            "CORE_UNSAT_CANDIDATE"
            if replay_result is not None and replay_result.status == "UNSAT"
            else "ASSUMPTION_UNKNOWN"
            if status == z3.unknown
            else "CORE_REPLAY_"
            + (replay_result.status if replay_result is not None else str(status))
        ),
        "solver_status": str(status),
        "reason_unknown": (
            master.solver.reason_unknown() if status == z3.unknown else None
        ),
        "replay_solver_status": (
            replay_result.raw_status if replay_result is not None else None
        ),
        "replay_reason_unknown": (
            replay_result.reason_unknown if replay_result is not None else None
        ),
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "selected_cell_encoding": selected_cell_encoding,
        "symmetry_breaking": symmetry_breaking,
        "symmetry_encoding": symmetry_encoding,
        "conversion_orbit": conversion_orbit,
        "universal_threshold_encoding": threshold_encoding,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "pool_size": len(pool),
        "core_size": len(core),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in core
        ],
        "core_minimization": minimize_core,
        "assumption_solve_seconds": assumption_seconds,
        "replay_solve_seconds": replay_seconds,
        "time_limit_seconds_per_solve": time_limit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "A proof-checked UNSAT replay establishes only the conditional "
            "bottom-pattern conversion lemma represented by this formula."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--minimize-core", action="store_true")
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="sorting",
    )
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    run(
        args.source,
        args.result,
        args.formula,
        args.time_limit,
        args.minimize_core,
        args.threshold_encoding,
    )


if __name__ == "__main__":
    main()
