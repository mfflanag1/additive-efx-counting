#!/usr/bin/env python3
"""Search for a blocked maximizer of a linear one-floater potential."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path

try:
    from . import core
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .anneal_lexmax_all_orders import load_values
    from .fast_count import FastParkability
except ImportError:
    import core
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_lexmax_all_orders import load_values
    from fast_count import FastParkability


SCHEMA = "partial-smooth-potential-anneal-v1"


def exact_landscape(
    values: list[list[int]],
    potential_name: str,
    penalty: Fraction,
) -> dict:
    row_totals = tuple(map(sum, values))
    candidates = []
    for floater in range(len(values[0])):
        floater_cost = penalty * sum(
            Fraction(values[agent][floater], row_totals[agent])
            for agent in range(len(values))
        )
        for base in core.iter_efx_bases(values, floater):
            utilities = tuple(base["own_values"])
            if not all(
                utilities[agent] >= values[agent][floater]
                for agent in range(len(values))
            ):
                continue
            normalized = tuple(
                Fraction(utilities[agent], row_totals[agent])
                for agent in range(len(values))
            )
            if potential_name == "linear_surplus":
                potential = sum(normalized, Fraction()) - floater_cost
            elif potential_name == "normalized_threshold":
                owner_thresholds = []
                for agent in range(len(values)):
                    bundle = tuple(
                        good
                        for good, owner in enumerate(base["base_owner"])
                        if owner == agent
                    )
                    threshold = (
                        sum(values[agent][good] for good in bundle)
                        - min(values[agent][good] for good in bundle)
                        if bundle
                        else 0
                    )
                    owner_thresholds.append(
                        Fraction(threshold, row_totals[agent])
                    )
                potential = sum(owner_thresholds, Fraction())
            elif potential_name == "normalized_nash":
                potential = math.prod(normalized)
            elif potential_name == "normalized_harmonic":
                potential = -sum(
                    (Fraction(1, share) for share in normalized),
                    Fraction(),
                )
            else:
                raise ValueError("unknown potential")
            candidates.append(
                {
                    "floater": floater,
                    "base_owner": base["base_owner"],
                    "utilities": utilities,
                    "potential": potential,
                    "parkable_hosts": tuple(base["parkable_hosts"]),
                }
            )
    if not candidates:
        raise AssertionError("profile has no eligible one-floater EFX state")
    best = max(candidate["potential"] for candidate in candidates)
    winners = [candidate for candidate in candidates if candidate["potential"] == best]
    best_margin = None
    best_hall_margin = None
    for candidate in winners:
        bundles = tuple(
            tuple(
                good
                for good, owner in enumerate(candidate["base_owner"])
                if owner == agent
            )
            for agent in range(len(values))
        )
        host_margins = []
        for host in range(len(values)):
            enlarged = bundles[host] + (candidate["floater"],)
            observer_margins = []
            for observer in range(len(values)):
                if observer == host:
                    continue
                threshold = sum(values[observer][good] for good in enlarged) - min(
                    values[observer][good] for good in enlarged
                )
                observer_margins.append(
                    Fraction(
                        candidate["utilities"][observer] - threshold,
                        row_totals[observer],
                    )
                )
            host_margins.append(min(observer_margins))
        candidate["best_host_normalized_margin"] = max(host_margins)
        if best_margin is None or candidate["best_host_normalized_margin"] > best_margin:
            best_margin = candidate["best_host_normalized_margin"]
        hall_margins = []
        for host in range(len(values)):
            complete_bundles = list(bundles)
            complete_bundles[host] = complete_bundles[host] + (
                candidate["floater"],
            )
            for permutation in itertools.permutations(range(len(values))):
                observer_margins = []
                for observer in range(len(values)):
                    assigned = permutation[observer]
                    own = sum(
                        values[observer][good]
                        for good in complete_bundles[assigned]
                    )
                    required = max(
                        (
                            sum(values[observer][good] for good in bundle)
                            - min(values[observer][good] for good in bundle)
                            if bundle
                            else 0
                        )
                        for target, bundle in enumerate(complete_bundles)
                        if target != assigned
                    )
                    observer_margins.append(
                        Fraction(own - required, row_totals[observer])
                    )
                hall_margins.append(min(observer_margins))
        candidate["best_hall_normalized_margin"] = max(hall_margins)
        if (
            best_hall_margin is None
            or candidate["best_hall_normalized_margin"] > best_hall_margin
        ):
            best_hall_margin = candidate["best_hall_normalized_margin"]
    assert best_margin is not None
    assert best_hall_margin is not None
    return {
        "eligible_base_count": len(candidates),
        "max_potential": {
            "numerator": best.numerator,
            "denominator": best.denominator,
        },
        "maximizer_count": len(winners),
        "insertable_maximizer_count": sum(
            bool(candidate["parkable_hosts"]) for candidate in winners
        ),
        "best_maximizer_host_normalized_margin": {
            "numerator": best_margin.numerator,
            "denominator": best_margin.denominator,
        },
        "hall_insertable_maximizer_count": sum(
            candidate["best_hall_normalized_margin"] >= 0
            for candidate in winners
        ),
        "best_maximizer_hall_normalized_margin": {
            "numerator": best_hall_margin.numerator,
            "denominator": best_hall_margin.denominator,
        },
        "maximizers": [
            {
                "floater": candidate["floater"],
                "base_owner": list(candidate["base_owner"]),
                "utilities": list(candidate["utilities"]),
                "parkable_hosts": list(candidate["parkable_hosts"]),
                "best_host_normalized_margin": {
                    "numerator": candidate["best_host_normalized_margin"].numerator,
                    "denominator": candidate["best_host_normalized_margin"].denominator,
                },
                "best_hall_normalized_margin": {
                    "numerator": candidate["best_hall_normalized_margin"].numerator,
                    "denominator": candidate["best_hall_normalized_margin"].denominator,
                },
            }
            for candidate in winners
        ],
    }


def selected_margin(landscape: dict, completion_mode: str) -> float:
    return landscape[
        "best_maximizer_host_normalized_margin"
        if completion_mode == "identity"
        else "best_maximizer_hall_normalized_margin"
    ]


def score(landscape: dict, completion_mode: str) -> float:
    margin = selected_margin(landscape, completion_mode)
    return margin + max(0, landscape["maximizer_count"] - 1) * 1e-6


def best_key(landscape: dict, completion_mode: str) -> tuple[bool, float, int]:
    margin = selected_margin(landscape, completion_mode)
    return margin >= 0, margin, landscape["maximizer_count"]


def run(
    *,
    seed_path: Path,
    potential_name: str,
    completion_mode: str,
    penalty: Fraction,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        penalty < 0
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
    n = len(seed)
    m = len(seed[0])
    evaluator = FastParkability(n, m)
    rng = random.Random(random_seed)
    current = [row[:] for row in seed]
    current_landscape = evaluator.partial_linear_potential_landscape(
        current,
        potential=potential_name,
        floater_penalty=float(penalty),
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
        candidate_landscape = evaluator.partial_linear_potential_landscape(
            candidate,
            potential=potential_name,
            floater_penalty=float(penalty),
        )
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = score(candidate_landscape, completion_mode) - score(
            current_landscape, completion_mode
        )
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_landscape = candidate_landscape
            accepted += 1
        if best_key(candidate_landscape, completion_mode) < best_key(
            best_landscape, completion_mode
        ):
            best = [row[:] for row in candidate]
            best_landscape = candidate_landscape
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
                f"maximizers={best_landscape['maximizer_count']} "
                f"insertable={best_landscape['insertable_maximizer_count']} "
                f"margin={selected_margin(best_landscape, completion_mode):.9f}",
                flush=True,
            )
            if selected_margin(best_landscape, completion_mode) < 0:
                break

    exact = exact_landscape(best, potential_name, penalty)
    insertable_key = (
        "insertable_maximizer_count"
        if completion_mode == "identity"
        else "hall_insertable_maximizer_count"
    )
    vectorized_insertable = best_landscape[insertable_key]
    if exact[insertable_key] != vectorized_insertable:
        raise AssertionError("vectorized endpoint failed exact potential replay")
    counterexample = exact[insertable_key] == 0
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_MAXIMIZER_COUNTEREXAMPLE" if counterexample else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "a blocked endpoint refutes only the stated partial-state "
            "potential completion lemma, not complete additive EFX"
        ),
        "n": n,
        "m": m,
        "potential": potential_name,
        "completion_mode": completion_mode,
        "floater_penalty": {
            "numerator": penalty.numerator,
            "denominator": penalty.denominator,
        },
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
    parser.add_argument(
        "--potential",
        choices=(
            "linear_surplus",
            "normalized_threshold",
            "normalized_nash",
            "normalized_harmonic",
        ),
        default="linear_surplus",
    )
    parser.add_argument("--floater-penalty", type=Fraction, default=Fraction(1))
    parser.add_argument(
        "--completion-mode", choices=("identity", "hall"), default="identity"
    )
    parser.add_argument("--iterations", type=int, default=5_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.02)
    parser.add_argument("--final-temperature", type=float, default=0.00001)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        potential_name=args.potential,
        completion_mode=args.completion_mode,
        penalty=args.floater_penalty,
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
