#!/usr/bin/env python3
"""Search against one-transfer completion from a maximum-Nash partial state."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .anneal_lexmax_all_orders import load_values
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_lexmax_all_orders import load_values
    from fast_count import FastParkability


SCHEMA = "partial-nash-completion-radius-anneal-v1"


def target_product_ratio(landscape: dict) -> float:
    target = landscape["nearest_maximum_product_completion"]
    return (
        target["utility_product"] / landscape["maximum_product"]
        if target is not None
        else 0.0
    )


def best_key(landscape: dict) -> tuple[int, int, float]:
    if landscape["maximum_product_has_insertable_realization"]:
        return 2, landscape["maximum_product_completion_target_count"], 1.0
    if not landscape["maximum_product_completion_within_radius"]:
        return 0, 0, 0.0
    return (
        1,
        landscape["maximum_product_completion_target_count"],
        target_product_ratio(landscape),
    )


def score(landscape: dict) -> float:
    category, count, ratio = best_key(landscape)
    return category * 2.0 + count * 0.02 + ratio * 0.01


def run(
    *,
    seed_path: Path,
    radius: int,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        radius < 0
        or iterations < 1
        or initial_temperature <= 0
        or final_temperature <= 0
        or output_path.exists()
        or (trace_path is not None and trace_path.exists())
    ):
        raise ValueError("valid parameters and new outputs are required")
    seed = load_values(seed_path)
    if has_universal_min(seed):
        raise ValueError("seed has a universal-minimum good")
    evaluator = FastParkability(len(seed), len(seed[0]))
    rng = random.Random(random_seed)
    current = [row[:] for row in seed]
    current_landscape = evaluator.partial_pareto_landscape(
        current,
        completion_radius=radius,
    )
    best = [row[:] for row in current]
    best_landscape = current_landscape
    accepted = 0
    improvements = 0
    started = time.time()

    for iteration in range(1, iterations + 1):
        candidate = mutate(
            current,
            current_landscape["eligible_base_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_landscape = evaluator.partial_pareto_landscape(
            candidate,
            completion_radius=radius,
        )
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = score(candidate_landscape) - score(current_landscape)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            accepted += 1
        if best_key(candidate_landscape) < best_key(best_landscape):
            best = [row[:] for row in candidate]
            best_landscape = candidate_landscape
            improvements += 1
            append_jsonl(
                trace_path,
                {
                    "iteration": iteration,
                    "elapsed_seconds": round(time.time() - started, 6),
                    "values": best,
                    "maximum_product_has_insertable_realization": (
                        best_landscape[
                            "maximum_product_has_insertable_realization"
                        ]
                    ),
                    "completion_target_count": best_landscape[
                        "maximum_product_completion_target_count"
                    ],
                    "target_product_ratio": target_product_ratio(best_landscape),
                },
            )
            print(
                f"iteration={iteration} "
                f"max_insertable={best_landscape['maximum_product_has_insertable_realization']} "
                f"targets={best_landscape['maximum_product_completion_target_count']} "
                f"ratio={target_product_ratio(best_landscape):.9f}",
                flush=True,
            )
            if (
                not best_landscape[
                    "maximum_product_has_insertable_realization"
                ]
                and not best_landscape[
                    "maximum_product_completion_within_radius"
                ]
            ):
                break

    counterexample = (
        not best_landscape["maximum_product_has_insertable_realization"]
        and not best_landscape["maximum_product_completion_within_radius"]
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "COMPLETION_RADIUS_COUNTEREXAMPLE"
            if counterexample
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes only the stated bounded completion "
            "repair, not complete additive EFX; exact replay is still required."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "n": len(best),
        "m": len(best[0]),
        "radius": radius,
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "values": best,
        "landscape": best_landscape,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.002)
    parser.add_argument("--final-temperature", type=float, default=0.0000001)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        radius=args.radius,
        iterations=args.iterations,
        random_seed=args.random_seed,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        output_path=args.output,
        trace_path=args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
