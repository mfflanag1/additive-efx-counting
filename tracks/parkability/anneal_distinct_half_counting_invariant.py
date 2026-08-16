#!/usr/bin/env python3
"""Stress-test the 15-state favorite-pair/Hall-cell counting invariant."""

from __future__ import annotations

import argparse
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
        branch_valid,
        favorite_triple_cell_counts,
        load_values,
        maximum_matching_rank,
        mutate,
    )
    from .run_distinct_half_full_cell_cegar import common_bottom_pairs
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import (
        Landscape,
        branch_valid,
        favorite_triple_cell_counts,
        load_values,
        maximum_matching_rank,
        mutate,
    )
    from run_distinct_half_full_cell_cegar import common_bottom_pairs


SCHEMA = "distinct-half-counting-invariant-anneal-v1"
COUNTING_LOWER_BOUND = 15
N = 4


def run(
    seed_paths,
    iterations,
    random_seed,
    restart_every,
    initial_temperature,
    final_temperature,
    output,
    forbid_common_bottom_pair=False,
):
    rng = random.Random(random_seed)
    landscape = Landscape("favorite_pair")

    def audit(values):
        graph_rows = tuple(landscape.row_graph_masks(row) for row in values)
        favorite_pair_count = sum(
            maximum_matching_rank(
                tuple(row[position] for row in graph_rows)
            )
            == N
            for position in range(len(landscape.universe))
        )
        cells = favorite_triple_cell_counts(values)
        maximum_cell_count = max(cells.values(), default=0)
        return {
            "favorite_pair_efx_partition_count": favorite_pair_count,
            "maximum_favorite_triple_cell_count": maximum_cell_count,
            "counting_score": favorite_pair_count + maximum_cell_count,
            "maximizing_low_pairs": [
                list(lows)
                for lows, count in sorted(cells.items())
                if count == maximum_cell_count
            ],
        }

    seeds = [load_values(path) for path in seed_paths]
    seeds = [
        values
        for values in seeds
        if branch_valid(values)
        and (not forbid_common_bottom_pair or not common_bottom_pairs(values))
    ]
    if not seeds:
        raise ValueError("no seed satisfies the hard branch")
    evaluated = [(audit(values), values) for values in seeds]
    objective_key = (
        "favorite_pair_efx_partition_count"
        if forbid_common_bottom_pair
        else "counting_score"
    )
    stopping_bound = 1 if forbid_common_bottom_pair else COUNTING_LOWER_BOUND
    evaluated.sort(
        key=lambda item: (
            item[0][objective_key],
            item[0]["maximum_favorite_triple_cell_count"],
        )
    )
    current_record, current = evaluated[0]
    best_record, best = current_record, current
    started = time.time()
    completed = 0
    accepted = 0
    for iteration in range(1, iterations + 1):
        completed = iteration
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            current_record, current = evaluated[
                ((iteration - 1) // restart_every) % len(evaluated)
            ]
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        scale = max(
            2,
            round(20 * temperature / initial_temperature),
        )
        candidate = mutate(current, rng, scale)
        if (
            not branch_valid(candidate)
            or (
                forbid_common_bottom_pair
                and common_bottom_pairs(candidate)
            )
        ):
            continue
        candidate_record = audit(candidate)
        change = (
            candidate_record[objective_key]
            - current_record[objective_key]
        )
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current_record, current = candidate_record, candidate
            accepted += 1
        candidate_key = (
            candidate_record[objective_key],
            candidate_record["maximum_favorite_triple_cell_count"],
        )
        best_key = (
            best_record[objective_key],
            best_record["maximum_favorite_triple_cell_count"],
        )
        if candidate_key < best_key:
            best_record, best = candidate_record, candidate
            print(
                f"iteration={iteration} score={candidate_key[0]} "
                f"favorite_pair="
                f"{candidate_record['favorite_pair_efx_partition_count']} "
                f"cell={candidate_record['maximum_favorite_triple_cell_count']}",
                flush=True,
            )
            if candidate_key[0] < stopping_bound:
                break

    if forbid_common_bottom_pair:
        if best_record[objective_key] == 0:
            status = "NO_COMMON_BOTTOM_SELECTION_COUNTEREXAMPLE"
        elif best_record[objective_key] < COUNTING_LOWER_BOUND:
            status = "NO_COMMON_BOTTOM_QUANTITATIVE_COUNTEREXAMPLE"
        else:
            status = "CHECKPOINT"
    else:
        status = (
            "COUNTING_INVARIANT_COUNTEREXAMPLE"
            if best_record[objective_key] < COUNTING_LOWER_BOUND
            else "CHECKPOINT"
        )
    result = {
        "schema": SCHEMA,
        "status": status,
        "scope": (
            "integer profiles normalized to favorite 100 in the exact "
            "universal-threshold distinct-representative branch"
        ),
        "candidate_lower_bound": COUNTING_LOWER_BOUND,
        "selection_counterexample_requires_favorite_pair_count": 0,
        "common_bottom_pair_forbidden": forbid_common_bottom_pair,
        "iterations_completed": completed,
        "accepted_moves": accepted,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "values": [list(row) for row in best],
        "audit": best_record,
        "literal_complete_efx_count": independent.count_complete_efx0(best),
        "warning": (
            "A positive favorite-pair count does not refute the qualitative "
            "common-bottom selection lemma. Any unrefuted lower bound is "
            "falsification evidence only, not a proof."
            if forbid_common_bottom_pair
            else "Failure to find score below 15 is falsification evidence "
            "only, not a proof of the counting invariant."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=50_000)
    parser.add_argument("--random-seed", type=int, default=20260818)
    parser.add_argument("--restart-every", type=int, default=5_000)
    parser.add_argument("--initial-temperature", type=float, default=8.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--forbid-common-bottom-pair", action="store_true")
    args = parser.parse_args()
    if (
        args.iterations < 1
        or args.restart_every < 1
        or args.initial_temperature <= 0
        or args.final_temperature <= 0
    ):
        parser.error("invalid annealing parameters")
    result = run(
        tuple(args.seed),
        args.iterations,
        args.random_seed,
        args.restart_every,
        args.initial_temperature,
        args.final_temperature,
        args.output,
        args.forbid_common_bottom_pair,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
