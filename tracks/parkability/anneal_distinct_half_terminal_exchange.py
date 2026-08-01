#!/usr/bin/env python3
"""Adversarial search for a terminal state isolated from radius-two repairs."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import (
        Landscape,
        maximum_matching_rank,
    )
    from .audit_distinct_half_rank_augmentation import universal_threshold_failure
    from .decide_distinct_half_terminal_exchange import (
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        matching_slacks,
        target_partitions,
    )
    from .run_distinct_half_full_cell_cegar import full_hall_cells
except ImportError:
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import (
        Landscape,
        maximum_matching_rank,
    )
    from audit_distinct_half_rank_augmentation import universal_threshold_failure
    from decide_distinct_half_terminal_exchange import (
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        matching_slacks,
        target_partitions,
    )
    from run_distinct_half_full_cell_cegar import full_hall_cells


SCHEMA = "distinct-half-terminal-exchange-anneal-v1"
N = 4
M = 9


def load_values(path):
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        raise ValueError(f"seed has no values: {path}")
    return tuple(tuple(row) for row in raw)


def branch_valid(values, terminal, matching):
    return all(
        row[0] > max(row[1:])
        and 2 * row[agent + 1] > row[0]
        and universal_threshold_failure(row)
        for agent, row in enumerate(values)
    ) and min(matching_slacks(values, terminal, matching)) >= 0


def mutate(values, rng, temperature):
    candidate = [list(row) for row in values]
    steps = 2 if rng.random() < 0.2 else 1
    for _ in range(steps):
        agent = rng.randrange(N)
        good = rng.randrange(1, M)
        favorite = candidate[agent][0]
        scale = max(1, round(favorite * temperature / 10))
        if rng.random() < 0.85:
            delta = rng.choice((-1, 1)) * rng.randint(1, scale)
            candidate[agent][good] = max(
                1, min(favorite - 1, candidate[agent][good] + delta)
            )
        else:
            candidate[agent][good] = rng.randint(1, favorite - 1)
    return tuple(tuple(row) for row in candidate)


def run(
    case,
    matching_orbit,
    seed_paths,
    iterations,
    random_seed,
    output,
    require_no_full_cell=False,
):
    rng = random.Random(random_seed)
    terminal = TERMINAL_PARTITIONS[case]
    matching = TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit]
    landscape = Landscape("favorite_pair")
    positions = {partition: position for position, partition in enumerate(landscape.universe)}
    target_positions = tuple(
        positions[partition] for partition in target_partitions("radius2", terminal)
    )

    def repair_count(values):
        graph_rows = tuple(landscape.row_graph_masks(row) for row in values)
        return sum(
            maximum_matching_rank(
                tuple(graph_rows[agent][position] for agent in range(N))
            )
            == N
            for position in target_positions
        )

    seeds = tuple(load_values(path) for path in seed_paths)
    evaluated = sorted(
        (repair_count(values), values)
        for values in seeds
        if branch_valid(values, terminal, matching)
        and (not require_no_full_cell or not full_hall_cells(values))
    )
    if not evaluated:
        raise ValueError("no seed satisfies the fixed terminal branch")
    best_count, best = evaluated[0]
    current_count, current = evaluated[0]
    started = time.time()
    completed = 0
    for iteration in range(1, iterations + 1):
        completed = iteration
        if iteration > 1 and (iteration - 1) % 1000 == 0:
            current_count, current = evaluated[
                ((iteration - 1) // 1000) % len(evaluated)
            ]
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = 1.0 * (0.02 ** progress)
        candidate = mutate(current, rng, temperature)
        if not branch_valid(candidate, terminal, matching):
            continue
        candidate_count = repair_count(candidate)
        change = candidate_count - current_count
        accepted = change <= 0 or rng.random() < math.exp(
            -change / max(temperature, 1e-9)
        )
        if accepted and require_no_full_cell and full_hall_cells(candidate):
            accepted = False
        if accepted:
            current_count, current = candidate_count, candidate
        if accepted and candidate_count < best_count:
            best_count, best = candidate_count, candidate
            print(f"iteration={iteration} repairs={best_count}", flush=True)
            if best_count == 0:
                break

    result = {
        "schema": SCHEMA,
        "status": "COUNTEREXAMPLE" if best_count == 0 else "CHECKPOINT",
        "case": case,
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": list(matching),
        "target": "radius2",
        "target_partition_count": len(target_positions),
        "target_repair_count": best_count,
        "full_hall_cell_forbidden": require_no_full_cell,
        "iterations_completed": completed,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "values": [list(row) for row in best],
        "minimum_terminal_matching_slack": min(
            matching_slacks(best, terminal, matching)
        ),
        "full_hall_cells": full_hall_cells(best),
        "warning": (
            "A zero-repair profile refutes only the selected terminal exchange "
            "lemma; a checkpoint is heuristic evidence only."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument("--matching-orbit", type=int, required=True)
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=10_000)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-no-full-cell", action="store_true")
    args = parser.parse_args()
    if (
        args.iterations < 1
        or not 0
        <= args.matching_orbit
        < len(TERMINAL_MATCHING_REPRESENTATIVES[args.case])
    ):
        parser.error("invalid annealing parameters")
    result = run(
        args.case,
        args.matching_orbit,
        tuple(args.seed),
        args.iterations,
        args.random_seed,
        args.output,
        args.require_no_full_cell,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
