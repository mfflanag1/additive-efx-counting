#!/usr/bin/env python3
"""Audit symmetry breaks for selected bottom-pair patterns."""

from __future__ import annotations

import argparse
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


SCHEMA = "remaining-repeated-pattern-symmetry-audit-v1"
N = 4
M = 9
IDENTITY_AGENTS = tuple(range(N))
IDENTITY_GOODS = tuple(range(M))


def action(*, agents=IDENTITY_AGENTS, goods=IDENTITY_GOODS):
    return tuple(agents), tuple(goods)


def swap_goods(left, right):
    goods = list(IDENTITY_GOODS)
    goods[left], goods[right] = goods[right], goods[left]
    return action(goods=goods)


def compose(left, right):
    return action(
        agents=tuple(left[0][right[0][agent]] for agent in range(N)),
        goods=tuple(left[1][right[1][good]] for good in range(M)),
    )


def generated_group(generators):
    identity = action()
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            image = compose(current, generator)
            if image not in group:
                group.add(image)
                frontier.append(image)
    return tuple(sorted(group))


def pattern_spec(pattern_index):
    repeated_agent_swap = action(agents=(1, 0, 2, 3))
    if pattern_index == 4:
        generators = (repeated_agent_swap,) + tuple(
            swap_goods(left, left + 1) for left in range(5, 8)
        )
        return generators, 48, 24, (
            3, 12, 6, 12, 12, 12, 6, 12, 3, 12, 12, 6, 12,
            6, 3, 12, 12, 12, 12, 6, 12, 6, 3, 12, 12, 12,
        )
    if pattern_index == 5:
        generators = (
            repeated_agent_swap,
            swap_goods(4, 5),
            swap_goods(6, 7),
            swap_goods(7, 8),
        )
        return generators, 24, 12, (
            6, 3, 6, 6, 6, 3, 6, 12, 3, 12, 3, 6, 3, 6,
            3, 6, 3, 6, 12, 6, 3, 6, 3, 6, 3, 6, 12, 6,
            3, 6, 6, 6, 6, 6, 6, 6, 12, 6, 6, 12, 12,
        )
    if pattern_index == 7:
        generators = (
            repeated_agent_swap,
            swap_goods(1, 2),
            action(
                agents=(0, 1, 3, 2),
                goods=(0, 1, 2, 3, 5, 4, 6, 7, 8),
            ),
            swap_goods(6, 7),
            swap_goods(7, 8),
        )
        return generators, 48, 24, (
            12, 6, 12, 6, 12, 24, 12, 6, 3, 6, 6, 12,
            12, 6, 24, 6, 6, 6, 6, 12, 12, 24, 12, 12,
        )
    if pattern_index == 8:
        generators = (
            repeated_agent_swap,
            swap_goods(1, 2),
            swap_goods(3, 4),
            swap_goods(5, 6),
            swap_goods(7, 8),
            action(
                agents=(0, 1, 3, 2),
                goods=(0, 1, 2, 5, 6, 3, 4, 7, 8),
            ),
        )
        return generators, 64, 32, (
            4, 8, 8, 16, 32, 16, 2, 4, 4, 16,
            4, 4, 8, 16, 32, 32, 16, 8, 32, 8,
        )
    if pattern_index == 14:
        generators = (
            action(
                agents=(1, 3, 0, 2),
                goods=(0, 3, 1, 4, 2, 5, 6, 7, 8),
            ),
            action(
                agents=(2, 3, 0, 1),
                goods=(0, 4, 2, 3, 1, 5, 6, 7, 8),
            ),
            swap_goods(5, 6),
            swap_goods(6, 7),
            swap_goods(7, 8),
        )
        return generators, 192, 192, (12, 48, 48, 96, 96)
    if pattern_index == 19:
        component_swaps = []
        for left_agent in range(N - 1):
            right_agent = left_agent + 1
            agents = list(IDENTITY_AGENTS)
            agents[left_agent], agents[right_agent] = (
                agents[right_agent], agents[left_agent],
            )
            goods = list(IDENTITY_GOODS)
            for left, right in zip(
                (2 * left_agent + 1, 2 * left_agent + 2),
                (2 * right_agent + 1, 2 * right_agent + 2),
            ):
                goods[left], goods[right] = goods[right], goods[left]
            component_swaps.append(action(agents=agents, goods=goods))
        generators = tuple(
            swap_goods(left, left + 1) for left in (1, 3, 5, 7)
        ) + tuple(component_swaps)
        return generators, 384, 384, (24, 48, 96, 192)
    raise ValueError("unsupported pattern index")


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


def canonicalize(values, group):
    return max(
        (transform(values, relabeling) for relabeling in group),
        key=lambda candidate: sum(normalized(candidate), ()),
    )


def map_partition(partition, goods):
    return canonical_partition(
        *(tuple(goods[good] for good in bundle) for bundle in partition)
    )


def audit_action_invariance(group, pattern, conversion_family):
    family = set(conversion_family)
    for agents, goods in group:
        for new_agent, lows in enumerate(pattern):
            mapped_lows = tuple(sorted(goods[good] for good in lows))
            if mapped_lows != pattern[agents[new_agent]]:
                raise AssertionError("symmetry action changed the bottom pattern")
        if {
            map_partition(partition, goods)
            for partition in conversion_family
        } != family:
            raise AssertionError("symmetry action changed the conversion closure")


def run(output, pattern_index, random_profiles=128, random_seed=20260801):
    generators, expected_group, expected_goods, expected_orbits = pattern_spec(
        pattern_index
    )
    group = generated_group(generators)
    if len(group) != expected_group:
        raise AssertionError("generated symmetry group size changed")
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    conversion_family, source_pairing_count = conversion_closure(selected_pairs)
    audit_action_invariance(group, pattern, conversion_family)
    orbit_sizes = tuple(
        map(len, pattern_conversion_orbits(pattern, conversion_family))
    )
    if orbit_sizes != expected_orbits:
        raise AssertionError("conversion orbit sizes changed")

    rng = random.Random(random_seed)
    for _ in range(random_profiles):
        values = tuple(
            tuple(rng.randint(1, 100) for _ in range(M))
            for _ in range(N)
        )
        canonical = normalized(canonicalize(values, group))
        if any(
            sum(canonical, ()) < sum(transform(canonical, generator), ())
            for generator in generators
        ):
            raise AssertionError("orbit maximum violated a generator lex cut")

    goods_automorphism_count = len({goods for _, goods in group})
    if goods_automorphism_count != expected_goods:
        raise AssertionError("goods automorphism count changed")
    result = {
        "schema": SCHEMA,
        "status": "REMAINING_REPEATED_PATTERN_SYMMETRY_AUDITED",
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "generator_count": len(generators),
        "group_size": len(group),
        "goods_automorphism_count": goods_automorphism_count,
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(conversion_family),
        "conversion_orbit_sizes": list(orbit_sizes),
        "action_invariance_checked": True,
        "random_canonical_representatives_checked": random_profiles,
        "random_seed": random_seed,
        "claim_boundary": (
            "This deterministically closes the generator group, checks every "
            "action on the bottom pattern and conversion family, and tests "
            "the generator lex leaders on deterministic orbit maxima."
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
