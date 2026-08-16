#!/usr/bin/env python3
"""Executable audit of the common-three lexicographic parking lemma."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .decide_common_three_anchored import (
        FAVORITE,
        HIGH_GOODS,
        LOW_GOODS,
        M,
        N,
        audit_branch,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from decide_common_three_anchored import (
        FAVORITE,
        HIGH_GOODS,
        LOW_GOODS,
        M,
        N,
        audit_branch,
    )


SCHEMA = "common-three-lex-parking-audit-v1"
ANCHORS = (FAVORITE,) + HIGH_GOODS
STATES = tuple(
    (anchors, lows[:N], lows[N])
    for anchors in itertools.permutations(ANCHORS)
    for lows in itertools.permutations(LOW_GOODS)
)


def lexmax_state(
    values: tuple[tuple[int, ...], ...],
    host: int,
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    order = tuple(agent for agent in range(N) if agent != host) + (host,)
    best_key = None
    best_state = None
    for anchors, lows, floater in STATES:
        own_values = tuple(
            values[agent][anchors[agent]] + values[agent][lows[agent]]
            for agent in range(N)
        )
        if any(
            own_values[agent] < values[agent][FAVORITE]
            for agent in range(N)
        ):
            continue
        key = tuple(own_values[agent] for agent in order)
        if best_key is None or key > best_key:
            best_key = key
            best_state = (anchors, lows, floater)
    if best_state is None:
        raise AssertionError("common-three profile has no valid pair state")
    return best_state


def complete_assignment(
    state: tuple[tuple[int, ...], tuple[int, ...], int],
    host: int,
) -> tuple[int, ...]:
    anchors, lows, floater = state
    assignment = [-1] * M
    for agent in range(N):
        assignment[anchors[agent]] = agent
        assignment[lows[agent]] = agent
    assignment[floater] = host
    if any(agent < 0 for agent in assignment):
        raise AssertionError("state did not allocate every good")
    return tuple(assignment)


def audit_profile(values: tuple[tuple[int, ...], ...]) -> None:
    audit_branch(values)
    for host in range(N):
        state = lexmax_state(values, host)
        assignment = complete_assignment(state, host)
        if not independent.is_complete_efx0(values, assignment):
            raise AssertionError((values, host, state, assignment))


def small_grid_profiles():
    rows = []
    for bad_low in (None,) + LOW_GOODS:
        lows = tuple(1 if low == bad_low else 2 for low in LOW_GOODS)
        rows.append((4, 3, 3, 3) + lows)
    yield from itertools.product(rows, repeat=N)


def random_profile(rng: random.Random) -> tuple[tuple[int, ...], ...]:
    rows = []
    for _ in range(N):
        favorite = rng.randint(4, 40)
        minimum_high = favorite - favorite // 2 + 1
        highs = tuple(
            rng.randint(minimum_high, favorite - 1)
            for _ in HIGH_GOODS
        )
        cutoff = favorite - min(highs) + 1
        lows = [
            rng.randint(cutoff, favorite // 2)
            for _ in range(len(LOW_GOODS) - 1)
        ]
        lows.append(rng.randint(1, favorite // 2))
        rng.shuffle(lows)
        rows.append((favorite,) + highs + tuple(lows))
    return tuple(rows)


def audit(random_profiles: int, seed: int) -> dict:
    grid_count = 0
    for values in small_grid_profiles():
        audit_profile(tuple(values))
        grid_count += 1
    rng = random.Random(seed)
    for _ in range(random_profiles):
        audit_profile(random_profile(rng))
    profile_count = grid_count + random_profiles
    return {
        "schema": SCHEMA,
        "status": "COMMON_THREE_LEX_PARKING_AUDIT_PASSED",
        "valid_pair_states_per_profile": len(STATES),
        "exhaustive_small_grid_profiles": grid_count,
        "deterministic_random_profiles": random_profiles,
        "random_seed": seed,
        "designated_hosts_per_profile": N,
        "completed_allocation_checks": profile_count * N,
        "claim": (
            "For every audited common-three profile and every designated "
            "last-priority host, adding the floater to a lexicographically "
            "maximal valid pair state produced a complete EFX allocation."
        ),
        "scope_warning": (
            "This is a semantic regression audit of the constructive proof, "
            "not a substitute for the cap-free exchange argument."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260731)
    args = parser.parse_args()
    if args.random_profiles < 0:
        parser.error("random profile count cannot be negative")
    result = audit(args.random_profiles, args.seed)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
