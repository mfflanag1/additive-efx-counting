#!/usr/bin/env python3
"""Regression audit for the one-defect favorite-triple conversion lemma."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
except ImportError:
    import independent
    from anneal import atomic_json


SCHEMA = "one-defect-favorite-triple-conversion-audit-v1"
N = 4
M = 9
FAVORITE = 0
BOUNDARY = (
    (100, 1, 4, 57, 48, 69, 70, 66, 67),
    (100, 1, 5, 79, 56, 59, 59, 85, 54),
    (100, 1, 2, 72, 52, 53, 90, 74, 62),
    (100, 8, 1, 56, 80, 61, 60, 40, 60),
)


def pairings(goods):
    goods = tuple(goods)
    first = goods[0]
    for partner in goods[1:]:
        remaining = tuple(
            good for good in goods if good not in (first, partner)
        )
        second = remaining[0]
        for second_partner in remaining[1:]:
            yield (
                (first, partner),
                (second, second_partner),
                tuple(
                    good
                    for good in remaining
                    if good not in (second, second_partner)
                ),
            )


def safe(values, agent, low_goods, pair):
    return (
        sum(values[agent][good] for good in pair)
        >= values[agent][FAVORITE]
        + max(values[agent][good] for good in low_goods)
    )


def literal_allocation(values, bundles, bundle_by_agent):
    assignment = [None] * M
    for agent, bundle_index in enumerate(bundle_by_agent):
        for good in bundles[bundle_index]:
            assignment[good] = agent
    if any(owner is None for owner in assignment):
        raise AssertionError("constructed allocation lost a good")
    return independent.is_complete_efx0(values, assignment)


def audit_candidate(values, low_goods, matching):
    defects = tuple(
        tuple(
            agent
            for agent in range(N)
            if not safe(values, agent, low_goods, pair)
        )
        for pair in matching
    )
    if all(not rejected for rejected in defects):
        bundles = ((FAVORITE,) + low_goods,) + matching
        if not literal_allocation(values, bundles, tuple(range(N))):
            raise AssertionError("all-safe construction is not EFX")
        return "all_safe"

    for exceptional in range(3):
        if len(defects[exceptional]) != 1 or any(
            defects[index] for index in range(3) if index != exceptional
        ):
            continue
        rejecter = defects[exceptional][0]
        ordinary = tuple(index for index in range(3) if index != exceptional)
        other_agents = tuple(agent for agent in range(N) if agent != rejecter)
        exceptional_value = {
            agent: sum(
                values[agent][good] for good in matching[exceptional]
            )
            for agent in other_agents
        }
        pair_matching = next(
            (
                (left_agent, right_agent)
                for left_agent in other_agents
                for right_agent in other_agents
                if left_agent != right_agent
                and sum(
                    values[left_agent][good]
                    for good in matching[ordinary[0]]
                )
                >= exceptional_value[left_agent]
                and sum(
                    values[right_agent][good]
                    for good in matching[ordinary[1]]
                )
                >= exceptional_value[right_agent]
            ),
            None,
        )
        if pair_matching is None:
            continue

        high = max(low_goods, key=lambda good: values[rejecter][good])
        low = next(good for good in low_goods if good != high)
        bundles = (
            (FAVORITE, high),
            tuple(sorted((low,) + matching[exceptional])),
            matching[ordinary[0]],
            matching[ordinary[1]],
        )
        bundle_by_agent = [None] * N
        bundle_by_agent[rejecter] = 0
        bundle_by_agent[pair_matching[0]] = 2
        bundle_by_agent[pair_matching[1]] = 3
        remaining_agent = next(
            agent for agent in other_agents if bundle_by_agent[agent] is None
        )
        bundle_by_agent[remaining_agent] = 1
        if not literal_allocation(values, bundles, tuple(bundle_by_agent)):
            raise AssertionError("one-defect construction is not EFX")
        return "one_defect"
    return None


def scan(values):
    counts = Counter()
    for low_goods in itertools.combinations(range(1, M), 2):
        remaining = tuple(
            good for good in range(1, M) if good not in low_goods
        )
        for matching in pairings(remaining):
            kind = audit_candidate(values, low_goods, matching)
            if kind is not None:
                counts[kind] += 1
    return counts


def audit(random_profiles, seed):
    all_safe_values = BOUNDARY
    one_defect_values = [list(row) for row in BOUNDARY]
    one_defect_values[3][4] = 67
    one_defect_values = tuple(tuple(row) for row in one_defect_values)
    boundary_counts = {
        "all_safe_boundary": scan(all_safe_values),
        "one_defect_boundary": scan(one_defect_values),
    }
    rng = random.Random(seed)
    random_counts = Counter()
    for profile_index in range(random_profiles):
        values = [
            [100, rng.randint(1, 10), rng.randint(1, 10)]
            + [rng.randint(60, 99) for _ in range(6)]
            for _ in range(N)
        ]
        if profile_index % 2:
            rejecter = rng.randrange(N)
            values[rejecter][3] = rng.randint(20, 40)
            values[rejecter][4] = rng.randint(20, 40)
        values = tuple(tuple(row) for row in values)
        random_counts.update(scan(values))
    if (
        boundary_counts["all_safe_boundary"]["all_safe"] != 3
        or boundary_counts["one_defect_boundary"]["one_defect"] < 3
        or not random_counts
    ):
        raise AssertionError("conversion boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_AUDIT_PASSED",
        "random_profiles": random_profiles,
        "random_seed": seed,
        "boundary_candidate_counts": {
            name: dict(sorted(counts.items()))
            for name, counts in boundary_counts.items()
        },
        "random_candidate_counts": dict(sorted(random_counts.items())),
        "interpretation": (
            "Every enumerated all-safe or one-defect candidate constructs "
            "a literal complete EFX allocation exactly as in the analytic "
            "lemma. This is a regression audit, not its proof."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260731)
    args = parser.parse_args()
    if args.random_profiles < 0:
        parser.error("random profile count must be nonnegative")
    result = audit(args.random_profiles, args.seed)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
