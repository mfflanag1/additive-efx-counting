#!/usr/bin/env python3
"""Audit the generic relabeling symmetry for an all-distinct pattern."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_bottom_pattern_conversion_orbits import automorphisms
    from .decide_bottom_pattern_conversion_selector import (
        add_all_distinct_pattern_symmetry,
        conversion_closure,
        pattern_conversion_orbits,
    )
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .lra_master import ParkabilityLRAMaster
    from .run_bottom_pair_pattern_selector_cegar import (
        goods_pattern,
        multiplicity_signature,
    )
except ImportError:
    from anneal import atomic_json
    from audit_bottom_pattern_conversion_orbits import automorphisms
    from decide_bottom_pattern_conversion_selector import (
        add_all_distinct_pattern_symmetry,
        conversion_closure,
        pattern_conversion_orbits,
    )
    from decide_common_bottom_pairing_conversion import canonical_partition
    from lra_master import ParkabilityLRAMaster
    from run_bottom_pair_pattern_selector_cegar import (
        goods_pattern,
        multiplicity_signature,
    )


SCHEMA = "all-distinct-pattern-symmetry-audit-v1"
N = 4
M = 9


def compose(left, right):
    return (
        tuple(left[0][right[0][agent]] for agent in range(N)),
        tuple(left[1][right[1][good]] for good in range(M)),
    )


def generated_group(generators):
    identity = (tuple(range(N)), tuple(range(M)))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            image = compose(current, generator)
            if image not in group:
                group.add(image)
                frontier.append(image)
    return group


def independent_actions(pattern):
    pair_to_agent = {pair: agent for agent, pair in enumerate(pattern)}
    actions = []
    for goods in automorphisms(pattern):
        mapped_pairs = tuple(
            tuple(sorted(goods[good] for good in pair))
            for pair in pattern
        )
        if any(pair not in pair_to_agent for pair in mapped_pairs):
            raise AssertionError("goods automorphism lost an agent edge")
        actions.append(
            (tuple(pair_to_agent[pair] for pair in mapped_pairs), goods)
        )
    return tuple(sorted(actions))


def transform(values, relabeling):
    agents, goods = relabeling
    return tuple(
        tuple(values[agents[agent]][goods[good]] for good in range(M))
        for agent in range(N)
    )


def normalized(values):
    return tuple(
        tuple(Fraction(value, sum(row)) for value in row) for row in values
    )


def canonicalize(values, actions):
    return max(
        (transform(values, action) for action in actions),
        key=lambda candidate: sum(normalized(candidate), ()),
    )


def map_partition(partition, goods):
    return canonical_partition(
        *(tuple(goods[good] for good in bundle) for bundle in partition)
    )


def run(output, pattern_index, random_profiles=128, random_seed=20260801):
    pattern = goods_pattern(pattern_index)
    if multiplicity_signature(pattern) != (1, 1, 1, 1):
        raise ValueError("pattern must have four distinct selected pairs")
    conversion_family, source_pairing_count = conversion_closure(pattern)
    actions = independent_actions(pattern)

    master = ParkabilityLRAMaster(N, M)
    metadata = add_all_distinct_pattern_symmetry(master, pattern_index)
    generators = tuple(
        zip(
            map(tuple, metadata["generator_agent_images"]),
            map(tuple, metadata["generator_good_images"]),
        )
    )
    if (
        generated_group(generators) != set(actions)
        or metadata["group_size"] != len(actions)
        or metadata["goods_automorphism_count"]
        != len({goods for _, goods in actions})
    ):
        raise AssertionError("implemented generators changed their group")

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

    rng = random.Random(random_seed)
    for _ in range(random_profiles):
        values = tuple(
            tuple(rng.randint(1, 100) for _ in range(M))
            for _ in range(N)
        )
        canonical = normalized(canonicalize(values, actions))
        if any(
            sum(canonical, ()) < sum(transform(canonical, generator), ())
            for generator in generators
        ):
            raise AssertionError("orbit maximum violated a generator lex cut")

    orbit_sizes = list(
        map(len, pattern_conversion_orbits(pattern, conversion_family))
    )
    result = {
        "schema": SCHEMA,
        "status": "ALL_DISTINCT_PATTERN_SYMMETRY_AUDITED",
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "generator_count": len(generators),
        "group_size": len(actions),
        "goods_automorphism_count": len({goods for _, goods in actions}),
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(conversion_family),
        "conversion_orbit_sizes": orbit_sizes,
        "action_invariance_checked": True,
        "random_canonical_representatives_checked": random_profiles,
        "random_seed": random_seed,
        "claim_boundary": (
            "This independently enumerates the full relabeling group, "
            "checks the implemented generators, bottom-pattern and "
            "conversion-family invariance, and generator lex leaders."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pattern-index", type=int, required=True)
    parser.add_argument("--random-profiles", type=int, default=128)
    args = parser.parse_args()
    if args.random_profiles < 1:
        parser.error("at least one random profile is required")
    print(
        json.dumps(
            run(args.output, args.pattern_index, args.random_profiles),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
