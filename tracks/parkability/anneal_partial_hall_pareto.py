#!/usr/bin/env python3
"""Promote a fixed radius-one Hall obstruction toward Pareto maximality."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

import numpy as np

try:
    from .anneal import append_jsonl, atomic_json
    from .anneal_partial_hall_completion import radius_one_landscape
    from .anneal_partial_hall_maximality import fixed_state, local_mutate
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json
    from anneal_partial_hall_completion import radius_one_landscape
    from anneal_partial_hall_maximality import fixed_state, local_mutate
    from fast_count import FastParkability


SCHEMA = "partial-hall-pareto-anneal-v1"


def evaluate(values, state, evaluator):
    matrix = np.asarray(values, dtype=np.int64)
    totals, thresholds = evaluator._tables(values)
    candidate = np.asarray(
        [totals[agent, state["masks"][agent]] for agent in range(4)],
        dtype=np.int64,
    )
    for agent in range(4):
        if candidate[agent] < matrix[agent, state["floater"]]:
            return None
        for target in range(4):
            if agent != target and candidate[agent] < thresholds[
                agent, state["masks"][target]
            ]:
                return None
    radius = radius_one_landscape(
        values, {**state, "utilities": tuple(int(value) for value in candidate)}
    )
    if radius["completable_partition_count"]:
        return None

    dominators = []
    eligible_count = 0
    for floater, masks in enumerate(evaluator.base_masks):
        valid = np.ones(len(masks), dtype=bool)
        own_values = np.empty((len(masks), 4), dtype=np.int64)
        for agent in range(4):
            own = totals[agent, masks[:, agent]]
            own_values[:, agent] = own
            valid &= own >= matrix[agent, floater]
            for target in range(4):
                if agent != target:
                    valid &= own >= thresholds[agent, masks[:, target]]
        indices = np.flatnonzero(valid)
        eligible_count += len(indices)
        if not len(indices):
            continue
        dominates = np.all(own_values[indices] >= candidate[None, :], axis=1)
        dominates &= np.any(own_values[indices] > candidate[None, :], axis=1)
        for offset in np.flatnonzero(dominates):
            index = int(indices[offset])
            utilities = tuple(int(value) for value in own_values[index])
            dominators.append(
                {
                    "floater": floater,
                    "base_index": index,
                    "utilities": list(utilities),
                    "total_normalized_surplus": sum(
                        (utilities[agent] - int(candidate[agent])) / sum(values[agent])
                        for agent in range(4)
                    ),
                }
            )
    dominators.sort(
        key=lambda record: record["total_normalized_surplus"], reverse=True
    )
    return {
        "eligible_state_count": eligible_count,
        "candidate_utilities": [int(value) for value in candidate],
        "dominator_count": len(dominators),
        "strongest_dominator_normalized_surplus": (
            dominators[0]["total_normalized_surplus"] if dominators else 0.0
        ),
        "strongest_dominator": dominators[0] if dominators else None,
        "dominators": dominators if len(dominators) <= 20 else None,
        "radius_one": radius,
    }


def objective(record):
    return (
        record["dominator_count"],
        record["strongest_dominator_normalized_surplus"],
    )


def score(record):
    return math.log1p(record["dominator_count"]) + record[
        "strongest_dominator_normalized_surplus"
    ]


def run(seed_path, iterations, random_seed, initial_temperature, final_temperature, max_delta, output_path, trace_path):
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output paths must be new")
    document = json.loads(seed_path.read_text())
    current = [list(row) for row in document["values"]]
    state = fixed_state(document)
    evaluator = FastParkability(4, len(current[0]))
    current_record = evaluate(current, state, evaluator)
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
        candidate_record = evaluate(candidate, state, evaluator)
        if candidate_record is None:
            continue
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = score(candidate_record) - score(current_record)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_record = candidate_record
            accepted += 1
        if objective(candidate_record) < objective(best_record):
            best = [row[:] for row in candidate]
            best_record = candidate_record
            improvements += 1
            update = {
                "iteration": iteration,
                "elapsed_seconds": round(time.time() - started, 6),
                "dominator_count": best_record["dominator_count"],
                "strongest_dominator_normalized_surplus": best_record[
                    "strongest_dominator_normalized_surplus"
                ],
                "values": best,
            }
            append_jsonl(trace_path, update)
            print(json.dumps(update, sort_keys=True), flush=True)
            if not best_record["dominator_count"]:
                break
    result = {
        "schema": SCHEMA,
        "status": (
            "PARETO_RADIUS_ONE_COUNTEREXAMPLE"
            if not best_record["dominator_count"]
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes Pareto-maximal radius-one Hall completion, "
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
        "audit": best_record,
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.02)
    parser.add_argument("--final-temperature", type=float, default=0.000001)
    parser.add_argument("--max-delta", type=int, default=100)
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
