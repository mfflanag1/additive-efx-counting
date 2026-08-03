#!/usr/bin/env python3
"""Adversarial search on the eight-minus-six orbit residual."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import (
        Landscape,
        load_values,
        maximum_matching_rank,
        mutate,
    )
    from .audit_distinct_half_rank_augmentation import (
        audit_branch,
        universal_threshold_failure,
    )
    from .run_distinct_half_full_cell_cegar import (
        common_bottom_pairs,
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import (
        Landscape,
        load_values,
        maximum_matching_rank,
        mutate,
    )
    from audit_distinct_half_rank_augmentation import (
        audit_branch,
        universal_threshold_failure,
    )
    from run_distinct_half_full_cell_cegar import (
        common_bottom_pairs,
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )


SCHEMA = "distinct-half-eight-orbit-anneal-v1"
N = 4
M = 9


def branch_valid(values):
    return all(
        row[0] > max(row[1:])
        and 2 * row[agent + 1] > row[0]
        and universal_threshold_failure(row)
        for agent, row in enumerate(values)
    )


def agent_bottom_pattern_holds(values, pattern):
    if pattern is None:
        return True
    return all(
        max(values[agent][low] for low in lows)
        <= min(
            values[agent][good]
            for good in range(1, M)
            if good not in lows
        )
        for agent, lows in enumerate(pattern)
    )


def parse_agent_bottom_pattern(raw):
    if raw is None:
        return None
    parts = raw.split(";")
    if len(parts) != N:
        raise ValueError("one bottom pair per agent is required")
    pattern = []
    for part in parts:
        lows = tuple(sorted(int(token) for token in part.split(",")))
        if len(lows) != 2 or len(set(lows)) != 2 or any(
            low not in range(1, M) for low in lows
        ):
            raise ValueError("bottom pairs must be two distinct residual goods")
        pattern.append(lows)
    return tuple(pattern)


def run(
    seed_paths,
    iterations,
    random_seed,
    restart_every,
    output,
    hard_six_orbit=True,
    partition_family="eight_orbit",
    use_margin=False,
    initial_temperature=4.0,
    final_temperature=0.02,
    forbid_common_bottom_pair=False,
    forbid_three_agent_bottom_pair=False,
    required_agent_bottom_pattern=None,
):
    rng = random.Random(random_seed)
    landscape = Landscape("favorite_pair")
    positions = {
        partition: position
        for position, partition in enumerate(landscape.universe)
    }
    six_orbit = set(favorite_pair_universe("six_orbit"))
    six_positions = tuple(positions[partition] for partition in six_orbit)
    residual_positions = tuple(
        positions[partition]
        for partition in favorite_pair_universe("eight_orbit")
        if partition not in six_orbit
    )
    if partition_family == "all":
        target_positions = tuple(range(len(landscape.universe)))
    elif hard_six_orbit:
        target_positions = residual_positions
    else:
        target_positions = tuple(sorted((*six_positions, *residual_positions)))

    def perfect_count(values, selected_positions):
        graph_rows = tuple(landscape.row_graph_masks(row) for row in values)
        return sum(
            maximum_matching_rank(
                tuple(graph_rows[agent][position] for agent in range(N))
            )
            == N
            for position in selected_positions
        )

    slack_cache = {}

    def row_slacks(row):
        cached = slack_cache.get(row)
        if cached is not None:
            return cached
        sums, minima = landscape.row_tables(row)
        result = tuple(
            tuple(
                sums[mask]
                - max(
                    sums[target] - minima[target]
                    for target in bundle_masks
                )
                for mask in bundle_masks
            )
            for bundle_masks in landscape.bundle_masks
        )
        slack_cache[row] = result
        return result

    def statistics(values, selected_positions):
        if not use_margin:
            return perfect_count(values, selected_positions), 0
        graph_rows = tuple(landscape.row_graph_masks(row) for row in values)
        slack_rows = tuple(row_slacks(row) for row in values)
        count = 0
        margin_sum = 0
        for position in selected_positions:
            if maximum_matching_rank(
                tuple(row[position] for row in graph_rows)
            ) != N:
                continue
            count += 1
            bottleneck = max(
                min(
                    slack_rows[agent][position][matching[agent]]
                    for agent in range(N)
                )
                for matching in itertools.permutations(range(N))
            )
            margin_sum += min(max(bottleneck, 0), 100)
        return count, margin_sum

    def objective(count, margin_sum):
        return count + 0.1 * margin_sum / (100 * max(count, 1))

    def counts(values):
        return (
            perfect_count(values, six_positions),
            perfect_count(values, residual_positions),
        )

    evaluated = []
    for path in seed_paths:
        values = load_values(path)
        if (
            not branch_valid(values)
            or full_hall_cells(values)
            or (forbid_common_bottom_pair and common_bottom_pairs(values))
            or (
                forbid_three_agent_bottom_pair
                and three_agent_bottom_pairs(values)
            )
            or not agent_bottom_pattern_holds(
                values, required_agent_bottom_pattern
            )
        ):
            continue
        six_count, residual_count = counts(values)
        if not hard_six_orbit or six_count == 0:
            count, margin_sum = statistics(values, target_positions)
            evaluated.append((count, margin_sum, values))
    if not evaluated:
        raise ValueError("no seed satisfies the fixed no-full-cell six-orbit gate")
    evaluated.sort()
    current_count, current_margin, current = evaluated[0]
    best_count, best_margin, best = current_count, current_margin, current
    started = time.time()
    completed = 0
    for iteration in range(1, iterations + 1):
        completed = iteration
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            current_count, current_margin, current = evaluated[
                ((iteration - 1) // restart_every) % len(evaluated)
            ]
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        scale = max(2, round(20 * temperature / initial_temperature))
        candidate = mutate(current, rng, scale)
        if not branch_valid(candidate):
            continue
        candidate_count, candidate_margin = statistics(
            candidate, target_positions
        )
        change = objective(candidate_count, candidate_margin) - objective(
            current_count, current_margin
        )
        if change > 0 and rng.random() >= math.exp(-change / temperature):
            continue
        if hard_six_orbit and perfect_count(candidate, six_positions):
            continue
        if full_hall_cells(candidate):
            continue
        if forbid_common_bottom_pair and common_bottom_pairs(candidate):
            continue
        if (
            forbid_three_agent_bottom_pair
            and three_agent_bottom_pairs(candidate)
        ):
            continue
        if not agent_bottom_pattern_holds(
            candidate, required_agent_bottom_pattern
        ):
            continue
        current_count, current_margin, current = (
            candidate_count,
            candidate_margin,
            candidate,
        )
        if (candidate_count, candidate_margin) < (best_count, best_margin):
            best_count, best_margin, best = (
                candidate_count,
                candidate_margin,
                candidate,
            )
            print(f"iteration={iteration} residual_repairs={best_count}", flush=True)
            if best_count == 0:
                break

    audit_branch(best)
    six_count, residual_count = counts(best)
    replayed_count = perfect_count(best, target_positions)
    replayed_count_with_margin, replayed_margin = statistics(
        best, target_positions
    )
    all_favorite_pair_count = perfect_count(
        best, tuple(range(len(landscape.universe)))
    )
    if (
        (hard_six_orbit and six_count)
        or replayed_count != best_count
        or replayed_count_with_margin != best_count
        or replayed_margin != best_margin
        or full_hall_cells(best)
        or (forbid_common_bottom_pair and common_bottom_pairs(best))
        or (
            forbid_three_agent_bottom_pair
            and three_agent_bottom_pairs(best)
        )
        or not agent_bottom_pattern_holds(
            best, required_agent_bottom_pattern
        )
    ):
        raise AssertionError("final annealing replay changed")
    result = {
        "schema": SCHEMA,
        "status": (
            (
                "FULL_CELL_SELECTION_COUNTEREXAMPLE"
                if partition_family == "all"
                else "EIGHT_ORBIT_SELECTOR_COUNTEREXAMPLE"
            )
            if best_count == 0
            else "CHECKPOINT"
        ),
        "scope": (
            "integer profiles normalized to favorite 100 in the fixed-"
            "representative universal-threshold branch"
        ),
        "hard_six_orbit": hard_six_orbit,
        "partition_family": partition_family,
        "margin_tiebreak": use_margin,
        "six_orbit_repair_count": six_count,
        "eight_minus_six_repair_count": residual_count,
        "eight_orbit_repair_count": six_count + residual_count,
        "favorite_pair_repair_count": all_favorite_pair_count,
        "target_repair_margin_sum": best_margin,
        "full_hall_cells": [],
        "common_bottom_pair_forbidden": forbid_common_bottom_pair,
        "three_agent_bottom_pair_forbidden": (
            forbid_three_agent_bottom_pair
        ),
        "required_agent_bottom_pairs": (
            [list(pair) for pair in required_agent_bottom_pattern]
            if required_agent_bottom_pattern is not None
            else None
        ),
        "literal_complete_efx_count": independent.count_complete_efx0(best),
        "iterations_completed": completed,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "values": [list(row) for row in best],
        "warning": (
            (
                "A zero-repair profile refutes the favorite-pair/full-cell "
                "selector, not general EFX, unless literal complete-EFX "
                "enumeration is also zero."
                if partition_family == "all"
                else "A zero-repair profile refutes only the eight-orbit "
                "selector unless literal complete-EFX enumeration is also "
                "zero."
            )
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=50_000)
    parser.add_argument("--random-seed", type=int, default=20260803)
    parser.add_argument("--restart-every", type=int, default=5_000)
    parser.add_argument("--allow-six-orbit", action="store_true")
    parser.add_argument(
        "--partition-family", choices=("eight_orbit", "all"), default="eight_orbit"
    )
    parser.add_argument("--use-margin", action="store_true")
    parser.add_argument("--initial-temperature", type=float, default=4.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument("--forbid-common-bottom-pair", action="store_true")
    parser.add_argument(
        "--forbid-three-agent-bottom-pair", action="store_true"
    )
    parser.add_argument(
        "--require-agent-bottom-pairs",
        help="semicolon-separated pair per agent, e.g. 5,7;3,7;5,7;3,7",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if (
        args.iterations < 1
        or args.restart_every < 1
        or args.initial_temperature <= 0
        or args.final_temperature <= 0
    ):
        parser.error("positive iteration limits are required")
    try:
        required_agent_bottom_pattern = parse_agent_bottom_pattern(
            args.require_agent_bottom_pairs
        )
    except ValueError as error:
        parser.error(str(error))
    result = run(
        tuple(args.seed),
        args.iterations,
        args.random_seed,
        args.restart_every,
        args.output,
        not args.allow_six_orbit,
        args.partition_family,
        args.use_margin,
        args.initial_temperature,
        args.final_temperature,
        args.forbid_common_bottom_pair,
        args.forbid_three_agent_bottom_pair,
        required_agent_bottom_pattern,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
