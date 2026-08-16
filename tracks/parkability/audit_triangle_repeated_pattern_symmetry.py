#!/usr/bin/env python3
"""Audit the 480-element symmetry break for bottom pattern two."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import (
        conversion_closure,
        pattern_conversion_orbits,
    )
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import (
        conversion_closure,
        pattern_conversion_orbits,
    )
    from decide_common_bottom_pairing_conversion import canonical_partition
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "triangle-repeated-pattern-symmetry-audit-v1"
N = 4
M = 9
FAVORITE = 0


def symmetry_actions():
    actions = []
    for repeated_agents in ((0, 1), (1, 0)):
        for reflected in (False, True):
            agents = repeated_agents + ((3, 2) if reflected else (2, 3))
            for free_goods in itertools.permutations(range(4, M)):
                goods = (
                    (0, 2, 1, 3, *free_goods)
                    if reflected
                    else (0, 1, 2, 3, *free_goods)
                )
                actions.append((agents, goods))
    if len(actions) != 480 or len(set(actions)) != 480:
        raise AssertionError("triangle-repeated symmetry action census changed")
    return tuple(actions)


def transform(values, action):
    agents, goods = action
    return tuple(
        tuple(values[agents[agent]][goods[good]] for good in range(M))
        for agent in range(N)
    )


def normalized(values):
    return tuple(
        tuple(Fraction(value, sum(row)) for value in row) for row in values
    )


def satisfies_symmetry(values):
    rows = normalized(values)
    if rows[0] < rows[1]:
        return False
    columns = tuple(
        tuple(rows[agent][good] for agent in range(N))
        for good in range(4, M)
    )
    if any(left < right for left, right in zip(columns, columns[1:])):
        return False
    reflected = transform(
        rows,
        ((0, 1, 3, 2), (0, 2, 1, 3, 4, 5, 6, 7, 8)),
    )
    return sum(rows, ()) >= sum(reflected, ())


def canonicalize(values, actions):
    return max(
        (transform(values, action) for action in actions),
        key=lambda candidate: sum(normalized(candidate), ()),
    )


def map_partition(partition, goods):
    return canonical_partition(
        *(tuple(goods[good] for good in bundle) for bundle in partition)
    )


def audit_action_invariance(actions, pattern, conversion_family):
    family = set(conversion_family)
    for agents, goods in actions:
        for new_agent, lows in enumerate(pattern):
            mapped_lows = tuple(sorted(goods[good] for good in lows))
            if mapped_lows != pattern[agents[new_agent]]:
                raise AssertionError("symmetry action changed the bottom pattern")
        if {
            map_partition(partition, goods)
            for partition in conversion_family
        } != family:
            raise AssertionError("symmetry action changed the conversion closure")


def run(output, random_profiles=128, random_seed=20260801):
    pattern = goods_pattern(2)
    selected_pairs = tuple(dict.fromkeys(pattern))
    conversion_family, source_pairing_count = conversion_closure(selected_pairs)
    actions = symmetry_actions()
    audit_action_invariance(actions, pattern, conversion_family)
    orbits = pattern_conversion_orbits(pattern, conversion_family)
    orbit_sizes = list(map(len, orbits))
    if orbit_sizes != [30, 60, 60, 15, 60]:
        raise AssertionError("triangle-repeated conversion orbits changed")

    rng = random.Random(random_seed)
    for _ in range(random_profiles):
        values = tuple(
            tuple(rng.randint(1, 100) for _ in range(M))
            for _ in range(N)
        )
        if not satisfies_symmetry(canonicalize(values, actions)):
            raise AssertionError("orbit maximum violated the symmetry cuts")

    result = {
        "schema": SCHEMA,
        "status": "TRIANGLE_REPEATED_PATTERN_SYMMETRY_AUDITED",
        "pattern_index": 2,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "group_size": len(actions),
        "goods_automorphism_count": len({goods for _, goods in actions}),
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(conversion_family),
        "conversion_orbit_sizes": orbit_sizes,
        "action_invariance_checked": True,
        "random_canonical_representatives_checked": random_profiles,
        "random_seed": random_seed,
        "claim_boundary": (
            "This deterministically checks the finite relabeling group, its "
            "bottom-pattern and conversion-family invariance, and the exact "
            "lex-leader implementation. The general WLOG step is the "
            "finite-orbit lexicographic-maximum argument."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=128)
    args = parser.parse_args()
    if args.random_profiles < 1:
        parser.error("at least one random profile is required")
    print(json.dumps(run(args.output, args.random_profiles), indent=2))


if __name__ == "__main__":
    main()
