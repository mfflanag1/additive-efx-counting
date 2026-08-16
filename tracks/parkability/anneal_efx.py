#!/usr/bin/env python3
"""Heuristic complete-EFX minimizer with exact terminal verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from . import core, independent
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .fast_count import FastParkability
except ImportError:
    import core
    import independent
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from fast_count import FastParkability


SCHEMA = "complete-efx-anneal-result-v1"


def load_seed_values(path: Path) -> list[list[list[int]]]:
    text = path.read_text()
    try:
        documents = [json.loads(text)]
    except json.JSONDecodeError:
        documents = [json.loads(line) for line in text.splitlines() if line.strip()]
    seeds = []
    for document in documents:
        values = document.get("candidate_values", document.get("values"))
        if values is not None:
            seeds.append([list(row) for row in core.validate_values(values, lower=1)])
    if not seeds:
        raise ValueError(f"{path} contains no valuation matrices")
    return seeds


def objective(landscape: dict) -> float:
    count = landscape["complete_efx0_count"]
    if count == 0:
        return 0.0
    average_margin = landscape["normalized_margin_sum"] / count
    return count + 0.1 * average_margin


def best_key(landscape: dict) -> tuple:
    return (
        landscape["complete_efx0_count"],
        landscape["normalized_margin_sum"],
        landscape["positive_margin_sum"],
    )


def run(
    *,
    seed_paths: list[Path],
    iterations: int,
    random_seed: int,
    restart_every: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        not seed_paths
        or iterations < 1
        or restart_every < 1
        or initial_temperature <= 0
        or final_temperature <= 0
    ):
        raise ValueError("seeds, iterations, restarts, and temperatures are required")
    if trace_path is not None and trace_path.exists():
        raise ValueError("annealing trace path must be new")
    seeds = [
        values
        for path in seed_paths
        for values in load_seed_values(path)
        if not has_universal_min(values)
    ]
    if not seeds:
        raise ValueError("all seeds have a universal-minimum good")
    n = len(seeds[0])
    m = len(seeds[0][0])
    if any(
        len(values) != n or len(values[0]) != m
        for values in seeds
    ):
        raise ValueError("all seeds must have the same dimensions")
    evaluator = FastParkability(n, m)
    seeds.sort(key=lambda values: best_key(evaluator.complete_efx0_landscape(values)))
    rng = random.Random(random_seed)
    started = time.time()
    current = [row[:] for row in seeds[0]]
    current_landscape = evaluator.complete_efx0_landscape(current)
    best = [row[:] for row in current]
    best_landscape = dict(current_landscape)
    accepted = 0
    improvements = 0

    for iteration in range(1, iterations + 1):
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            seed_index = ((iteration - 1) // restart_every) % len(seeds)
            current = [row[:] for row in seeds[seed_index]]
            current_landscape = evaluator.complete_efx0_landscape(current)

        candidate = mutate(
            current,
            current_landscape["complete_efx0_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_landscape = evaluator.complete_efx0_landscape(candidate)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective(candidate_landscape) - objective(current_landscape)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            accepted += 1

        if best_key(candidate_landscape) < best_key(best_landscape):
            best = [row[:] for row in candidate]
            best_landscape = dict(candidate_landscape)
            improvements += 1
            append_jsonl(
                trace_path,
                {
                    "iteration": iteration,
                    "elapsed_seconds": round(time.time() - started, 6),
                    "random_seed": random_seed,
                    "values": best,
                    **best_landscape,
                },
            )
            print(
                f"iteration={iteration} "
                f"complete_efx0={best_landscape['complete_efx0_count']} "
                f"normalized_margin={best_landscape['normalized_margin_sum']:.6f}",
                flush=True,
            )
            if best_landscape["complete_efx0_count"] == 0:
                break

    status = "CHECKPOINT"
    independent_audit = None
    if best_landscape["complete_efx0_count"] == 0:
        exact = core.landscape(best, sample_limit=0)
        literal_count = independent.count_complete_efx0(best)
        base_first = independent.enumerate_base_first(best)
        completion_first = independent.enumerate_completion_first(best)
        if (
            exact["complete_efx0_count"]
            or exact["parkable_triple_count"]
            or literal_count
            or base_first
            or completion_first
        ):
            raise AssertionError("zero-EFX candidate failed independent terminal audit")
        status = "ZERO_COMPLETE_EFX0"
        independent_audit = {
            "core_landscape": exact,
            "literal_complete_efx0_count": literal_count,
            "base_first_parkable_triples": len(base_first),
            "completion_first_parkable_triples": len(completion_first),
        }

    result = {
        "schema": SCHEMA,
        "status": status,
        "seed_paths": [str(path.resolve()) for path in seed_paths],
        "seed_sha256": {
            str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in seed_paths
        },
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "restart_every": restart_every,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "values": best,
        "landscape": best_landscape,
        "independent_audit": independent_audit,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--restart-every", type=int, default=5_000)
    parser.add_argument("--initial-temperature", type=float, default=2.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_paths=args.seed,
        iterations=args.iterations,
        random_seed=args.random_seed,
        restart_every=args.restart_every,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        output_path=args.output,
        trace_path=args.trace,
    )
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
