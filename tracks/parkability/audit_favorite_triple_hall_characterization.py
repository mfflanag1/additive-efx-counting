#!/usr/bin/env python3
"""Regression audit for the favorite-triple Hall characterization."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import balanced_state_universe
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import balanced_state_universe


SCHEMA = "favorite-triple-hall-characterization-audit-v1"
N = 4
M = 9
FAVORITE = 0
BOUNDARY = (
    (100, 1, 4, 57, 48, 69, 70, 66, 67),
    (100, 1, 5, 79, 56, 59, 59, 85, 54),
    (100, 1, 2, 72, 52, 53, 90, 74, 62),
    (100, 8, 1, 56, 80, 61, 60, 40, 60),
)


def favorite_triple_universe():
    result = tuple(
        partition
        for partition in balanced_state_universe()
        if len(next(bundle for bundle in partition if FAVORITE in bundle)) == 3
    )
    if len(result) != 420:
        raise AssertionError("favorite-triple universe changed")
    return result


def pair_agent_masks(values, partition):
    triple = next(bundle for bundle in partition if FAVORITE in bundle)
    lows = tuple(good for good in triple if good != FAVORITE)
    pairs = tuple(bundle for bundle in partition if bundle != triple)
    masks = []
    for pair in pairs:
        mask = 0
        for agent, row in enumerate(values):
            threshold = row[FAVORITE] + max(row[good] for good in lows)
            if sum(row[good] for good in pair) >= threshold:
                mask |= 1 << agent
        masks.append(mask)
    return tuple(masks)


def saturates_pairs(masks):
    return any(
        all(masks[pair] & (1 << agent) for pair, agent in enumerate(agents))
        for agents in itertools.permutations(range(N), 3)
    )


def hall_failure_type(masks):
    if any(mask == 0 for mask in masks):
        return "one_pair_zero_neighbors"
    if any(
        (masks[left] | masks[right]).bit_count() <= 1
        for left, right in itertools.combinations(range(3), 2)
    ):
        return "two_pairs_at_most_one_neighbor"
    if (masks[0] | masks[1] | masks[2]).bit_count() <= 2:
        return "three_pairs_at_most_two_neighbors"
    return None


def perfect_pairings(goods):
    goods = tuple(goods)
    if not goods:
        yield ()
        return
    first = goods[0]
    for partner in goods[1:]:
        remaining = tuple(
            good for good in goods if good not in (first, partner)
        )
        for rest in perfect_pairings(remaining):
            yield ((first, partner),) + rest


def audit_two_core_tutte(values):
    checks = 0
    qualifying_cells = 0
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        edges = tuple(itertools.combinations(residual, 2))
        masks = {
            edge: pair_agent_masks(
                values,
                ((FAVORITE,) + lows, edge, (), ()),
            )[0]
            for edge in edges
        }
        pairings = tuple(perfect_pairings(residual))
        all_pairings_hall = all(
            saturates_pairs(tuple(masks[edge] for edge in pairing))
            for pairing in pairings
        )
        for core in itertools.combinations(range(N), 2):
            core_mask = sum(1 << agent for agent in core)
            if any(mask & core_mask != core_mask for mask in masks.values()):
                continue
            outsider_mask = ((1 << N) - 1) ^ core_mask
            bad_edges = {
                edge for edge, mask in masks.items() if not mask & outsider_mask
            }
            bad_has_perfect_matching = any(
                all(tuple(sorted(edge)) in bad_edges for edge in pairing)
                for pairing in pairings
            )
            if all_pairings_hall != (not bad_has_perfect_matching):
                raise AssertionError("two-core/Tutte corollary changed")
            checks += 1
            qualifying_cells += all_pairings_hall
    return checks, qualifying_cells


def audit_profile(values, universe):
    counts = Counter()
    for partition in universe:
        masks = pair_agent_masks(values, partition)
        hall = saturates_pairs(masks)
        literal = matching_rank(feasible_graph(values, partition)) == N
        if hall != literal:
            raise AssertionError("Hall criterion disagrees with literal EFX graph")
        if hall:
            counts["hall_supporting"] += 1
        else:
            failure = hall_failure_type(masks)
            if failure is None:
                raise AssertionError("missing Hall obstruction")
            counts[failure] += 1
    return counts


def audit(random_profiles, seed):
    universe = favorite_triple_universe()
    modified = [list(row) for row in BOUNDARY]
    modified[3][4] = 67
    boundary_counts = {
        "three_all_safe_repairs": audit_profile(BOUNDARY, universe),
        "one_defect_repairs": audit_profile(
            tuple(tuple(row) for row in modified),
            universe,
        ),
    }
    boundary_tutte = {
        "three_all_safe_repairs": audit_two_core_tutte(BOUNDARY),
        "one_defect_repairs": audit_two_core_tutte(
            tuple(tuple(row) for row in modified)
        ),
    }
    rng = random.Random(seed)
    aggregate = Counter()
    random_tutte_checks = 0
    random_tutte_qualifying = 0
    for _ in range(random_profiles):
        values = tuple(
            (100,) + tuple(rng.randint(1, 99) for _ in range(M - 1))
            for _ in range(N)
        )
        aggregate.update(audit_profile(values, universe))
        checks, qualifying = audit_two_core_tutte(values)
        random_tutte_checks += checks
        random_tutte_qualifying += qualifying
    if (
        boundary_counts["three_all_safe_repairs"]["hall_supporting"] != 15
        or boundary_counts["one_defect_repairs"]["hall_supporting"] != 15
        or sum(aggregate.values()) != random_profiles * len(universe)
    ):
        raise AssertionError("favorite-triple Hall census changed")
    return {
        "schema": SCHEMA,
        "status": "FAVORITE_TRIPLE_HALL_CHARACTERIZATION_AUDIT_PASSED",
        "favorite_triple_partition_count": len(universe),
        "random_profiles": random_profiles,
        "random_seed": seed,
        "literal_partition_checks": (
            (random_profiles + len(boundary_counts)) * len(universe)
        ),
        "boundary_counts": {
            name: dict(sorted(counts.items()))
            for name, counts in boundary_counts.items()
        },
        "boundary_two_core_tutte": {
            name: {
                "applicable_core_checks": counts[0],
                "qualifying_core_cells": counts[1],
            }
            for name, counts in boundary_tutte.items()
        },
        "random_hall_census": dict(sorted(aggregate.items())),
        "random_two_core_tutte_checks": random_tutte_checks,
        "random_two_core_tutte_qualifying_cells": random_tutte_qualifying,
        "claim": (
            "A favorite-triple balanced partition supports EFX exactly when "
            "its three residual pairs have a matching to three agents at "
            "the favorite-triple deletion threshold."
        ),
        "scope_warning": (
            "This finite audit is a regression check for the cap-free "
            "analytic equivalence."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260731)
    args = parser.parse_args()
    if args.random_profiles < 0:
        parser.error("random profile count must be nonnegative")
    result = audit(args.random_profiles, args.seed)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
