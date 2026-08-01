#!/usr/bin/env python3
"""Adversarial search against existential-order lex-max completion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

try:
    from . import core
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .fast_count import FastParkability
except ImportError:
    import core
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from fast_count import FastParkability


SCHEMA = "lexmax-all-agent-orders-anneal-v1"


def load_values(path: Path) -> list[list[int]]:
    document = json.loads(path.read_text())
    raw = document.get("candidate_values", document.get("values"))
    if raw is None:
        raw = document.get("positive_nondegenerate_lift", {}).get("values")
    if raw is None:
        raise ValueError(f"{path} contains no valuation matrix")
    return [
        list(row)
        for row in core.validate_values(raw, lower=1)
    ]


def score(landscape: dict) -> float:
    return (
        landscape["insertable_agent_order_count"]
        + landscape["best_rescue_order_normalized_margin"]
    )


def best_key(landscape: dict) -> tuple[int, float]:
    return (
        landscape["insertable_agent_order_count"],
        landscape["best_rescue_order_normalized_margin"],
    )


def exact_all_orders(
    values: list[list[int]],
) -> dict:
    candidates = []
    for floater in range(len(values[0])):
        for base in core.iter_efx_bases(values, floater):
            utilities = tuple(base["own_values"])
            if all(
                utilities[observer] >= values[observer][floater]
                for observer in range(len(values))
            ):
                candidates.append(
                    {
                        "floater": floater,
                        "base_owner": base["base_owner"],
                        "utilities": utilities,
                        "insertable": bool(base["parkable_hosts"]),
                    }
                )
    records = []
    for order in itertools.permutations(range(len(values))):
        best_key = max(
            tuple(candidate["utilities"][agent] for agent in order)
            for candidate in candidates
        )
        best = [
            candidate
            for candidate in candidates
            if tuple(candidate["utilities"][agent] for agent in order)
            == best_key
        ]
        records.append(
            {
                "agent_order": list(order),
                "eligible_base_count": len(candidates),
                "lexmax_key": list(best_key),
                "lexmax_base_count": len(best),
                "lexmax_insertable_count": sum(
                    candidate["insertable"] for candidate in best
                ),
            }
        )
    return {
        "agent_order_count": len(records),
        "insertable_agent_order_count": sum(
            record["lexmax_insertable_count"] > 0
            for record in records
        ),
        "blocked_agent_order_count": sum(
            record["lexmax_insertable_count"] == 0
            for record in records
        ),
        "records": records,
    }


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
    n = len(seed)
    m = len(seed[0])
    evaluator = FastParkability(n, m)
    rng = random.Random(random_seed)
    current = [row[:] for row in seed]
    current_landscape = evaluator.lexmax_all_agent_orders_landscape(current)
    best = [row[:] for row in current]
    best_landscape = current_landscape
    accepted = 0
    improvements = 0
    started = time.time()

    for iteration in range(1, iterations + 1):
        candidate = mutate(
            current,
            21 + current_landscape["insertable_agent_order_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_landscape = evaluator.lexmax_all_agent_orders_landscape(
            candidate
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
                    "insertable_agent_order_count": best_landscape[
                        "insertable_agent_order_count"
                    ],
                    "blocked_agent_order_count": best_landscape[
                        "blocked_agent_order_count"
                    ],
                    "best_rescue_order_normalized_margin": best_landscape[
                        "best_rescue_order_normalized_margin"
                    ],
                },
            )
            print(
                f"iteration={iteration} "
                f"insertable_orders="
                f"{best_landscape['insertable_agent_order_count']} "
                f"best_rescue_margin="
                f"{best_landscape['best_rescue_order_normalized_margin']:.9f}",
                flush=True,
            )
            if best_landscape["insertable_agent_order_count"] == 0:
                break

    exact = exact_all_orders(best)
    if (
        exact["insertable_agent_order_count"]
        != best_landscape["insertable_agent_order_count"]
        or exact["blocked_agent_order_count"]
        != best_landscape["blocked_agent_order_count"]
    ):
        raise AssertionError("vectorized all-order endpoint failed exact replay")
    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_ORDERS_BLOCKED_COUNTEREXAMPLE"
            if exact["insertable_agent_order_count"] == 0
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "an all-orders-blocked result refutes only existential-order "
            "lex-max direct completion, not complete EFX existence"
        ),
        "n": n,
        "m": m,
        "seed_path": str(seed_path.resolve()),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
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
    parser.add_argument("--iterations", type=int, default=5_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=1.0)
    parser.add_argument("--final-temperature", type=float, default=0.001)
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
