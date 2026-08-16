#!/usr/bin/env python3
"""Audit the strict boundary refuting favorite-pair rank augmentation."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import (
        N,
        audit_branch,
        build_state_graph,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import balanced_state_universe
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import (
        N,
        audit_branch,
        build_state_graph,
    )
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import balanced_state_universe


SCHEMA = "distinct-half-favorite-pair-rank-boundary-audit-v1"
FAVORITE = 0
VALUES = (
    (100, 1, 2, 55, 69, 59, 96, 77, 95),
    (100, 5, 17, 73, 69, 62, 55, 68, 53),
    (100, 8, 1, 48, 73, 69, 61, 67, 65),
    (100, 8, 1, 55, 79, 90, 71, 66, 82),
)


def has_perfect_matching(graph):
    return any(
        all(graph[agent][matching[agent]] for agent in range(N))
        for matching in itertools.permutations(range(N))
    )


def common_low_repairs(universe):
    repairs = []
    for partition in universe:
        favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
        if len(favorite_bundle) != 3:
            continue
        low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
        pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
        if all(
            all(
                sum(row[good] for good in pair)
                >= row[FAVORITE] + max(row[good] for good in low_goods)
                for pair in pairs
            )
            for row in VALUES
        ):
            repairs.append(partition)
    return tuple(repairs)


def literal_efx_census():
    labeled_shapes = Counter()
    examples = {}
    for assignment in itertools.product(range(N), repeat=len(VALUES[0])):
        if not independent.is_complete_efx0(VALUES, assignment):
            continue
        bundles = tuple(
            tuple(good for good, owner in enumerate(assignment) if owner == agent)
            for agent in range(N)
        )
        shape = tuple(sorted(map(len, bundles), reverse=True))
        favorite_size = len(bundles[assignment[FAVORITE]])
        key = (shape, favorite_size)
        labeled_shapes[key] += 1
        examples.setdefault(key, assignment)
    return labeled_shapes, examples


def audit():
    representatives = audit_branch(VALUES)
    favorite_pair_universe, favorite_pair_neighbors = build_state_graph()
    favorite_pair_graphs = tuple(
        feasible_graph(VALUES, partition) for partition in favorite_pair_universe
    )
    favorite_pair_ranks = tuple(map(matching_rank, favorite_pair_graphs))

    balanced_universe = tuple(balanced_state_universe())
    balanced_graphs = tuple(
        feasible_graph(VALUES, partition) for partition in balanced_universe
    )
    balanced_ranks = tuple(map(matching_rank, balanced_graphs))
    balanced_perfect = tuple(
        partition
        for partition, graph in zip(balanced_universe, balanced_graphs)
        if has_perfect_matching(graph)
    )
    repairs = common_low_repairs(balanced_universe)
    labeled_shapes, examples = literal_efx_census()

    expected_key = ((3, 2, 2, 2), 3)
    if (
        representatives != (3, 4, 5, 6)
        or any(len(set(row)) != len(row) for row in VALUES)
        or Counter(favorite_pair_ranks)
        != Counter({1: 20, 2: 237, 3: 583})
        or Counter(balanced_ranks)
        != Counter({1: 278, 2: 359, 3: 608, 4: 15})
        or len(balanced_perfect) != 15
        or len(repairs) != 9
        or labeled_shapes != Counter({expected_key: 324})
        or independent.count_complete_efx0(VALUES) != 324
    ):
        raise AssertionError("favorite-pair rank boundary census changed")
    if any(
        tuple(next(bundle for bundle in partition if FAVORITE in bundle))
        != (0, 1, 2)
        for partition in balanced_perfect
    ):
        raise AssertionError("balanced repairs lost the common low triple")

    example_assignment = examples[expected_key]
    example_bundles = [
        [
            good
            for good, owner in enumerate(example_assignment)
            if owner == agent
        ]
        for agent in range(N)
    ]
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FAVORITE_PAIR_RANK_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "strict_common_favorite": True,
        "distinct_item_values_per_row": True,
        "half_favorite_representatives": list(representatives),
        "favorite_pair_state_graph": {
            "partitions": len(favorite_pair_universe),
            "undirected_edges": sum(map(len, favorite_pair_neighbors)) // 2,
            "degree": len(favorite_pair_neighbors[0]),
            "matching_rank_histogram": {
                str(rank): count
                for rank, count in sorted(Counter(favorite_pair_ranks).items())
            },
            "efx_partition_count": sum(rank == N for rank in favorite_pair_ranks),
        },
        "all_balanced_partitions": {
            "partitions": len(balanced_universe),
            "matching_rank_histogram": {
                str(rank): count
                for rank, count in sorted(Counter(balanced_ranks).items())
            },
            "efx_partition_count": len(balanced_perfect),
            "favorite_bundle_size_in_every_efx_partition": 3,
            "common_favorite_triple_in_every_efx_partition": [0, 1, 2],
        },
        "common_low_triple_repair_partition_count": len(repairs),
        "common_low_triple_repair_example": [
            list(bundle) for bundle in repairs[0]
        ],
        "literal_complete_efx_allocation_count": sum(labeled_shapes.values()),
        "literal_complete_efx_shape_census": {
            "3+2+2+2_favorite_in_triple": labeled_shapes[expected_key],
        },
        "literal_complete_efx_example_bundles_by_owner": example_bundles,
        "interpretation": (
            "The branch-specific favorite-pair rank-augmentation conjecture "
            "is false. Complete EFX survives only after moving the favorite "
            "into a triple with the two common low goods."
        ),
        "limitation": (
            "This profile has 324 complete EFX allocations and is not an "
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
