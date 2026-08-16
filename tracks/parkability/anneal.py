#!/usr/bin/env python3
"""Heuristic parkability-count minimizer with exact terminal verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import tempfile
import time
from pathlib import Path

try:
    from . import core, independent
    from .fast_count import FastParkability
except ImportError:
    import core
    import independent
    from fast_count import FastParkability


SCHEMA = "parkability-anneal-result-v1"


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def append_jsonl(path: Path | None, value: dict) -> None:
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as handle:
            handle.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def load_trace_seeds(path: Path) -> list[list[list[int]]]:
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    records.sort(
        key=lambda record: (
            record["parkable_triple_count"],
            record.get("normalized_margin_sum", math.inf),
        )
    )
    return [
        record["candidate_values"] if "candidate_values" in record else record["values"]
        for record in records
    ]


def has_universal_min(values: list[list[int]]) -> bool:
    return any(
        all(
            values[observer][good] == min(values[observer])
            for observer in range(len(values))
        )
        for good in range(len(values[0]))
    )


def mutate(
    values: list[list[int]],
    parkable_count: int,
    rng: random.Random,
) -> list[list[int]]:
    candidate = [row[:] for row in values]
    steps = 1
    if parkable_count <= 20:
        draw = rng.random()
        steps = 3 if draw < 0.05 else 2 if draw < 0.3 else 1
    for _ in range(steps):
        observer = rng.randrange(len(values))
        left, right = rng.sample(range(len(values[0])), 2)
        if rng.random() < (0.04 if parkable_count <= 20 else 0.12):
            candidate[observer][left], candidate[observer][right] = (
                candidate[observer][right],
                candidate[observer][left],
            )
            continue

        if candidate[observer][left] == 1:
            left, right = right, left
        available = candidate[observer][left] - 1
        if available < 1:
            continue
        scale = max(1, sum(candidate[observer]) // 25)
        if parkable_count <= 20 and rng.random() < 0.8:
            scale = min(scale, 5)
        maximum = min(available, scale)
        delta = rng.randrange(1, maximum + 1)
        candidate[observer][left] -= delta
        candidate[observer][right] += delta
    return candidate


def objective(landscape: dict) -> float:
    count = landscape["parkable_triple_count"]
    if count > 20:
        return count + 0.001 * landscape["normalized_margin_sum"]
    floater_counts = [
        sum(row)
        for row in landscape["parkable_triple_count_by_floater_host"]
    ]
    return (
        count
        + 0.002 * max(floater_counts, default=0)
        + 0.0001 * sum(value * value for value in floater_counts)
        + 0.00001 * landscape["normalized_margin_sum"]
    )


def best_key(landscape: dict) -> tuple:
    floater_counts = [
        sum(row)
        for row in landscape["parkable_triple_count_by_floater_host"]
    ]
    return (
        landscape["parkable_triple_count"],
        max(floater_counts, default=0),
        sum(value * value for value in floater_counts),
        landscape["normalized_margin_sum"],
    )


def run(
    *,
    seed_trace: Path,
    iterations: int,
    random_seed: int,
    restart_every: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        iterations < 1
        or restart_every < 1
        or initial_temperature <= 0
        or final_temperature <= 0
    ):
        raise ValueError("iteration and restart counts must be positive")
    if trace_path is not None and trace_path.exists():
        raise ValueError("annealing trace path must be new")
    seeds = load_trace_seeds(seed_trace)
    if not seeds:
        raise ValueError("seed trace contains no candidates")
    evaluator = FastParkability()
    rng = random.Random(random_seed)
    started = time.time()
    current = [row[:] for row in seeds[0]]
    current_landscape = evaluator.landscape(current)
    best = [row[:] for row in current]
    best_landscape = dict(current_landscape)
    accepted = 0
    improvements = 0

    for iteration in range(1, iterations + 1):
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            seed_index = ((iteration - 1) // restart_every) % min(len(seeds), 12)
            current = [row[:] for row in seeds[seed_index]]
            current_landscape = evaluator.landscape(current)

        candidate = mutate(
            current,
            current_landscape["parkable_triple_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_landscape = evaluator.landscape(candidate)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective(candidate_landscape) - objective(current_landscape)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            accepted += 1

        candidate_key = best_key(candidate_landscape)
        prior_best_key = best_key(best_landscape)
        if candidate_key < prior_best_key:
            best = [row[:] for row in candidate]
            best_landscape = dict(candidate_landscape)
            improvements += 1
            record = {
                "iteration": iteration,
                "elapsed_seconds": round(time.time() - started, 6),
                "random_seed": random_seed,
                "values": best,
                **best_landscape,
            }
            append_jsonl(trace_path, record)
            print(
                f"iteration={iteration} count={candidate_key[0]} "
                f"max_floater={candidate_key[1]} "
                f"normalized_margin={candidate_key[3]:.6f}",
                flush=True,
            )
            if candidate_key[0] == 0:
                break

    status = "CHECKPOINT"
    independent_audit = None
    if best_landscape["parkable_triple_count"] == 0:
        exact = core.landscape(best, sample_limit=0)
        base_first = independent.enumerate_base_first(best)
        completion_first = independent.enumerate_completion_first(best)
        complete = independent.count_complete_efx0(best)
        if (
            exact["parkable_triple_count"] != 0
            or base_first
            or completion_first
            or exact["complete_efx0_count"] != complete
        ):
            raise AssertionError("zero candidate failed independent terminal audit")
        status = "ZERO_PARKABLE_TRIPLES"
        independent_audit = {
            "core_landscape": exact,
            "base_first_parkable_triples": len(base_first),
            "completion_first_parkable_triples": len(completion_first),
            "complete_efx0_count": complete,
        }

    result = {
        "schema": SCHEMA,
        "status": status,
        "seed_trace": str(seed_trace.resolve()),
        "seed_trace_sha256": hashlib.sha256(seed_trace.read_bytes()).hexdigest(),
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
    parser.add_argument("--seed-trace", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--restart-every", type=int, default=5_000)
    parser.add_argument("--initial-temperature", type=float, default=2.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_trace=args.seed_trace,
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
