#!/usr/bin/env python3
"""Search for a trapped plateau in partition EFX-matching rank."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json, mutate
    from .audit_matching_augmentation import audit
except ImportError:
    import core
    from anneal import atomic_json, mutate
    from audit_matching_augmentation import audit


def load_values(path: Path) -> list[list[int]]:
    raw = json.loads(path.read_text())
    return [
        list(row)
        for row in core.validate_values(raw["values"], lower=1)
    ]


def key(result: dict) -> tuple[int, int, int]:
    if result["trapped_component_count"]:
        return (-1, result["perfect_partition_count"], 0)
    minimum = result["minimum_augmenting_exit_count"]
    if minimum is None:
        minimum = 10**9
    total_exits = sum(
        int(count) * frequency
        for count, frequency in result["augmenting_exit_count_histogram"].items()
    )
    return minimum, result["perfect_partition_count"], total_exits


def objective(result_key: tuple[int, int, int]) -> float:
    return result_key[0] + 0.001 * result_key[1] + 0.0000001 * result_key[2]


def run(
    seed_paths: list[Path],
    iterations: int,
    random_seed: int,
    restart_every: int,
    initial_temperature: float,
    final_temperature: float,
) -> dict:
    if not seed_paths or iterations < 1 or restart_every < 1:
        raise ValueError("seeds and positive limits are required")
    rng = random.Random(random_seed)
    seeds = [load_values(path) for path in seed_paths]
    evaluated_seeds = [(audit(tuple(map(tuple, values))), values) for values in seeds]
    evaluated_seeds.sort(key=lambda item: key(item[0]))
    started = time.time()
    current_result, current = evaluated_seeds[0]
    current = [row[:] for row in current]
    current_key = key(current_result)
    best_result = current_result
    best = [row[:] for row in current]
    best_key = current_key

    for iteration in range(1, iterations + 1):
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            current_result, seed = evaluated_seeds[
                ((iteration - 1) // restart_every) % len(evaluated_seeds)
            ]
            current = [row[:] for row in seed]
            current_key = key(current_result)
        candidate = mutate(current, max(current_key[0], 1), rng)
        if candidate == current:
            continue
        candidate_result = audit(tuple(map(tuple, candidate)))
        candidate_key = key(candidate_result)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective(candidate_key) - objective(current_key)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_result = candidate_result
            current_key = candidate_key
        if candidate_key < best_key:
            best = [row[:] for row in candidate]
            best_result = candidate_result
            best_key = candidate_key
            print(
                f"iteration={iteration} min_exits={best_key[0]} "
                f"perfect={best_key[1]} total_exits={best_key[2]}",
                flush=True,
            )
            if best_key[0] == -1:
                break
    return {
        "status": (
            "COUNTEREXAMPLE"
            if best_result["trapped_component_count"]
            else "CHECKPOINT"
        ),
        "iterations_completed": iteration,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "values": best,
        "audit": best_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=2_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--restart-every", type=int, default=500)
    parser.add_argument("--initial-temperature", type=float, default=1.0)
    parser.add_argument("--final-temperature", type=float, default=0.001)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.seed,
        args.iterations,
        args.random_seed,
        args.restart_every,
        args.initial_temperature,
        args.final_temperature,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
