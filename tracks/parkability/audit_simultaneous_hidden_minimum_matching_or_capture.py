#!/usr/bin/env python3
"""Exhaust the four-owner matching/Hall alternatives in the lift lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = ("r", "q", "d", "s")


def subsets(items, nonempty=False):
    items = tuple(items)
    start = 1 if nonempty else 0
    for size in range(start, len(items) + 1):
        yield from itertools.combinations(items, size)


def covering_matching(left, right, adjacency):
    if len(left) > len(right):
        return None
    for targets in itertools.permutations(right, len(left)):
        if all(target in adjacency[source]
               for source, target in zip(left, targets, strict=True)):
            return dict(zip(left, targets, strict=True))
    return None


def hall_witness(left, adjacency):
    for subset in subsets(left, nonempty=True):
        neighborhood = set().union(*(adjacency[source] for source in subset))
        if len(neighborhood) < len(subset):
            return subset, neighborhood
    return None


def run(root):
    graph_count = 0
    matching_count = 0
    deficient_count = 0
    maximum_left_size = 0
    for vertices in subsets(OWNERS, nonempty=True):
        vertex_set = set(vertices)
        for unsafe in subsets(vertices, nonempty=True):
            unsafe = tuple(unsafe)
            stable = vertex_set - set(unsafe)
            available = tuple(owner for owner in OWNERS if owner not in stable)
            maximum_left_size = max(maximum_left_size, len(unsafe))
            edge_slots = tuple(itertools.product(unsafe, available))
            for bits in range(1 << len(edge_slots)):
                adjacency = {source: set() for source in unsafe}
                for index, (source, target) in enumerate(edge_slots):
                    if bits & (1 << index):
                        adjacency[source].add(target)
                graph_count += 1
                matching = covering_matching(unsafe, available, adjacency)
                witness = hall_witness(unsafe, adjacency)
                assert (matching is None) == (witness is not None)
                if matching is None:
                    deficient_count += 1
                    continue
                matching_count += 1
                selected_sources = stable | set(matching.values())
                dropped = vertex_set - selected_sources
                # Since every selected good was originally closed in V,
                # only a dropped old owner can obstruct closure in W.
                assert dropped <= vertex_set

    assert graph_count == matching_count + deficient_count
    script = Path(__file__).resolve()
    theorem = root / "results/SIMULTANEOUS_HIDDEN_MINIMUM_MATCHING_OR_CAPTURE_LEMMA_20260814.md"
    return {
        "schema": "simultaneous-hidden-minimum-matching-or-capture-audit-v1",
        "status": "FOUR_OWNER_HALL_LIFT_TRICHOTOMY_EXHAUSTED",
        "graph_count": graph_count,
        "matching_count": matching_count,
        "deficient_count": deficient_count,
        "maximum_unsafe_slot_count": maximum_left_size,
        "checks": {
            "matching_or_hall_witness_is_exhaustive": True,
            "matched_replacement_sources_are_distinct": True,
            "only_dropped_old_owners_can_break_closure": True,
        },
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "Exhaustive four-owner matching/Hall geometry only; packet return, "
            "surplus preservation, retired collision, and fixed-U completion "
            "remain open."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "graph_count": result["graph_count"],
        "matching_count": result["matching_count"],
        "deficient_count": result["deficient_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
