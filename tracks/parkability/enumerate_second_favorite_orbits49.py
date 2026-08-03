#!/usr/bin/env python3
"""Enumerate top-two ranking orbits in the favorite-211 4x9 cell."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


N = 4
M = 9
FAVORITES = (0, 0, 1, 2)
UNUSED = tuple(range(3, M))


def transform(
    pattern: tuple[int, ...],
    *,
    swap_shared_agents: bool,
    swap_unique_favorites: bool,
    unused_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    agent_map = [1, 0, 2, 3] if swap_shared_agents else [0, 1, 2, 3]
    if swap_unique_favorites:
        agent_map[2], agent_map[3] = agent_map[3], agent_map[2]
    good_map = {
        0: 0,
        1: 2 if swap_unique_favorites else 1,
        2: 1 if swap_unique_favorites else 2,
        **dict(zip(UNUSED, unused_permutation)),
    }
    result = [None] * N
    for old_agent in range(N):
        result[agent_map[old_agent]] = good_map[pattern[old_agent]]
    return tuple(result)


def orbit(pattern: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        transform(
            pattern,
            swap_shared_agents=swap_shared,
            swap_unique_favorites=swap_unique,
            unused_permutation=unused_permutation,
        )
        for swap_shared in (False, True)
        for swap_unique in (False, True)
        for unused_permutation in itertools.permutations(UNUSED)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be new")
    patterns = {
        pattern
        for pattern in itertools.product(range(M), repeat=N)
        if all(
            pattern[agent] != FAVORITES[agent]
            for agent in range(N)
        )
    }
    unseen = set(patterns)
    records = []
    while unseen:
        seed = min(unseen)
        members = orbit(seed)
        if not members <= patterns:
            raise AssertionError("symmetry left the second-favorite cell")
        unseen -= members
        records.append({
            "representative": list(min(members)),
            "orbit_size": len(members),
        })
    records.sort(key=lambda record: record["representative"])
    if len(patterns) != 4096 or len(records) != 57:
        raise AssertionError("top-two orbit census changed")
    result = {
        "schema": "favorite-211-second-orbits-v1",
        "n": N,
        "m": M,
        "favorite_pattern": list(FAVORITES),
        "raw_second_favorite_pattern_count": len(patterns),
        "symmetry_group_order": 2 * 2 * 720,
        "orbit_count": len(records),
        "orbits": records,
        "sound_runner_configuration": {
            "favorite_pattern_stabilizer": False,
            "ranking_prefix_stabilizer": True,
            "reason": (
                "after fixing an orbit representative, only permutations "
                "preserving the full top-two prefixes remain valid"
            ),
        },
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
