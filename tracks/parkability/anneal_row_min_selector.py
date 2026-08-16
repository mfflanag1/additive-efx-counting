#!/usr/bin/env python3
"""Heuristically search for an unparkable row-minimum set."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json, mutate
    from .fast_count import FastParkability
except ImportError:
    import core
    import independent
    from anneal import atomic_json, mutate
    from fast_count import FastParkability


def load_values(path: Path) -> list[list[int]]:
    raw = json.loads(path.read_text())
    values = raw.get("values", raw.get("candidate_values"))
    if values is None:
        raise ValueError(f"{path} contains no values")
    return [list(row) for row in core.validate_values(values, lower=1)]


def low_rank_goods(
    values: tuple[tuple[int, ...], ...],
    rank_depth: int,
) -> tuple[int, ...]:
    if rank_depth < 0 or rank_depth > len(values[0]):
        raise ValueError("rank depth is outside the goods range")
    if rank_depth == 0:
        for candidate_depth in range(1, len(values[0]) + 1):
            low_sets = []
            for row in values:
                cutoff = sorted(row)[candidate_depth - 1]
                low_sets.append({
                    good
                    for good, value in enumerate(row)
                    if value <= cutoff
                })
            if any(
                all(good in low_sets[agent] for agent, good in enumerate(matching))
                for matching in itertools.permutations(
                    range(len(values[0])),
                    len(values),
                )
            ):
                return tuple(sorted(set().union(*low_sets)))
        raise AssertionError("full low-rank graph lacks a matching")
    selected = set()
    for row in values:
        cutoff = sorted(row)[rank_depth - 1]
        selected.update(
            good for good, value in enumerate(row) if value <= cutoff
        )
    return tuple(sorted(selected))


def score(
    values: list[list[int]],
    landscape: dict,
    rank_depth: int,
) -> tuple[int, int, float]:
    selected = low_rank_goods(
        tuple(tuple(row) for row in values),
        rank_depth,
    )
    counts = [
        sum(host_counts)
        for host_counts in landscape["parkable_triple_count_by_floater_host"]
    ]
    return (
        sum(counts[good] for good in selected),
        landscape["parkable_triple_count"],
        landscape["normalized_margin_sum"],
    )


def objective(key: tuple[int, int, float]) -> float:
    return key[0] + 0.01 * key[1] + 0.000001 * key[2]


def run(
    seed_paths: list[Path],
    iterations: int,
    random_seed: int,
    restart_every: int,
    initial_temperature: float,
    final_temperature: float,
    rank_depth: int,
) -> dict:
    if not seed_paths or iterations < 1 or restart_every < 1:
        raise ValueError("seeds and positive iteration limits are required")
    evaluator = FastParkability()
    seeds = [load_values(path) for path in seed_paths]
    seeds.sort(
        key=lambda values: score(
            values,
            evaluator.landscape(values),
            rank_depth,
        )
    )
    rng = random.Random(random_seed)
    started = time.time()
    current = [row[:] for row in seeds[0]]
    current_landscape = evaluator.landscape(current)
    current_key = score(current, current_landscape, rank_depth)
    best = [row[:] for row in current]
    best_landscape = dict(current_landscape)
    best_key = current_key

    for iteration in range(1, iterations + 1):
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            seed = seeds[((iteration - 1) // restart_every) % len(seeds)]
            current = [row[:] for row in seed]
            current_landscape = evaluator.landscape(current)
            current_key = score(current, current_landscape, rank_depth)
        candidate = mutate(current, max(current_key[0], 1), rng)
        if candidate == current:
            continue
        candidate_landscape = evaluator.landscape(candidate)
        candidate_key = score(candidate, candidate_landscape, rank_depth)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective(candidate_key) - objective(current_key)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            current_key = candidate_key
        if candidate_key < best_key:
            best = [row[:] for row in candidate]
            best_landscape = dict(candidate_landscape)
            best_key = candidate_key
            print(
                f"iteration={iteration} selected={best_key[0]} "
                f"total={best_key[1]}",
                flush=True,
            )
            if best_key[0] == 0:
                break

    values = tuple(tuple(row) for row in best)
    selected_goods = low_rank_goods(values, rank_depth)
    literal = independent.enumerate_base_first(values)
    selected_literal = [
        triple for triple in literal if triple[0] in selected_goods
    ]
    if bool(selected_literal) != bool(best_key[0]):
        raise AssertionError("vectorized and literal selected counts disagree")
    return {
        "status": (
            "COUNTEREXAMPLE"
            if not selected_literal
            else "CHECKPOINT"
        ),
        "iterations_completed": iteration,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "rank_depth": rank_depth,
        "rank_depth_meaning": (
            "minimum Hall-saturating depth"
            if rank_depth == 0
            else "fixed bottom-rank depth"
        ),
        "values": [list(row) for row in values],
        "low_rank_goods": list(selected_goods),
        "low_rank_parkable_triple_count": len(selected_literal),
        "complete_efx0_count": independent.count_complete_efx0(values),
        "landscape": best_landscape,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--restart-every", type=int, default=5_000)
    parser.add_argument("--initial-temperature", type=float, default=2.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument("--rank-depth", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.seed,
        args.iterations,
        args.random_seed,
        args.restart_every,
        args.initial_temperature,
        args.final_temperature,
        args.rank_depth,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
