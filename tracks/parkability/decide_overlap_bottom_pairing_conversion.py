#!/usr/bin/env python3
"""Test a one-cell conversion lemma in the overlapping 2+2 bottom pattern."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        MATCHING,
        RESIDUAL,
        conversion_partitions,
    )
    from .decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
        pairing_has_hall_matching,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    from anneal import atomic_json
    from decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        MATCHING,
        RESIDUAL,
        conversion_partitions,
    )
    from decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
        pairing_has_hall_matching,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "overlap-bottom-pairing-conversion-lra-v1"
N = 4
M = 9
PRIMARY_AGENTS = (0, 1)
OUTSIDE_AGENTS = (2, 3)
PRIMARY_SPECIFIC = 7
SHARED_LOW = 8
OUTSIDE_SPECIFIC = 6
OUTSIDE_LOWS = (OUTSIDE_SPECIFIC, SHARED_LOW)
CORE = (1, 2, 3, 4, 5)


def run(result_path, formula_path, time_limit, orient_shared_low):
    conversions = conversion_partitions()
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure_cardinal(master)
    add_bottom_orders(master, LOWS, PRIMARY_AGENTS)
    add_bottom_orders(master, OUTSIDE_LOWS, OUTSIDE_AGENTS)
    for agent in OUTSIDE_AGENTS:
        for good in CORE:
            master.solver.add(
                master.values[agent][PRIMARY_SPECIFIC]
                <= master.values[agent][good]
            )
        if orient_shared_low:
            master.solver.add(
                master.values[agent][SHARED_LOW]
                <= master.values[agent][OUTSIDE_SPECIFIC]
            )

    accept = add_acceptance_literals(master, LOWS, RESIDUAL)
    master.solver.add(hall_failure(accept, MATCHING))
    for partition in conversions:
        master.add_partition_obstruction(partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    values = solved.values
    if values is not None:
        audit_threshold_failure(values)
        for lows, agents in (
            (LOWS, PRIMARY_AGENTS),
            (OUTSIDE_LOWS, OUTSIDE_AGENTS),
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
                raise AssertionError("model lost an overlap bottom order")
        if any(
            values[agent][PRIMARY_SPECIFIC] > values[agent][good]
            for agent in OUTSIDE_AGENTS
            for good in CORE
        ):
            raise AssertionError("model lost a near-common core order")
        if orient_shared_low and any(
            values[agent][SHARED_LOW]
            > values[agent][OUTSIDE_SPECIFIC]
            for agent in OUTSIDE_AGENTS
        ):
            raise AssertionError("model lost the shared-low orientation")
        if pairing_has_hall_matching(values, LOWS, MATCHING):
            raise AssertionError("model lost its Hall failure")
        if supported_partitions(values, list(conversions)):
            raise AssertionError("model gained a local conversion")

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "CONVERSION_COUNTEREXAMPLE"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "primary_bottom_pair": list(LOWS),
        "primary_bottom_agents": list(PRIMARY_AGENTS),
        "outside_bottom_pair": list(OUTSIDE_LOWS),
        "outside_bottom_agents": list(OUTSIDE_AGENTS),
        "near_common_core_goods": list(CORE),
        "shared_low_orientation_required": orient_shared_low,
        "fixed_residual_matching": [list(edge) for edge in MATCHING],
        "conversion_partition_count": len(conversions),
        "values": [list(row) for row in values] if values else None,
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds": time_limit,
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "This tests a local six-conversion lemma in a near-common "
            "subbranch of the overlapping 2+2 pattern. Even UNSAT does not "
            "prove that the near-common orders are globally forced."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--orient-shared-low", action="store_true")
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    print(
        json.dumps(
            run(
                args.result,
                args.formula,
                args.time_limit,
                args.orient_shared_low,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
