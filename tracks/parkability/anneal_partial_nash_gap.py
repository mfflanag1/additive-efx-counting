#!/usr/bin/env python3
"""Search for a blocked maximum-Nash eligible partial EFX state."""

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
    from .audit_partial_pareto_radius_rescue import exact_rescue_audit
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_lexmax_all_orders import load_values
    from audit_partial_pareto_radius_rescue import exact_rescue_audit
    from fast_count import FastParkability


SCHEMA = "partial-nash-gap-anneal-v1"


def best_key(landscape: dict) -> tuple[int, float, int]:
    if not landscape["maximum_product_has_insertable_realization"]:
        return 0, 0.0, -landscape["blocked_pareto_frontier_utility_vector_count"]
    ratio = landscape["blocked_pareto_to_maximum_product_ratio"]
    if ratio is not None:
        return (
            1,
            1.0 - ratio,
            -landscape["blocked_pareto_frontier_utility_vector_count"],
        )
    return 2, 1.0, 0


def score(landscape: dict) -> float:
    category, gap, count = best_key(landscape)
    return category * 2.0 + gap + count * 1e-5


def run(
    *,
    seed_path: Path,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        iterations < 1
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
    current_landscape = evaluator.partial_pareto_landscape(current)
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
        candidate_landscape = evaluator.partial_pareto_landscape(candidate)
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
                    "maximum_product": best_landscape["maximum_product"],
                    "maximum_product_has_insertable_realization": (
                        best_landscape[
                            "maximum_product_has_insertable_realization"
                        ]
                    ),
                    "blocked_pareto_maximum_product": best_landscape[
                        "blocked_pareto_maximum_product"
                    ],
                    "blocked_pareto_to_maximum_product_ratio": best_landscape[
                        "blocked_pareto_to_maximum_product_ratio"
                    ],
                },
            )
            print(
                f"iteration={iteration} "
                f"blocked={best_landscape['blocked_pareto_frontier_utility_vector_count']} "
                f"ratio={best_landscape['blocked_pareto_to_maximum_product_ratio']} "
                f"max_insertable={best_landscape['maximum_product_has_insertable_realization']}",
                flush=True,
            )
            if not best_landscape[
                "maximum_product_has_insertable_realization"
            ]:
                break

    exact = exact_rescue_audit(best, len(best[0]))
    compared_keys = (
        "blocked_pareto_frontier_utility_vector_count",
        "maximum_product",
        "maximum_product_vector_count",
        "maximum_product_has_insertable_realization",
        "blocked_pareto_maximum_product",
    )
    if any(exact[key] != best_landscape[key] for key in compared_keys):
        raise AssertionError("vectorized endpoint failed exact Nash-gap replay")
    counterexample = not exact["maximum_product_has_insertable_realization"]
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_NASH_MAXIMIZER_COUNTEREXAMPLE"
            if counterexample
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes maximum-Nash direct completion, not "
            "complete additive EFX; the endpoint is exactly enumerated."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "n": len(best),
        "m": len(best[0]),
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
        "exact_audit": exact,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.01)
    parser.add_argument("--final-temperature", type=float, default=0.000001)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
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
