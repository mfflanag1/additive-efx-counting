#!/usr/bin/env python3
"""Audit the strict boundary refuting favorite-triple-only EFX."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import N, audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import balanced_state_universe
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import N, audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import balanced_state_universe


SCHEMA = "distinct-half-favorite-triple-boundary-audit-v1"
FAVORITE = 0
VALUES = (
    (100, 82, 87, 69, 40, 34, 39, 58, 44),
    (100, 54, 97, 69, 68, 36, 71, 52, 26),
    (100, 2, 70, 89, 35, 65, 27, 56, 61),
    (100, 31, 73, 99, 60, 66, 26, 64, 22),
)


def literal_census():
    counts = Counter()
    example = None
    for assignment in itertools.product(range(N), repeat=len(VALUES[0])):
        if not independent.is_complete_efx0(VALUES, assignment):
            continue
        bundles = tuple(
            tuple(good for good, owner in enumerate(assignment) if owner == agent)
            for agent in range(N)
        )
        key = (
            tuple(sorted(map(len, bundles), reverse=True)),
            len(bundles[assignment[FAVORITE]]),
        )
        counts[key] += 1
        if example is None:
            example = bundles
    return counts, example


def audit():
    representatives = audit_branch(VALUES)
    universe = tuple(balanced_state_universe())
    records = tuple(
        (
            partition,
            matching_rank(feasible_graph(VALUES, partition)),
            len(next(bundle for bundle in partition if FAVORITE in bundle)),
        )
        for partition in universe
    )
    ranks = Counter(rank for _, rank, _ in records)
    favorite_pair_perfect = sum(
        rank == N and favorite_size == 2
        for _, rank, favorite_size in records
    )
    favorite_triple_perfect = sum(
        rank == N and favorite_size == 3
        for _, rank, favorite_size in records
    )
    labeled, example = literal_census()
    expected_key = ((3, 2, 2, 2), 2)
    if (
        representatives != (1, 2, 3, 4)
        or any(len(set(row)) != len(row) for row in VALUES)
        or ranks != Counter({1: 218, 2: 296, 3: 390, 4: 356})
        or favorite_pair_perfect != 356
        or favorite_triple_perfect != 0
        or labeled != Counter({expected_key: 1906})
        or example is None
    ):
        raise AssertionError("favorite-triple boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FAVORITE_TRIPLE_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "strict_common_favorite": True,
        "distinct_item_values_per_row": True,
        "half_favorite_representatives": list(representatives),
        "balanced_partition_count": len(universe),
        "matching_rank_histogram": {
            str(rank): count for rank, count in sorted(ranks.items())
        },
        "favorite_pair_efx_partition_count": favorite_pair_perfect,
        "favorite_triple_efx_partition_count": favorite_triple_perfect,
        "literal_complete_efx_allocation_count": sum(labeled.values()),
        "literal_complete_efx_shape_census": {
            "3+2+2+2_favorite_in_pair": labeled[expected_key],
        },
        "literal_complete_efx_example_bundles_by_owner": [
            list(bundle) for bundle in example
        ],
        "interpretation": (
            "The favorite-triple-only normal form is false even in strict "
            "generic position. Every complete EFX allocation instead has "
            "the common favorite in a pair."
        ),
        "limitation": (
            "This profile has 1,906 complete EFX allocations and is not an "
            "additive EFX counterexample."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
