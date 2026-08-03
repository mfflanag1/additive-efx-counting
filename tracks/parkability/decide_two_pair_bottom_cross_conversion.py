#!/usr/bin/env python3
"""Test a cross-conversion lemma for two two-agent bottom pairs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        favorite_pair_universe,
        hall_failure,
        pairing_has_hall_matching,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    from anneal import atomic_json
    from decide_common_bottom_pairing_conversion import canonical_partition
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        favorite_pair_universe,
        hall_failure,
        pairing_has_hall_matching,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "two-pair-bottom-cross-conversion-lra-v1"
N = 4
M = 9
FAVORITE = 0
FIRST_LOWS = (7, 8)
FIRST_AGENTS = (0, 1)
DEFAULT_FIRST_MATCHING = ((1, 2), (3, 4), (5, 6))


def canonical_matching(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def disjoint_matching_orbits():
    first_matchings = tuple(perfect_pairings((1, 2, 3, 4, 5, 6)))
    second_matchings = tuple(perfect_pairings((1, 2, 3, 4, 7, 8)))
    universe = {
        (canonical_matching(first), canonical_matching(second))
        for first in first_matchings
        for second in second_matchings
    }
    groups = []
    for core_image in itertools.permutations((1, 2, 3, 4)):
        for swap_first_lows in (False, True):
            for swap_second_lows in (False, True):
                mapping = {
                    good: image
                    for good, image in zip((1, 2, 3, 4), core_image)
                }
                mapping.update(
                    {5: 6, 6: 5}
                    if swap_first_lows
                    else {5: 5, 6: 6}
                )
                mapping.update(
                    {7: 8, 8: 7}
                    if swap_second_lows
                    else {7: 7, 8: 8}
                )
                groups.append(mapping)

    def act(pair, mapping):
        return tuple(
            canonical_matching(
                tuple(
                    (mapping[edge[0]], mapping[edge[1]])
                    for edge in matching
                )
            )
            for matching in pair
        )

    representatives = []
    unseen = set(universe)
    while unseen:
        seed = min(unseen)
        orbit = {act(seed, mapping) for mapping in groups}
        if not orbit <= universe:
            raise AssertionError("disjoint matching action left its universe")
        representatives.append(min(orbit))
        unseen.difference_update(orbit)
    return tuple(sorted(representatives))


def overlap_matching_orbits():
    first_matchings = tuple(perfect_pairings((1, 2, 3, 4, 5, 6)))
    second_matchings = tuple(perfect_pairings((1, 2, 3, 4, 5, 7)))
    universe = {
        (canonical_matching(first), canonical_matching(second))
        for first in first_matchings
        for second in second_matchings
    }
    groups = []
    for core_image in itertools.permutations((1, 2, 3, 4, 5)):
        mapping = {
            good: image
            for good, image in zip((1, 2, 3, 4, 5), core_image)
        }
        mapping.update({6: 6, 7: 7})
        groups.append(mapping)

    def act(pair, mapping):
        return tuple(
            canonical_matching(
                tuple(
                    (mapping[edge[0]], mapping[edge[1]])
                    for edge in matching
                )
            )
            for matching in pair
        )

    representatives = []
    unseen = set(universe)
    while unseen:
        seed = min(unseen)
        orbit = {act(seed, mapping) for mapping in groups}
        if not orbit <= universe:
            raise AssertionError("overlap matching action left its universe")
        representatives.append(min(orbit))
        unseen.difference_update(orbit)
    return tuple(sorted(representatives))


def cells(pattern, orbit_index):
    if pattern == "disjoint":
        orbits = disjoint_matching_orbits()
        if orbit_index not in range(len(orbits)):
            raise ValueError("disjoint matching-orbit index is out of range")
        first_matching, second_matching = orbits[orbit_index]
        return first_matching, (5, 6), (2, 3), second_matching, len(orbits)
    if pattern == "overlap":
        orbits = overlap_matching_orbits()
        if orbit_index not in range(len(orbits)):
            raise ValueError("overlap matching-orbit index is out of range")
        first_matching, second_matching = orbits[orbit_index]
        return first_matching, (6, 8), (2, 3), second_matching, len(orbits)
    raise ValueError("unknown bottom-pair pattern")


def conversions(lows, matching):
    return tuple(
        canonical_partition(
            (FAVORITE, high),
            (*edge, low),
            *(pair for pair in matching if pair != edge),
        )
        for high, low in (lows, tuple(reversed(lows)))
        for edge in matching
    )


def add_bottom_orders(master, lows, agents):
    residual = tuple(good for good in range(1, M) if good not in lows)
    for agent in agents:
        for low in lows:
            for good in residual:
                master.solver.add(
                    master.values[agent][low]
                    <= master.values[agent][good]
                )


def run(
    output: Path,
    formula_output: Path,
    pattern: str,
    orbit_index: int,
    time_limit: float,
    obstruction_family: str = "local_conversions",
):
    (
        first_matching,
        second_lows,
        second_agents,
        second_matching,
        matching_orbit_count,
    ) = cells(pattern, orbit_index)
    first_residual = tuple(
        good for good in range(1, M) if good not in FIRST_LOWS
    )
    second_residual = tuple(
        good for good in range(1, M) if good not in second_lows
    )
    conversion_family = tuple(
        dict.fromkeys(
            (*conversions(FIRST_LOWS, first_matching),
             *conversions(second_lows, second_matching))
        )
    )
    obstruction_partitions = (
        conversion_family
        if obstruction_family == "local_conversions"
        else tuple(favorite_pair_universe("all"))
        if obstruction_family == "all_favorite_pair"
        else None
    )
    if obstruction_partitions is None:
        raise ValueError("unknown obstruction family")

    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure_cardinal(master)
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
    for partition in obstruction_partitions:
        master.add_partition_obstruction(partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    values = solved.values
    if values is not None:
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
        if supported_partitions(values, list(obstruction_partitions)):
            raise AssertionError("model gained an obstructed repair")

    formula = master.to_smt2()
    formula_output.parent.mkdir(parents=True, exist_ok=True)
    formula_output.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "CROSS_CONVERSION_COUNTEREXAMPLE"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "pattern": pattern,
        "matching_orbit_index": orbit_index,
        "matching_orbit_count": matching_orbit_count,
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
        "conversion_partition_count": len(conversion_family),
        "obstruction_family": obstruction_family,
        "obstruction_partition_count": len(obstruction_partitions),
        "values": [list(row) for row in values] if values else None,
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds": time_limit,
        "smt2_path": str(formula_output),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "This tests one canonical pair of residual matchings. Even UNSAT "
            "does not cover the other relative matching orbits. With the "
            "all-favorite-pair obstruction family, SAT would refute only the "
            "conditional two-cell selector, not complete EFX."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--pattern", choices=("disjoint", "overlap"), required=True)
    parser.add_argument("--orbit-index", type=int, default=0)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument(
        "--obstruction-family",
        choices=("local_conversions", "all_favorite_pair"),
        default="local_conversions",
    )
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    result = run(
        args.output,
        args.formula,
        args.pattern,
        args.orbit_index,
        args.time_limit,
        args.obstruction_family,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
