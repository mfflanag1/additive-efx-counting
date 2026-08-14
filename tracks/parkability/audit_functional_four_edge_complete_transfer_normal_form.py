#!/usr/bin/env python3
"""Exhaust the functional four-edge complete-transfer graph normal form."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
CHARITY = "charity"


def weak_components(edges):
    vertices = set(OWNERS) | {CHARITY}
    adjacency = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = []
    unseen = set(vertices)
    while unseen:
        seed = min(unseen)
        seen = set()
        queue = deque([seed])
        while queue:
            vertex = queue.popleft()
            if vertex in seen:
                continue
            seen.add(vertex)
            queue.extend(adjacency[vertex] - seen)
        components.append(frozenset(seen))
        unseen -= seen
    return tuple(sorted(components, key=lambda component: sorted(component)))


def directed_owner_cycles(edges):
    edge_set = set(edges)
    found = set()
    for size in range(2, len(OWNERS) + 1):
        for vertices in itertools.permutations(OWNERS, size):
            if vertices[0] != min(vertices):
                continue
            if all(
                (vertices[index], vertices[(index + 1) % size]) in edge_set
                for index in range(size)
            ):
                found.add(frozenset(vertices))
    return tuple(sorted(found, key=lambda cycle: sorted(cycle)))


def classify(edges):
    components = weak_components(edges)
    charity_component = next(component for component in components if CHARITY in component)
    cycles = directed_owner_cycles(edges)
    indegree = Counter(target for _, target in edges)
    if (
        len(charity_component) == 5
        and not cycles
        and all(indegree[owner] == 1 for owner in OWNERS)
    ):
        kind = "charity_hamiltonian_path"
    elif len(charity_component) == 5 and not cycles:
        kind = "charity_connected_acyclic_branching"
    elif any(cycle <= charity_component for cycle in cycles):
        kind = "charity_fed_owner_cycle"
    elif cycles:
        kind = "disconnected_owner_cycle"
    else:
        # With five vertices and four edges, a disconnected acyclic graph
        # cannot occur. Keep this fail-closed label if the enumeration is
        # generalized later.
        kind = "acyclic_disconnected_forest"
    return kind, components, cycles


def run():
    records = []
    counts = Counter()
    # Exactly four edges, distinct sources, one source is charity.  Therefore
    # exactly three of the four owners send one packet and the fourth is the
    # unique owner sink/source-hole.  Complete allocation forbids charity as
    # a target; self-retention is not an active edge.
    for active_owners in itertools.combinations(OWNERS, 3):
        sources = (CHARITY, *active_owners)
        choices = {
            source: tuple(owner for owner in OWNERS if owner != source)
            for source in sources
        }
        for targets in itertools.product(*(choices[source] for source in sources)):
            edges = tuple(sorted(zip(sources, targets)))
            kind, components, cycles = classify(edges)
            counts[kind] += 1
            records.append({
                "edges": [list(edge) for edge in edges],
                "class": kind,
                "weak_components": [sorted(component) for component in components],
                "owner_cycles": [sorted(cycle) for cycle in cycles],
            })
    assert len(records) == 432
    assert sum(counts.values()) == 432
    assert counts["charity_hamiltonian_path"] == 24
    assert set(counts) == {
        "charity_hamiltonian_path",
        "charity_connected_acyclic_branching",
        "charity_fed_owner_cycle",
        "disconnected_owner_cycle",
    }
    script = Path(__file__).resolve()
    return {
        "schema": "functional-four-edge-complete-transfer-normal-form-v1",
        "status": "ALL_FUNCTIONAL_FOUR_EDGE_GRAPHS_CLASSIFIED",
        "owner_count": 4,
        "edge_count": 4,
        "functional": True,
        "topology_count": len(records),
        "class_counts": dict(sorted(counts.items())),
        "hamiltonian_path_count": counts["charity_hamiltonian_path"],
        "records": records,
        "claim_boundary": (
            "cap-free graph classification of exactly-four-edge functional "
            "complete transfer systems. It does not prove that arbitrary packet "
            "values admit one of these systems or that cycle/forest classes are "
            "release-compatible under the full signed GG premises."
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "topology_count": result["topology_count"],
        "class_counts": result["class_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
