#!/usr/bin/env python3
"""Search for a rank-three partition with no nearby EFX partition."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json, mutate
    from .audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )
except ImportError:
    import core
    from anneal import atomic_json, mutate
    from audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )


def parse_partition(
    raw: str,
    n: int,
    m: int,
) -> tuple[tuple[int, ...], ...]:
    partition = canonical_partition([
        [int(good) for good in bundle.split(",") if good]
        for bundle in raw.split("/")
    ])
    if (
        len(partition) != n
        or any(not bundle for bundle in partition)
        or sorted(good for bundle in partition for good in bundle)
        != list(range(m))
    ):
        raise ValueError("source must partition every good into n bundles")
    return partition


def radius_ball(
    source: tuple[tuple[int, ...], ...],
    radius: int,
) -> dict[tuple[tuple[int, ...], ...], int]:
    distances = {source: 0}
    frontier = {source}
    for distance in range(1, radius + 1):
        frontier = {
            neighbor
            for partition in frontier
            for neighbor in transfer_neighbors(partition)
            if neighbor not in distances
        }
        distances.update((partition, distance) for partition in frontier)
    return distances


def evaluate(
    values: list[list[int]],
    source: tuple[tuple[int, ...], ...],
    distances: dict[tuple[tuple[int, ...], ...], int],
) -> dict:
    validated = tuple(map(tuple, values))
    ranks = {
        partition: matching_rank(feasible_graph(validated, partition))
        for partition in distances
    }
    n = len(values)
    perfect_by_distance = Counter(
        distance
        for partition, distance in distances.items()
        if ranks[partition] == n
    )
    return {
        "source_rank": ranks[source],
        "perfect_partition_count": sum(perfect_by_distance.values()),
        "perfect_partition_count_by_distance": {
            str(distance): perfect_by_distance[distance]
            for distance in range(max(distances.values()) + 1)
        },
    }


def objective(result: dict, n: int) -> float:
    rank_penalty = 0 if result["source_rank"] == n - 1 else 100_000
    return rank_penalty + result["perfect_partition_count"]


def run(
    seed_paths: list[Path],
    source: tuple[tuple[int, ...], ...],
    radius: int,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
) -> dict:
    rng = random.Random(random_seed)
    seeds = [
        [
            list(row)
            for row in core.validate_values(
                json.loads(path.read_text())["values"],
                lower=1,
            )
        ]
        for path in seed_paths
    ]
    n = len(seeds[0])
    distances = radius_ball(source, radius)
    evaluated = [(evaluate(values, source, distances), values) for values in seeds]
    evaluated.sort(key=lambda item: objective(item[0], n))
    current_result, current = evaluated[0]
    current = [row[:] for row in current]
    best_result = current_result
    best = [row[:] for row in current]
    started = time.time()

    for iteration in range(1, iterations + 1):
        candidate = mutate(
            current,
            max(current_result["perfect_partition_count"], 1),
            rng,
        )
        candidate_result = evaluate(candidate, source, distances)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = (
            objective(candidate_result, n) - objective(current_result, n)
        )
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_result = candidate_result
        if objective(candidate_result, n) < objective(best_result, n):
            best = [row[:] for row in candidate]
            best_result = candidate_result
            print(
                f"iteration={iteration} source_rank={best_result['source_rank']} "
                f"nearby_perfect={best_result['perfect_partition_count']}",
                flush=True,
            )
            if (
                best_result["source_rank"] == n - 1
                and best_result["perfect_partition_count"] == 0
            ):
                break
    return {
        "status": (
            "COUNTEREXAMPLE"
            if (
                best_result["source_rank"] == n - 1
                and best_result["perfect_partition_count"] == 0
            )
            else "CHECKPOINT"
        ),
        "iterations_completed": iteration,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "transfer_radius": radius,
        "ball_partition_count": len(distances),
        "source_partition": [list(bundle) for bundle in source],
        "values": best,
        "audit": best_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--iterations", type=int, default=10_000)
    parser.add_argument("--random-seed", type=int, default=20260730)
    parser.add_argument("--initial-temperature", type=float, default=2.0)
    parser.add_argument("--final-temperature", type=float, default=0.01)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.radius < 1 or args.iterations < 1:
        parser.error("radius and iterations must be positive")
    first = json.loads(args.seed[0].read_text())
    n = len(first["values"])
    m = len(first["values"][0])
    source = parse_partition(args.source, n, m)
    result = run(
        args.seed,
        source,
        args.radius,
        args.iterations,
        args.random_seed,
        args.initial_temperature,
        args.final_temperature,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
