#!/usr/bin/env python3
"""Promote a fixed Hall obstruction toward normalized-utilitarian maximality."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import append_jsonl, atomic_json
    from .anneal_partial_hall_completion import radius_one_landscape
    from .anneal_partial_hall_maximality import fixed_eligible, fixed_state, local_mutate
    from .fast_count import FastParkability
except ImportError:
    from anneal import append_jsonl, atomic_json
    from anneal_partial_hall_completion import radius_one_landscape
    from anneal_partial_hall_maximality import fixed_eligible, fixed_state, local_mutate
    from fast_count import FastParkability


SCHEMA = "partial-hall-utilitarian-maximality-anneal-v1"


def score(values, masks, utilities, potential):
    row_totals = tuple(map(sum, values))
    if potential == "normalized_utilitarian":
        numerators = utilities
    elif potential == "normalized_threshold":
        numerators = []
        for agent, mask in enumerate(masks):
            bundle = [
                good
                for good in range(len(values[0]))
                if mask & (1 << good)
            ]
            numerators.append(
                sum(values[agent][good] for good in bundle)
                - min(values[agent][good] for good in bundle)
                if bundle
                else 0
            )
    else:
        raise ValueError("unknown potential")
    return sum(
        (
            Fraction(numerator, total)
            for numerator, total in zip(numerators, row_totals)
        ),
        Fraction(),
    )


def record(values, state, evaluator, potential):
    eligible = fixed_eligible(values, state, evaluator)
    if eligible is None:
        return None
    radius = radius_one_landscape(values, eligible)
    if radius["completable_partition_count"] > 0:
        return None
    landscape = evaluator.partial_linear_potential_landscape(
        values, potential=potential
    )
    candidate_score = score(
        values, state["masks"], eligible["utilities"], potential
    )
    maximum_winners = [
        {
            "floater": winner["floater"],
            "masks": [
                int(mask)
                for mask in evaluator.base_masks[winner["floater"]][
                    winner["base_index"]
                ]
            ],
            "hall_insertable": winner["hall_insertable"],
        }
        for winner in landscape["maximizers"]
    ]
    maximum_score = max(
        score(
            values,
            winner["masks"],
            next(
                source["utilities"]
                for source in landscape["maximizers"]
                if source["floater"] == winner["floater"]
                and [
                    int(mask)
                    for mask in evaluator.base_masks[source["floater"]][
                        source["base_index"]
                    ]
                ]
                == winner["masks"]
            ),
            potential,
        )
        for winner in maximum_winners
    )
    return {
        "eligible_state_count": landscape["eligible_base_count"],
        "candidate_utilities": list(eligible["utilities"]),
        "candidate_score": {
            "numerator": candidate_score.numerator,
            "denominator": candidate_score.denominator,
        },
        "maximum_score": {
            "numerator": maximum_score.numerator,
            "denominator": maximum_score.denominator,
        },
        "candidate_to_maximum_ratio": float(candidate_score / maximum_score),
        "is_global_maximizer": candidate_score == maximum_score,
        "all_global_maximizers_hall_blocked": (
            landscape["hall_insertable_maximizer_count"] == 0
        ),
        "hall_insertable_global_maximizer_count": landscape[
            "hall_insertable_maximizer_count"
        ],
        "global_maximizer_count": len(landscape["maximizers"]),
        "global_maximizers": maximum_winners,
        "radius_one": radius,
    }


def seed_values(document):
    if document.get("values") is not None:
        return [list(row) for row in document["values"]]
    if document.get("trace"):
        return [list(row) for row in document["trace"][-1]["values"]]
    raise ValueError("seed has no valuation matrix")


def guided_mutate(values, state, current_record, rng, max_delta):
    winner = rng.choice(current_record["global_maximizers"])
    agent_order = list(range(len(values)))
    rng.shuffle(agent_order)
    for agent in agent_order:
        donor_mask = winner["masks"][agent] & ~state["masks"][agent]
        recipient_mask = state["masks"][agent] & ~winner["masks"][agent]
        donors = [
            good
            for good in range(len(values[0]))
            if donor_mask & (1 << good) and values[agent][good] > 1
        ]
        recipients = [
            good
            for good in range(len(values[0]))
            if recipient_mask & (1 << good)
        ]
        if not donors or not recipients:
            continue
        source = rng.choice(donors)
        destination = rng.choice(recipients)
        delta = rng.randrange(
            1, min(values[agent][source] - 1, max_delta) + 1
        )
        candidate = [row[:] for row in values]
        candidate[agent][source] -= delta
        candidate[agent][destination] += delta
        return candidate
    return local_mutate(values, rng, max_delta)


def run(
    seed_path,
    iterations,
    random_seed,
    initial_temperature,
    final_temperature,
    max_delta,
    output_path,
    trace_path,
    guided_probability,
    potential,
):
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output paths must be new")
    if not 0 <= guided_probability <= 1:
        raise ValueError("guided probability must lie in [0,1]")
    document = json.loads(seed_path.read_text())
    current = seed_values(document)
    state = fixed_state(document)
    evaluator = FastParkability(4, len(current[0]))
    current_record = record(current, state, evaluator, potential)
    if current_record is None:
        raise ValueError("seed does not preserve the fixed radius-one obstruction")
    best = [row[:] for row in current]
    best_record = current_record
    rng = random.Random(random_seed)
    accepted = 0
    improvements = 0
    started = time.time()
    for iteration in range(1, iterations + 1):
        candidate = (
            guided_mutate(
                current, state, current_record, rng, max_delta
            )
            if rng.random() < guided_probability
            else local_mutate(current, rng, max_delta)
        )
        if candidate == current:
            continue
        candidate_record = record(candidate, state, evaluator, potential)
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
            if best_record["all_global_maximizers_hall_blocked"]:
                break
    result = {
        "schema": SCHEMA,
        "status": (
            "THRESHOLD_MAXIMAL_HALL_COUNTEREXAMPLE"
            if best_record["all_global_maximizers_hall_blocked"]
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes the stated potential-maximal Hall "
            "selector, not complete additive EFX."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "max_delta": max_delta,
        "guided_probability": guided_probability,
        "potential": potential,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "fixed_state": state,
        "values": best,
        "fixed_obstruction_record": best_record,
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
    parser.add_argument("--guided-probability", type=float, default=0.8)
    parser.add_argument(
        "--potential",
        choices=("normalized_utilitarian", "normalized_threshold"),
        default="normalized_utilitarian",
    )
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
        args.guided_probability,
        args.potential,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
