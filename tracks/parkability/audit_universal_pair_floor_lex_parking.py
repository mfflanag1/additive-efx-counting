#!/usr/bin/env python3
"""Executable audit of the universal pair-floor parking lemma."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
except ImportError:
    import independent
    from anneal import atomic_json


SCHEMA = "universal-pair-floor-lex-parking-audit-v1"


def pair_states(n: int):
    goods = tuple(range(2 * n + 1))
    states = set()
    for ordering in itertools.permutations(goods):
        pairs = tuple(
            tuple(sorted(ordering[2 * agent : 2 * agent + 2]))
            for agent in range(n)
        )
        states.add((pairs, ordering[-1]))
    return tuple(sorted(states))


def audit_profile(values: tuple[tuple[int, ...], ...], states) -> None:
    n = len(values)
    m = 2 * n + 1
    for row in values:
        if any(row[0] < row[good] for good in range(1, m)):
            raise AssertionError("good zero is not a common favorite")
        if any(
            row[left] + row[right] < row[0]
            for left in range(1, m)
            for right in range(left + 1, m)
        ):
            raise AssertionError("profile violates the residual pair floor")
    for host in range(n):
        order = tuple(agent for agent in range(n) if agent != host) + (host,)
        best_key = None
        best_state = None
        for pairs, floater in states:
            own = tuple(
                sum(values[agent][good] for good in pairs[agent])
                for agent in range(n)
            )
            if any(own[agent] < values[agent][0] for agent in range(n)):
                continue
            key = tuple(own[agent] for agent in order)
            if best_key is None or key > best_key:
                best_key = key
                best_state = (pairs, floater)
        if best_state is None:
            raise AssertionError("pair-floor profile has no valid state")
        pairs, floater = best_state
        assignment = [-1] * m
        for agent, pair in enumerate(pairs):
            for good in pair:
                assignment[good] = agent
        assignment[floater] = host
        if not independent.is_complete_efx0(values, assignment):
            raise AssertionError((values, host, best_state, assignment))


def exhaustive_n2_profiles():
    for flat in itertools.product((1, 2), repeat=10):
        values = (tuple(flat[:5]), tuple(flat[5:]))
        if all(
            row[0] >= max(row[1:])
            and min(
                row[left] + row[right]
                for left in range(1, 5)
                for right in range(left + 1, 5)
            )
            >= row[0]
            for row in values
        ):
            yield values


def random_profile(n: int, rng: random.Random):
    rows = []
    for _ in range(n):
        favorite = rng.randint(2, 30)
        residual = tuple(
            rng.randint((favorite + 1) // 2, favorite)
            for _ in range(2 * n)
        )
        rows.append((favorite,) + residual)
    return tuple(rows)


def audit(random_n3: int, random_n4: int, seed: int) -> dict:
    states_by_n = {n: pair_states(n) for n in (2, 3, 4)}
    exhaustive_count = 0
    for values in exhaustive_n2_profiles():
        audit_profile(values, states_by_n[2])
        exhaustive_count += 1
    rng = random.Random(seed)
    for _ in range(random_n3):
        audit_profile(random_profile(3, rng), states_by_n[3])
    for _ in range(random_n4):
        audit_profile(random_profile(4, rng), states_by_n[4])
    completed_checks = 2 * exhaustive_count + 3 * random_n3 + 4 * random_n4
    return {
        "schema": SCHEMA,
        "status": "UNIVERSAL_PAIR_FLOOR_LEX_PARKING_AUDIT_PASSED",
        "exhaustive_n2_profiles": exhaustive_count,
        "deterministic_random_n3_profiles": random_n3,
        "deterministic_random_n4_profiles": random_n4,
        "random_seed": seed,
        "valid_pair_state_counts": {
            str(n): len(states) for n, states in states_by_n.items()
        },
        "completed_allocation_checks": completed_checks,
        "claim": (
            "For every audited profile and designated last-priority host, "
            "parking the floater in a lexicographically maximal valid pair "
            "state produced complete EFX."
        ),
        "scope_warning": (
            "This is a semantic regression audit, not a substitute for the "
            "general analytic exchange proof."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-n3", type=int, default=128)
    parser.add_argument("--random-n4", type=int, default=32)
    parser.add_argument("--seed", type=int, default=20260731)
    args = parser.parse_args()
    if args.random_n3 < 0 or args.random_n4 < 0:
        parser.error("random profile counts cannot be negative")
    result = audit(args.random_n3, args.random_n4, args.seed)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
