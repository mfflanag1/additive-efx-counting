#!/usr/bin/env python3
"""Audit the essential-edge Hall classification for four bundles."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "row-merge-essential-edge-hall-audit-v1"
N = 4
MOVING = 0
CRITICAL_BUNDLE = 0
MATCHINGS = tuple(itertools.permutations(range(N)))


def has_perfect_matching(graph):
    return any(
        all(graph[agent][matching[agent]] for agent in range(N))
        for matching in MATCHINGS
    )


def minimal_hall_witnesses(graph):
    deficient = []
    for size in range(1, N + 1):
        for agents in itertools.combinations(range(N), size):
            neighbors = tuple(
                bundle
                for bundle in range(N)
                if any(graph[agent][bundle] for agent in agents)
            )
            if len(neighbors) < len(agents):
                deficient.append((agents, neighbors))
    return tuple(
        witness
        for witness in deficient
        if not any(
            set(other_agents) < set(witness[0])
            for other_agents, _other_neighbors in deficient
        )
    )


def canonical_graph(graph):
    images = []
    for resident_order in itertools.permutations(range(1, N)):
        row_order = (MOVING,) + resident_order
        for other_bundles in itertools.permutations(range(1, N)):
            bundle_order = (CRITICAL_BUNDLE,) + other_bundles
            images.append(
                tuple(
                    graph[agent][bundle]
                    for agent in row_order
                    for bundle in bundle_order
                )
            )
    return min(images)


def run(output):
    if output.exists():
        raise ValueError("output path already exists")
    graph_count = 0
    orbit_representatives = {}
    graph_type_count = Counter()
    for bits in range(1 << (N * N)):
        graph = tuple(
            tuple(
                bool(bits & (1 << (N * agent + bundle)))
                for bundle in range(N)
            )
            for agent in range(N)
        )
        if (
            not graph[MOVING][CRITICAL_BUNDLE]
            or any(not any(row) for row in graph)
            or not has_perfect_matching(graph)
        ):
            continue
        deleted = tuple(
            tuple(
                False
                if (agent, bundle) == (MOVING, CRITICAL_BUNDLE)
                else graph[agent][bundle]
                for bundle in range(N)
            )
            for agent in range(N)
        )
        if has_perfect_matching(deleted):
            continue
        witnesses = minimal_hall_witnesses(deleted)
        types = tuple(
            sorted(
                {
                    (
                        len(agents),
                        len(neighbors),
                        MOVING in agents,
                        CRITICAL_BUNDLE in neighbors,
                    )
                    for agents, neighbors in witnesses
                }
            )
        )
        if (
            not witnesses
            or len(types) != 1
            or types[0][1] != types[0][0] - 1
            or types[0][2:] != (True, False)
        ):
            raise AssertionError("essential-edge Hall classification failed")
        graph_count += 1
        graph_type_count[types[0][0]] += 1
        orbit_representatives.setdefault(canonical_graph(graph), types[0][0])

    orbit_type_count = Counter(orbit_representatives.values())
    if (
        graph_count != 4929
        or len(orbit_representatives) != 213
        or set(graph_type_count) != {1, 2, 3, 4}
        or set(orbit_type_count) != {1, 2, 3, 4}
    ):
        raise AssertionError("essential-edge graph census changed")
    result = {
        "schema": SCHEMA,
        "status": "ESSENTIAL_EDGE_HALL_CLASSIFICATION_VERIFIED",
        "agent_count": N,
        "bundle_count": N,
        "distinguished_moving_agent": MOVING,
        "distinguished_deleted_edge_bundle": CRITICAL_BUNDLE,
        "graph_count": graph_count,
        "symmetry_orbit_count": len(orbit_representatives),
        "graph_count_by_minimal_hall_witness_size": {
            str(size): graph_type_count[size] for size in range(1, N + 1)
        },
        "orbit_count_by_minimal_hall_witness_size": {
            str(size): orbit_type_count[size] for size in range(1, N + 1)
        },
        "classification": (
            "Every minimal Hall witness contains the moving agent, excludes "
            "the critical bundle from its neighborhood, and has exactly one "
            "fewer neighbor than agents. Its size is 1, 2, 3, or 4."
        ),
        "claim_boundary": (
            "This is a complete graph-theoretic audit of the four-by-four "
            "essential-edge cases. It does not prove the bundle-changing "
            "single-wall pivot conjecture."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
