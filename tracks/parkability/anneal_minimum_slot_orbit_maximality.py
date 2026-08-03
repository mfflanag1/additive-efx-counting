#!/usr/bin/env python3
"""Promote a blocked five-token orbit toward global threshold maximality."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from .anneal import append_jsonl, atomic_json
    from .anneal_partial_hall_maximality import local_mutate
    from .audit_minimum_slot_orbit import audit_orbit, exact_eligible, exact_theta
    from .fast_count import FastParkability
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        CORES,
        FLOATER,
        TOKENS,
        masks_from_bundles,
    )
except ImportError:
    from anneal import append_jsonl, atomic_json
    from anneal_partial_hall_maximality import local_mutate
    from audit_minimum_slot_orbit import audit_orbit, exact_eligible, exact_theta
    from fast_count import FastParkability
    from run_minimum_slot_orbit_cegar import (
        BASE,
        CORES,
        FLOATER,
        TOKENS,
        masks_from_bundles,
    )


SCHEMA = "minimum-slot-orbit-threshold-maximality-anneal-v1"
FIXED_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def winner_state(evaluator, winner):
    return {
        "floater": int(winner["floater"]),
        "masks": tuple(
            int(mask)
            for mask in evaluator.base_masks[winner["floater"]][
                winner["base_index"]
            ]
        ),
    }


def fraction_record(value: Fraction):
    return {"numerator": value.numerator, "denominator": value.denominator}


def record(values, evaluator):
    if any(
        values[owner][token] >= values[owner][core]
        for owner, (core, token) in enumerate(zip(CORES, TOKENS[:4]))
    ):
        return None
    if not exact_eligible(values, FIXED_STATE):
        return None
    orbit = audit_orbit(
        values,
        FIXED_STATE,
        TOKENS[:4],
        include_records=False,
    )
    if orbit["status"] != "ORBIT_ALL_ELIGIBLE_STATES_BLOCKED":
        return None

    landscape = evaluator.partial_linear_potential_landscape(
        values,
        potential="normalized_threshold",
    )
    maximizers = [winner_state(evaluator, winner) for winner in landscape["maximizers"]]
    maximum_scores = {exact_theta(values, state) for state in maximizers}
    if len(maximum_scores) != 1:
        raise AssertionError("global threshold maximizers have unequal exact scores")
    maximum_score = next(iter(maximum_scores))
    candidate_score = exact_theta(values, FIXED_STATE)
    if candidate_score > maximum_score:
        raise AssertionError("fixed state exceeds enumerated global maximum")
    return {
        "candidate_score": fraction_record(candidate_score),
        "maximum_score": fraction_record(maximum_score),
        "candidate_to_maximum_ratio": float(candidate_score / maximum_score),
        "is_global_maximizer": candidate_score == maximum_score,
        "eligible_state_count": landscape["eligible_base_count"],
        "global_maximizer_count": landscape["maximizer_count"],
        "hall_insertable_global_maximizer_count": landscape[
            "hall_insertable_maximizer_count"
        ],
        "global_maximizers": [
            {
                "floater": state["floater"],
                "masks": list(state["masks"]),
            }
            for state in maximizers
        ],
        "orbit_audit": orbit,
    }


def guided_mutate(values, current_record, rng, max_delta):
    winner = rng.choice(current_record["global_maximizers"])
    owners = list(range(len(values)))
    rng.shuffle(owners)
    for owner in owners:
        donor_mask = winner["masks"][owner] & ~FIXED_STATE["masks"][owner]
        recipient_mask = FIXED_STATE["masks"][owner] & ~winner["masks"][owner]
        donors = [
            good
            for good in range(len(values[0]))
            if donor_mask & (1 << good) and values[owner][good] > 1
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
        delta = rng.randrange(1, min(values[owner][source] - 1, max_delta) + 1)
        candidate = [row[:] for row in values]
        candidate[owner][source] -= delta
        candidate[owner][destination] += delta
        return candidate
    return local_mutate(values, rng, max_delta)


def run(
    seed_path,
    iterations,
    random_seed,
    initial_temperature,
    final_temperature,
    max_delta,
    guided_probability,
    output_path,
    trace_path,
):
    if output_path.exists() or (trace_path is not None and trace_path.exists()):
        raise ValueError("output paths must be new")
    if not 0 <= guided_probability <= 1:
        raise ValueError("guided probability must lie in [0,1]")
    document = json.loads(seed_path.read_text())
    current = [list(row) for row in document["values"]]
    evaluator = FastParkability(4, 9)
    current_record = record(current, evaluator)
    if current_record is None:
        raise ValueError("seed does not preserve an exact blocked token orbit")
    best = [row[:] for row in current]
    best_record = current_record
    rng = random.Random(random_seed)
    accepted = 0
    improvements = 0
    started = time.time()
    iteration = 0

    for iteration in range(1, iterations + 1):
        candidate = (
            guided_mutate(current, current_record, rng, max_delta)
            if rng.random() < guided_probability
            else local_mutate(current, rng, max_delta)
        )
        if candidate == current:
            continue
        candidate_record = record(candidate, evaluator)
        if candidate_record is None:
            continue
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = (
            current_record["candidate_to_maximum_ratio"]
            - candidate_record["candidate_to_maximum_ratio"]
        )
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
            if best_record["is_global_maximizer"]:
                break

    exact_replay = record(best, evaluator)
    if exact_replay != best_record:
        raise AssertionError("terminal replay did not reproduce the best record")
    result = {
        "schema": SCHEMA,
        "status": (
            "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND"
            if best_record["is_global_maximizer"]
            else "NO_GLOBAL_MAXIMUM_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes the fixed-core five-token orbit lemma at "
            "a global normalized-threshold maximum. It does not refute complete "
            "additive EFX or the existential threshold selector."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "max_delta": max_delta,
        "guided_probability": guided_probability,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "fixed_state": {
            "floater": FIXED_STATE["floater"],
            "masks": list(FIXED_STATE["masks"]),
        },
        "values": best,
        "exact_record": best_record,
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
    parser.add_argument("--max-delta", type=int, default=2048)
    parser.add_argument("--guided-probability", type=float, default=0.8)
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
        args.guided_probability,
        args.output,
        args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
