#!/usr/bin/env python3
"""Search for a counterexample to lexicographic owner-floor completion."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_distinct_half_floor_exchange import (
        efx_violations,
        floor_matchings,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    from anneal import atomic_json
    from analyze_distinct_half_floor_exchange import (
        efx_violations,
        floor_matchings,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-lex-floor-search-v1"
N = 4


def sample_row(rng: random.Random, observer: int, upper: int) -> tuple[int, ...]:
    while True:
        favorite = rng.randrange(max(4, upper // 2), upper + 1)
        residual = [rng.randrange(1, favorite) for _ in range(8)]
        residual[observer] = rng.randrange(favorite // 2 + 1, favorite)
        ordered = sorted(residual, reverse=True)
        if (
            ordered[4] + ordered[5] + ordered[6] > favorite
            and (
                ordered[2] + ordered[6] > favorite
                or ordered[3] + ordered[4] > favorite
            )
        ):
            return (favorite, *residual)


def lex_failure(values, universe):
    states_by_host = {host: [] for host in range(N)}
    for partition in universe:
        triple_index = next(
            index for index, bundle in enumerate(partition) if len(bundle) == 3
        )
        for matching in floor_matchings(values, partition):
            host = matching.index(triple_index)
            utilities = tuple(
                sum(values[observer][good] for good in partition[matching[observer]])
                for observer in range(N)
            )
            states_by_host[host].append((utilities, partition, matching))
    for host, states in states_by_host.items():
        if not states:
            continue
        for prefix in itertools.permutations(
            observer for observer in range(N) if observer != host
        ):
            order = prefix + (host,)
            best = max(
                states,
                key=lambda state: tuple(state[0][observer] for observer in order),
            )
            utilities, partition, matching = best
            violations = efx_violations(values, partition, matching)
            if violations:
                return {
                    "host": host,
                    "priority_order": list(order),
                    "partition": [list(bundle) for bundle in partition],
                    "matching": list(matching),
                    "utilities": list(utilities),
                    "violations": violations,
                }
    return None


def run(iterations: int, upper: int, seed: int) -> dict:
    rng = random.Random(seed)
    universe = favorite_pair_balanced_universe()
    for iteration in range(1, iterations + 1):
        values = tuple(sample_row(rng, observer, upper) for observer in range(N))
        failure = lex_failure(values, universe)
        if failure is not None:
            return {
                "schema": SCHEMA,
                "status": "LEX_FLOOR_COUNTEREXAMPLE",
                "seed": seed,
                "iteration": iteration,
                "upper": upper,
                "values": [list(row) for row in values],
                "failure": failure,
                "interpretation": (
                    "This refutes only the stated lexicographic selection "
                    "rule, not the favorite-pair EFX target."
                ),
            }
    return {
        "schema": SCHEMA,
        "status": "NO_COUNTEREXAMPLE_FOUND",
        "seed": seed,
        "iterations": iterations,
        "upper": upper,
        "target_partition_count": len(universe),
        "interpretation": "Heuristic evidence only; no theorem is claimed.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--upper", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260731)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.iterations, args.upper, args.seed)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
