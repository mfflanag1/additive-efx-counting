#!/usr/bin/env python3
"""Audit a strict branch-valid boundary to radius-two rank augmentation."""

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
        canonical,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import (
        N,
        audit_branch,
        build_state_graph,
        canonical,
    )
    from audit_matching_augmentation import feasible_graph, matching_rank


SCHEMA = "distinct-half-rank-radius-boundary-audit-v1"
VALUES = (
    (100, 35, 55, 37, 4, 99, 51, 83, 56),
    (100, 93, 41, 77, 80, 1, 57, 86, 99),
    (100, 92, 86, 27, 99, 72, 77, 14, 53),
    (100, 99, 84, 1, 93, 83, 75, 61, 36),
)
START = canonical(((0, 3), (1, 4, 5), (2, 8), (6, 7)))


def perfect_matching(graph):
    return next(
        (
            matching
            for matching in itertools.permutations(range(N))
            if all(graph[agent][matching[agent]] for agent in range(N))
        ),
        None,
    )


def audit():
    representatives = audit_branch(VALUES)
    universe, neighbors = build_state_graph()
    positions = {partition: position for position, partition in enumerate(universe)}
    start = positions[START]
    graphs = tuple(feasible_graph(VALUES, partition) for partition in universe)
    ranks = tuple(matching_rank(graph) for graph in graphs)
    if ranks[start] != N - 1:
        raise AssertionError("start no longer has rank three")

    parent = {start: None}
    queue = [start]
    exits = set()
    first_exit = None
    while queue:
        current = queue.pop(0)
        for neighbor in neighbors[current]:
            if ranks[neighbor] == N:
                exits.add(neighbor)
                candidate = (parent_distance(parent, current) + 1, current, neighbor)
                if first_exit is None or candidate < first_exit:
                    first_exit = candidate
            elif ranks[neighbor] == N - 1 and neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if first_exit is None:
        raise AssertionError("rank-three plateau became trapped")

    distance, boundary, destination = first_exit
    path = [boundary]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    path.append(destination)

    radius_one = set(neighbors[start])
    radius_two_plateau = {
        second
        for middle in radius_one
        if ranks[middle] == N - 1
        for second in neighbors[middle]
    }
    radius_two_perfect = {
        position
        for position in radius_one | radius_two_plateau
        if ranks[position] == N
    }
    complete_count = independent.count_complete_efx0(VALUES)
    if (
        representatives != (2, 1, 4, 5)
        or radius_two_perfect
        or distance != 3
        or len(parent) != 395
        or len(exits) != 312
        or sum(rank == N for rank in ranks) != 312
        or complete_count != 1052
        or any(len(set(row)) != len(row) for row in VALUES)
    ):
        raise AssertionError("rank-radius boundary census changed")

    final_matching = perfect_matching(graphs[destination])
    if final_matching is None:
        raise AssertionError("rank-four destination lost its matching")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_RANK_RADIUS_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "strict_common_favorite": True,
        "distinct_item_values_per_row": True,
        "half_favorite_representatives": list(representatives),
        "favorite_pair_state_graph": {
            "partitions": len(universe),
            "undirected_edges": sum(map(len, neighbors)) // 2,
            "degree": len(neighbors[0]),
        },
        "matching_rank_histogram": {
            str(rank): count for rank, count in sorted(Counter(ranks).items())
        },
        "start_partition": [list(bundle) for bundle in START],
        "start_feasibility_graph": [
            [int(edge) for edge in row] for row in graphs[start]
        ],
        "start_matching_rank": ranks[start],
        "perfect_partitions_within_radius_two_via_rank_three": 0,
        "minimum_rank_preserving_walk_then_augmentation_length": distance,
        "rank_three_plateau_component_size": len(parent),
        "distinct_perfect_exit_partitions": len(exits),
        "shortest_augmenting_path": [
            {
                "partition": [list(bundle) for bundle in universe[position]],
                "matching_rank": ranks[position],
            }
            for position in path
        ],
        "destination_perfect_matching_agent_to_bundle": list(final_matching),
        "favorite_pair_balanced_efx_partition_count": sum(
            rank == N for rank in ranks
        ),
        "literal_complete_efx_allocation_count": complete_count,
        "interpretation": (
            "The branch-specific plateau conjecture survives, but its former "
            "empirical radius-two strengthening is false. This strict profile "
            "requires two rank-preserving swaps before an augmenting swap."
        ),
        "limitation": (
            "The rank-three plateau has many exits and the profile has complete "
            "EFX allocations; this is not a counterexample to EFX existence."
        ),
    }


def parent_distance(parent, position):
    distance = 0
    while parent[position] is not None:
        position = parent[position]
        distance += 1
    return distance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
