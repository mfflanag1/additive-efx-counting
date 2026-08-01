#!/usr/bin/env python3
"""Exhaustively audit the six-vertex Tutte obstruction classification."""

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


SCHEMA = "six-vertex-tutte-classification-audit-v1"
VERTICES = tuple(range(6))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_pairings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for partner in vertices[1:]:
        remaining = tuple(
            vertex
            for vertex in vertices
            if vertex not in (first, partner)
        )
        for rest in perfect_pairings(remaining):
            yield ((first, partner),) + rest


PAIRINGS = tuple(perfect_pairings(VERTICES))


def odd_component_count(edge_set, removed):
    remaining = set(VERTICES).difference(removed)
    odd = 0
    while remaining:
        start = remaining.pop()
        stack = [start]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            neighbors = {
                other
                for edge in edge_set
                if vertex in edge
                for other in edge
                if other != vertex and other in remaining
            }
            remaining.difference_update(neighbors)
            stack.extend(neighbors)
        odd += size % 2
    return odd


def witness_types(edge_set):
    types = []
    if odd_component_count(edge_set, ()) >= 2:
        types.append("two_odd_components")
    if any(
        odd_component_count(edge_set, (vertex,)) >= 3
        for vertex in VERTICES
    ):
        types.append("one_vertex_three_odd_components")
    if any(
        not any(
            left not in removed and right not in removed
            for left, right in edge_set
        )
        for removed in itertools.combinations(VERTICES, 2)
    ):
        types.append("two_vertex_cover")
    return tuple(types)


def audit():
    signature_counts = Counter()
    perfect_matching_count = 0
    no_perfect_matching_count = 0
    for mask in range(1 << len(EDGES)):
        edge_set = {
            edge for index, edge in enumerate(EDGES) if mask & (1 << index)
        }
        has_perfect_matching = any(
            all(edge in edge_set for edge in pairing) for pairing in PAIRINGS
        )
        types = witness_types(edge_set)
        if has_perfect_matching == bool(types):
            raise AssertionError("Tutte classification disagrees with matching")
        if has_perfect_matching:
            perfect_matching_count += 1
        else:
            no_perfect_matching_count += 1
            signature_counts[" + ".join(types)] += 1
    if perfect_matching_count + no_perfect_matching_count != 1 << 15:
        raise AssertionError("six-vertex graph census changed")
    return {
        "schema": SCHEMA,
        "status": "SIX_VERTEX_TUTTE_CLASSIFICATION_AUDIT_PASSED",
        "labeled_graph_count": 1 << len(EDGES),
        "perfect_pairing_count": len(PAIRINGS),
        "graphs_with_perfect_matching": perfect_matching_count,
        "graphs_without_perfect_matching": no_perfect_matching_count,
        "obstruction_signature_counts": dict(sorted(signature_counts.items())),
        "claim": (
            "A graph on six vertices has no perfect matching iff it has "
            "at least two odd components, or deleting one vertex leaves at least "
            "three odd components, or two vertices cover every edge."
        ),
        "scope": (
            "Exhaustive semantic audit over all 2^15 labeled simple graphs; "
            "the cap-free proof is the six-vertex specialization of Tutte's "
            "theorem."
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
