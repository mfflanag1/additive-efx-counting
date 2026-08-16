#!/usr/bin/env python3
"""Extract small repair cores in all disjoint failed-matching orbits."""

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
        add_bottom_orders,
        cells,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
    from .run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
    )
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
    )
except ImportError:
    from anneal import atomic_json
    from decide_two_pair_bottom_cross_conversion import (
        add_bottom_orders,
        cells,
    )
    from lra_master import ParkabilityLRAMaster
    from run_bottom_pair_pattern_selector_cegar import goods_pattern
    from run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
    )
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
    )


SCHEMA = "disjoint-conversion-matching-orbit-cores-v1"
N = 4
M = 9
FAVORITE = 0
PATTERN_INDEX = 6
FIRST_LOWS = (1, 2)
SECOND_LOWS = (3, 4)
RELABEL = {0: 0, 7: 1, 8: 2, 5: 3, 6: 4, 1: 5, 2: 6, 3: 7, 4: 8}


def decode(raw):
    return tuple(tuple(bundle) for bundle in raw)


def relabel_matching(matching):
    return tuple(
        sorted(tuple(sorted((RELABEL[left], RELABEL[right]))) for left, right in matching)
    )


def build_base(first_matching, second_matching):
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure(master)
    pattern = goods_pattern(PATTERN_INDEX)
    for agent, lows in enumerate(pattern):
        add_bottom_orders(master, lows, (agent,))
    first_residual = tuple(
        good for good in range(1, M) if good not in FIRST_LOWS
    )
    second_residual = tuple(
        good for good in range(1, M) if good not in SECOND_LOWS
    )
    first_accept = add_acceptance_literals(
        master, FIRST_LOWS, first_residual
    )
    second_accept = add_acceptance_literals(
        master, SECOND_LOWS, second_residual
    )
    master.solver.add(hall_failure(first_accept, first_matching))
    master.solver.add(hall_failure(second_accept, second_matching))
    return master


def run(source, output, formula_prefix, time_limit, minimize_core, direct):
    payload = json.loads(source.read_text())
    if (
        payload.get("schema") != "bottom-pattern-conversion-core-lra-v1"
        or payload.get("status") != "CORE_UNSAT_CANDIDATE"
        or payload.get("pattern_index") != PATTERN_INDEX
    ):
        raise ValueError("source is not the disjoint conversion core")
    partitions = tuple(map(decode, payload["core_partitions"]))
    if len(partitions) != len(set(partitions)):
        raise AssertionError("duplicate source partitions")

    orbit_records = []
    for orbit_index in range(9):
        old_first, _, _, old_second, orbit_count = cells(
            "disjoint", orbit_index
        )
        if orbit_count != 9:
            raise AssertionError("disjoint matching orbit census changed")
        first_matching = relabel_matching(old_first)
        second_matching = relabel_matching(old_second)
        master = build_base(first_matching, second_matching)
        guards = []
        by_guard = {}
        for position, partition in enumerate(partitions):
            guard = z3.Bool(f"orbit_{orbit_index}_partition_{position}")
            master.add_partition_obstruction(partition, activation=guard)
            guards.append(guard)
            by_guard[str(guard)] = partition
        status = None
        assumption_seconds = 0.0
        core = ()
        if not direct:
            master.solver.set(timeout=round(time_limit * 1000), unsat_core=True)
            if minimize_core:
                master.solver.set("core.minimize", True)
            started = time.time()
            status = master.solver.check(*guards)
            assumption_seconds = time.time() - started
            if status == z3.unsat:
                core = tuple(
                    by_guard[str(guard)] for guard in master.solver.unsat_core()
                )

        replay_pool = core if core else partitions
        replay = build_base(first_matching, second_matching)
        for partition in replay_pool:
            replay.add_partition_obstruction(partition)
        replay_result = replay.solve(time_limit_s=time_limit)
        formula = replay.to_smt2()
        formula_path = Path(f"{formula_prefix}{orbit_index}.smt2")
        if formula_path.exists():
            raise ValueError(f"new formula path required: {formula_path}")
        formula_path.parent.mkdir(parents=True, exist_ok=True)
        formula_path.write_text(formula)
        orbit_records.append(
            {
                "orbit_index": orbit_index,
                "first_matching": [list(edge) for edge in first_matching],
                "second_matching": [list(edge) for edge in second_matching],
                "solver_status": str(status) if status is not None else "not_run",
                "reason_unknown": (
                    master.solver.reason_unknown() if status == z3.unknown else None
                ),
                "replay_status": (
                    replay_result.status
                ),
                "extracted_core_size": len(core),
                "replay_partition_count": len(replay_pool),
                "core_partitions": [
                    [list(bundle) for bundle in partition] for partition in core
                ],
                "assumption_solve_seconds": assumption_seconds,
                "formula": str(formula_path),
                "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
            }
        )
        if replay_result.status != "UNSAT":
            break

    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_MATCHING_ORBITS_UNSAT_CANDIDATE"
            if len(orbit_records) == 9
            and all(record["replay_status"] == "UNSAT" for record in orbit_records)
            else "INCOMPLETE"
        ),
        "source": str(source),
        "source_core_size": len(partitions),
        "matching_orbit_count": 9,
        "completed_orbit_count": len(orbit_records),
        "core_minimization": minimize_core,
        "direct_replay_only": direct,
        "time_limit_seconds_per_solve": time_limit,
        "orbits": orbit_records,
        "claim_boundary": (
            "These fixed-matching cores decompose the already established "
            "conditional disjoint conversion lemma; independent proof is "
            "still required for each replay formula."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formula-prefix", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--minimize-core", action="store_true")
    parser.add_argument("--direct", action="store_true")
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    run(
        args.source,
        args.output,
        args.formula_prefix,
        args.time_limit,
        args.minimize_core,
        args.direct,
    )


if __name__ == "__main__":
    main()
