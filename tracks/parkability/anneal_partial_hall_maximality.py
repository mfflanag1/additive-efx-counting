#!/usr/bin/env python3
"""Promote a fixed radius-one Hall obstruction toward maximum Nash welfare."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from .anneal import append_jsonl, atomic_json
    from .anneal_partial_hall_completion import evaluate, radius_one_landscape
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json
    from anneal_partial_hall_completion import evaluate, radius_one_landscape
    from fast_count import FastParkability


SCHEMA = "partial-hall-maximality-anneal-v1"


def local_mutate(values, rng, max_delta):
    candidate = [row[:] for row in values]
    agent = rng.randrange(len(values))
    source, destination = rng.sample(range(len(values[0])), 2)
    available = candidate[agent][source] - 1
    if available < 1:
        return candidate
    delta = rng.randrange(1, min(available, max_delta) + 1)
    candidate[agent][source] -= delta
    candidate[agent][destination] += delta
    return candidate


def fixed_state(document):
    if "fixed_state" in document:
        return {
            "floater": document["fixed_state"]["floater"],
            "masks": tuple(document["fixed_state"]["masks"]),
        }
    base = document["base_bundles"]
    return {
        "floater": document["floater"],
        "masks": tuple(sum(1 << good for good in bundle) for bundle in base),
    }


def fixed_eligible(values, state, evaluator):
    totals, thresholds = evaluator._tables(values)
    utilities = tuple(
        int(totals[agent, state["masks"][agent]]) for agent in range(4)
    )
    for agent in range(4):
        if utilities[agent] < values[agent][state["floater"]]:
            return None
        for target in range(4):
            if agent != target and utilities[agent] < thresholds[
                agent, state["masks"][target]
            ]:
                return None
    return {**state, "utilities": utilities}


def record(values, state, evaluator):
    eligible = fixed_eligible(values, state, evaluator)
    if eligible is None:
        return None
    radius = radius_one_landscape(values, eligible)
    if radius["completable_partition_count"] > 0:
        return None
    nash = evaluator.partial_linear_potential_landscape(
        values, potential="normalized_nash"
    )
    candidate_product = math.prod(eligible["utilities"])
    maximum_product = max(
        math.prod(winner["utilities"]) for winner in nash["maximizers"]
    )
    return {
        "eligible_state_count": nash["eligible_base_count"],
        "candidate_utilities": list(eligible["utilities"]),
        "candidate_product": candidate_product,
        "maximum_product": maximum_product,
        "candidate_to_maximum_ratio": candidate_product / maximum_product,
        "maximum_nash_winner_count": len(nash["maximizers"]),
        "radius_one": radius,
    }


def run(seed_path, iterations, random_seed, initial_temperature, final_temperature, max_delta, output_path, trace_path):
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output paths must be new")
    document = json.loads(seed_path.read_text())
    current = [list(row) for row in document["values"]]
    state = fixed_state(document)
    evaluator = FastParkability(4, len(current[0]))
    current_record = record(current, state, evaluator)
    if current_record is None:
        raise ValueError("seed does not preserve the fixed radius-one obstruction")
    best = [row[:] for row in current]
    best_record = current_record
    rng = random.Random(random_seed)
    accepted = 0
    improvements = 0
    started = time.time()
    for iteration in range(1, iterations + 1):
        candidate = local_mutate(current, rng, max_delta)
        if candidate == current:
            continue
        candidate_record = record(candidate, state, evaluator)
        if candidate_record is None:
            continue
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        current_gap = 1.0 - current_record["candidate_to_maximum_ratio"]
        candidate_gap = 1.0 - candidate_record["candidate_to_maximum_ratio"]
        change = candidate_gap - current_gap
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_record = candidate_record
            accepted += 1
        if (
            candidate_record["candidate_to_maximum_ratio"]
            > best_record["candidate_to_maximum_ratio"]
        ):
            best = [row[:] for row in candidate]
            best_record = candidate_record
            improvements += 1
            update = {
                "iteration": iteration,
                "elapsed_seconds": round(time.time() - started, 6),
                "candidate_to_maximum_ratio": best_record[
                    "candidate_to_maximum_ratio"
                ],
                "values": best,
            }
            append_jsonl(trace_path, update)
            print(json.dumps(update, sort_keys=True), flush=True)
            if best_record["candidate_product"] == best_record["maximum_product"]:
                break

    maximum_audit = evaluate(best, evaluator)
    counterexample = not maximum_audit["has_radius_one_completion"]
    result = {
        "schema": SCHEMA,
        "status": (
            "MAXIMUM_NASH_RADIUS_ONE_COUNTEREXAMPLE"
            if counterexample
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes the maximum-Nash radius-one Hall selector, "
            "not complete additive EFX."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "max_delta": max_delta,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "fixed_state": state,
        "values": best,
        "fixed_obstruction_record": best_record,
        "maximum_nash_audit": maximum_audit,
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.01)
    parser.add_argument("--final-temperature", type=float, default=0.000001)
    parser.add_argument("--max-delta", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        args.seed,
        args.iterations,
        args.random_seed,
        args.initial_temperature,
        args.final_temperature,
        args.max_delta,
        args.output,
        args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
