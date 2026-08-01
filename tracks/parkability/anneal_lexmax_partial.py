#!/usr/bin/env python3
"""Adversarial search against the lex-max one-unallocated completion lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from . import core
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .anneal_efx import load_seed_values
    from .fast_count import FastParkability
except ImportError:
    import core
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_efx import load_seed_values
    from fast_count import FastParkability


SCHEMA = "lexmax-one-unallocated-anneal-v1"


def exact_lexmax_audit(
    values: list[list[int]],
    agent_order: tuple[int, ...],
) -> dict:
    candidates = []
    for floater in range(len(values[0])):
        for base in core.iter_efx_bases(values, floater):
            if all(
                base["own_values"][observer] >= values[observer][floater]
                for observer in range(len(values))
            ):
                utilities = tuple(base["own_values"])
                candidates.append({
                    "floater": floater,
                    "base_owner": base["base_owner"],
                    "utilities": list(utilities),
                    "key": tuple(utilities[observer] for observer in agent_order),
                    "parkable_hosts": base["parkable_hosts"],
                })
    if not candidates:
        return {
            "eligible_base_count": 0,
            "lexmax_key": None,
            "lexmax_base_count": 0,
            "lexmax_insertable_count": 0,
        }
    best_key = max(candidate["key"] for candidate in candidates)
    best = [
        candidate
        for candidate in candidates
        if candidate["key"] == best_key
    ]
    return {
        "eligible_base_count": len(candidates),
        "lexmax_key": list(best_key),
        "lexmax_base_count": len(best),
        "lexmax_insertable_count": sum(
            bool(candidate["parkable_hosts"]) for candidate in best
        ),
        "lexmax_bases": [
            {
                key: value
                for key, value in candidate.items()
                if key != "key"
            }
            for candidate in best
        ],
    }


def run(
    *,
    seed_paths: list[Path],
    iterations: int,
    random_seed: int,
    restart_every: int,
    initial_temperature: float,
    final_temperature: float,
    agent_order: tuple[int, ...],
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
        raise ValueError("valid seeds, iteration counts, and temperatures are required")
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output and trace paths must be new")
    seeds = [
        values
        for path in seed_paths
        for values in load_seed_values(path)
        if not has_universal_min(values)
    ]
    if not seeds:
        raise ValueError("all seeds have a universal minimum")
    n = len(seeds[0])
    m = len(seeds[0][0])
    if (
        sorted(agent_order) != list(range(n))
        or any(len(values) != n or len(values[0]) != m for values in seeds)
    ):
        raise ValueError("agent order and seed dimensions must agree")
    evaluator = FastParkability(n, m)

    def evaluate(values: list[list[int]]) -> dict:
        result = evaluator.lexmax_one_unallocated_landscape(
            values,
            agent_order=agent_order,
        )
        if result["best_lexmax_host_normalized_margin"] is None:
            raise AssertionError("profile has no eligible one-unallocated EFX base")
        return result

    seeds.sort(
        key=lambda values: evaluate(values)["best_lexmax_host_normalized_margin"]
    )
    rng = random.Random(random_seed)
    started = time.time()
    current = [row[:] for row in seeds[0]]
    current_landscape = evaluate(current)
    best = [row[:] for row in current]
    best_landscape = dict(current_landscape)
    accepted = 0
    improvements = 0

    for iteration in range(1, iterations + 1):
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            seed_index = ((iteration - 1) // restart_every) % len(seeds)
            current = [row[:] for row in seeds[seed_index]]
            current_landscape = evaluate(current)
        candidate = mutate(
            current,
            current_landscape["lexmax_insertable_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_landscape = evaluate(candidate)
        current_score = current_landscape[
            "best_lexmax_host_normalized_margin"
        ]
        candidate_score = candidate_landscape[
            "best_lexmax_host_normalized_margin"
        ]
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = candidate_score - current_score
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            accepted += 1
        if candidate_score < best_landscape[
            "best_lexmax_host_normalized_margin"
        ]:
            best = [row[:] for row in candidate]
            best_landscape = dict(candidate_landscape)
            improvements += 1
            append_jsonl(
                trace_path,
                {
                    "iteration": iteration,
                    "elapsed_seconds": round(time.time() - started, 6),
                    "values": best,
                    **best_landscape,
                },
            )
            print(
                f"iteration={iteration} "
                f"lexmax_margin="
                f"{best_landscape['best_lexmax_host_normalized_margin']:.9f} "
                f"insertable={best_landscape['lexmax_insertable_count']}",
                flush=True,
            )
            if best_landscape["lexmax_insertable_count"] == 0:
                break

    exact = exact_lexmax_audit(best, agent_order)
    if (
        exact["eligible_base_count"] != best_landscape["eligible_base_count"]
        or exact["lexmax_key"] != best_landscape["lexmax_utility_key"]
        or exact["lexmax_base_count"] != best_landscape["lexmax_base_count"]
        or exact["lexmax_insertable_count"]
        != best_landscape["lexmax_insertable_count"]
    ):
        raise AssertionError("vectorized candidate failed exact lex-max replay")
    status = (
        "LEXMAX_BLOCKED_COUNTEREXAMPLE"
        if exact["lexmax_insertable_count"] == 0
        else "NO_COUNTEREXAMPLE"
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "a blocked result refutes only the lex-max direct-completion "
            "lemma, not complete EFX existence"
        ),
        "n": n,
        "m": m,
        "agent_order": list(agent_order),
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
        "exact_audit": exact,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--iterations", type=int, default=10_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--restart-every", type=int, default=2_000)
    parser.add_argument("--initial-temperature", type=float, default=0.002)
    parser.add_argument("--final-temperature", type=float, default=0.00001)
    parser.add_argument("--agent-order", default="0,1,2,3")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    order = tuple(map(int, args.agent_order.split(",")))
    result = run(
        seed_paths=args.seed,
        iterations=args.iterations,
        random_seed=args.random_seed,
        restart_every=args.restart_every,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        agent_order=order,
        output_path=args.output,
        trace_path=args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
