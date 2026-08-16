#!/usr/bin/env python3
"""Test coarse density consequences for the favorite-pair floor theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import (
        FAVORITE,
        M,
        N,
        REPRESENTATIVES,
        add_floor_state_obstruction,
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_universal_threshold_balanced_cegar import sorted_descending
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import (
        FAVORITE,
        M,
        N,
        REPRESENTATIVES,
        add_floor_state_obstruction,
        favorite_pair_balanced_universe,
    )
    from lra_master import ParkabilityLRAMaster
    from run_universal_threshold_balanced_cegar import sorted_descending


SCHEMA = "distinct-half-density-floor-lra-result-v1"


def at_least_k_above_fraction(master, observer, k, denominator):
    row = master.values[observer]
    favorite = row[FAVORITE]
    residual = tuple(range(1, M))
    master.solver.add(
        z3.Or(
            *(
                z3.And(
                    *(
                        denominator * row[good] > favorite
                        for good in goods
                    )
                )
                for goods in itertools.combinations(residual, k)
            )
        )
    )


def add_density_branch(
    master,
    require_three_halves,
    require_residual_total,
    require_tail_seven,
):
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    for observer, representative in enumerate(REPRESENTATIVES):
        master.solver.add(
            2 * master.values[observer][representative]
            > master.values[observer][FAVORITE]
        )
        at_least_k_above_fraction(master, observer, 5, 3)
        if require_three_halves:
            at_least_k_above_fraction(master, observer, 3, 2)
        if require_residual_total:
            master.solver.add(
                3 * master._sum(observer, tuple(range(1, M)))
                > 7 * master.values[observer][FAVORITE]
            )
        if require_tail_seven:
            ordered = sorted_descending(master.values[observer][1:])
            master.solver.add(
                ordered[4] + ordered[5] + ordered[6]
                > master.values[observer][FAVORITE]
            )


def audit(
    values,
    require_three_halves,
    require_residual_total,
    require_tail_seven,
):
    for observer, representative in enumerate(REPRESENTATIVES):
        row = values[observer]
        favorite = row[FAVORITE]
        if any(row[good] >= favorite for good in range(1, M)):
            raise AssertionError("strict favorite was lost")
        if 2 * row[representative] <= favorite:
            raise AssertionError("fixed half-favorite representative was lost")
        if sum(3 * row[good] > favorite for good in range(1, M)) < 5:
            raise AssertionError("five-above-third density was lost")
        if (
            require_three_halves
            and sum(2 * row[good] > favorite for good in range(1, M)) < 3
        ):
            raise AssertionError("three-above-half density was lost")
        if (
            require_residual_total
            and 3 * sum(row[1:]) <= 7 * favorite
        ):
            raise AssertionError("residual total density was lost")
        ordered = sorted(row[1:], reverse=True)
        if (
            require_tail_seven
            and ordered[4] + ordered[5] + ordered[6] <= favorite
        ):
            raise AssertionError("ordered tail density was lost")


def run(
    result_path,
    smt2_path,
    time_limit,
    require_three_halves,
    require_residual_total,
    require_tail_seven,
):
    universe = favorite_pair_balanced_universe()
    master = ParkabilityLRAMaster(N, M)
    add_density_branch(
        master,
        require_three_halves,
        require_residual_total,
        require_tail_seven,
    )
    for partition in universe:
        add_floor_state_obstruction(master, partition)
    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    if solved.values is not None:
        audit(
            solved.values,
            require_three_halves,
            require_residual_total,
            require_tail_seven,
        )
    formula = master.to_smt2()
    smt2_path.write_text(formula)
    status = (
        "UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "SAT_DENSITY_COUNTEREXAMPLE"
        if solved.status == "SAT"
        else "MASTER_UNKNOWN"
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "strict_common_favorite": FAVORITE,
        "fixed_half_favorite_representatives": list(REPRESENTATIVES),
        "at_least_five_residual_goods_above_one_third": True,
        "at_least_three_residual_goods_above_one_half": require_three_halves,
        "residual_total_above_seven_thirds": require_residual_total,
        "ordered_x5_x6_x7_above_favorite": require_tail_seven,
        "target_partition_count": len(universe),
        "elapsed_seconds": elapsed,
        "values": (
            [list(row) for row in solved.values]
            if solved.values is not None
            else None
        ),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE would show that the coarse stated density "
            "conditions already force a favorite-pair owner-floor state. "
            "SAT_DENSITY_COUNTEREXAMPLE refutes only that weakening."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--require-three-halves", action="store_true")
    parser.add_argument("--require-residual-total", action="store_true")
    parser.add_argument("--require-tail-seven", action="store_true")
    args = parser.parse_args()
    if args.time_limit < 0:
        parser.error("time limit cannot be negative")
    result = run(
        args.result,
        args.smt2,
        args.time_limit,
        args.require_three_halves,
        args.require_residual_total,
        args.require_tail_seven,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
