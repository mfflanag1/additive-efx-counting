#!/usr/bin/env python3
"""Search for a maximum-Nash state defeating radius-one Hall completion."""

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
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .anneal_lexmax_all_orders import load_values
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_lexmax_all_orders import load_values
    from fast_count import FastParkability


SCHEMA = "partial-hall-completion-anneal-v1"


def candidate_partitions(state, n, m):
    old_owner = {}
    for bundle, mask in enumerate(state["masks"]):
        for good in range(m):
            if mask & (1 << good):
                old_owner[good] = bundle
    moves = [(None, None)] + [
        (good, destination)
        for good, source in old_owner.items()
        for destination in range(n)
        if destination != source
    ]
    seen = set()
    for floater_host in range(n):
        for good, destination in moves:
            masks = list(state["masks"])
            masks[floater_host] |= 1 << state["floater"]
            source = None
            if good is not None:
                source = old_owner[good]
                masks[source] ^= 1 << good
                masks[destination] |= 1 << good
            masks = tuple(masks)
            if 0 in masks or masks in seen:
                continue
            seen.add(masks)
            yield {
                "floater_host": floater_host,
                "moved_good": good,
                "move_source": source,
                "move_destination": destination,
                "masks": masks,
            }


def radius_one_landscape(values, state):
    n = len(values)
    m = len(values[0])
    subset_count = 1 << m
    totals = [[0] * subset_count for _ in range(n)]
    thresholds = [[0] * subset_count for _ in range(n)]
    minima = [[0] * subset_count for _ in range(n)]
    for agent, row in enumerate(values):
        for mask in range(1, subset_count):
            bit = mask & -mask
            good = bit.bit_length() - 1
            rest = mask ^ bit
            totals[agent][mask] = totals[agent][rest] + row[good]
            minima[agent][mask] = (
                row[good] if rest == 0 else min(minima[agent][rest], row[good])
            )
            thresholds[agent][mask] = totals[agent][mask] - minima[agent][mask]
    row_totals = [sum(row) for row in values]
    best_slack = -math.inf
    best = None
    completion_count = 0
    completion_witnesses = []
    partition_count = 0
    for move in candidate_partitions(state, n, m):
        partition_count += 1
        masks = move["masks"]
        partition_completable = False
        for matching in itertools.permutations(range(n)):
            constraint_slacks = [
                (
                    totals[agent][masks[matching[agent]]]
                    - thresholds[agent][masks[target]]
                ) / row_totals[agent]
                for agent in range(n)
                for target in range(n)
                if target != matching[agent]
            ]
            slack = min(constraint_slacks)
            if slack > best_slack:
                best_slack = slack
                best = {
                    **move,
                    "masks": list(masks),
                    "matching": list(matching),
                    "normalized_minimum_slack": slack,
                }
            if slack >= 0:
                partition_completable = True
                exact_constraints = [
                    {
                        "agent": agent,
                        "target_bundle": target,
                        "slack": (
                            totals[agent][masks[matching[agent]]]
                            - thresholds[agent][masks[target]]
                        ),
                        "row_total": row_totals[agent],
                    }
                    for agent in range(n)
                    for target in range(n)
                    if target != matching[agent]
                ]
                minimum_exact_constraints = [
                    constraint
                    for constraint in exact_constraints
                    if constraint["slack"] / constraint["row_total"] == slack
                ]
                completion_witnesses.append(
                    {
                        **move,
                        "masks": list(masks),
                        "matching": list(matching),
                        "normalized_minimum_slack": slack,
                        "minimum_constraints": minimum_exact_constraints,
                    }
                )
                break
        completion_count += partition_completable
    return {
        "candidate_partition_count": partition_count,
        "completable_partition_count": completion_count,
        "completion_witnesses": completion_witnesses,
        "best_normalized_slack": best_slack,
        "best_witness": best,
    }


def evaluate(values, evaluator):
    nash = evaluator.partial_linear_potential_landscape(
        values, potential="normalized_nash"
    )
    winners = []
    for winner in nash["maximizers"]:
        state = {
            **winner,
            "masks": tuple(
                int(mask)
                for mask in evaluator.base_masks[winner["floater"]][
                    winner["base_index"]
                ]
            ),
        }
        winners.append({**state, "radius_one": radius_one_landscape(values, state)})
    return {
        "eligible_state_count": nash["eligible_base_count"],
        "maximum_product": nash["max_potential"],
        "winner_count": len(winners),
        "has_direct_insertion": any(winner["insertable"] for winner in winners),
        "best_winner_normalized_slack": max(
            winner["radius_one"]["best_normalized_slack"] for winner in winners
        ),
        "has_radius_one_completion": any(
            winner["radius_one"]["completable_partition_count"] > 0
            for winner in winners
        ),
        "winners": winners,
    }


def objective_key(record):
    return (
        int(record["has_direct_insertion"]),
        record["best_winner_normalized_slack"],
    )


def objective_score(record):
    category, slack = objective_key(record)
    return 2.0 * category + slack


def run(
    seed_path,
    iterations,
    random_seed,
    initial_temperature,
    final_temperature,
    output_path,
    trace_path,
):
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output paths must be new")
    seed = load_values(seed_path)
    evaluator = FastParkability(len(seed), len(seed[0]))
    rng = random.Random(random_seed)
    current = [row[:] for row in seed]
    current_record = evaluate(current, evaluator)
    best = [row[:] for row in current]
    best_record = current_record
    accepted = 0
    improvements = 0
    started = time.time()
    for iteration in range(1, iterations + 1):
        candidate = mutate(current, current_record["eligible_state_count"], rng)
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_record = evaluate(candidate, evaluator)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective_score(candidate_record) - objective_score(current_record)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_record = candidate_record
            accepted += 1
        if objective_key(candidate_record) < objective_key(best_record):
            best = [row[:] for row in candidate]
            best_record = candidate_record
            improvements += 1
            trace = {
                "iteration": iteration,
                "elapsed_seconds": round(time.time() - started, 6),
                "values": best,
                "best_winner_normalized_slack": best_record[
                    "best_winner_normalized_slack"
                ],
                "has_radius_one_completion": best_record[
                    "has_radius_one_completion"
                ],
                "has_direct_insertion": best_record["has_direct_insertion"],
            }
            append_jsonl(trace_path, trace)
            print(json.dumps(trace, sort_keys=True), flush=True)
            if not best_record["has_radius_one_completion"]:
                break
    result = {
        "schema": SCHEMA,
        "status": (
            "RADIUS_ONE_HALL_COUNTEREXAMPLE"
            if not best_record["has_radius_one_completion"]
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes maximum-Nash radius-one Hall completion, "
            "not complete additive EFX."
        ),
        "seed_path": str(seed_path),
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
        "landscape": best_record,
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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        args.seed,
        args.iterations,
        args.random_seed,
        args.initial_temperature,
        args.final_temperature,
        args.output,
        args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
