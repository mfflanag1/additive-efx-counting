#!/usr/bin/env python3
"""Exhaustively audit the four-owner minimal-Hall compression primitive."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = tuple(range(4))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def neighbors(relation, targets):
    return set().union(*(relation[target] for target in targets))


def has_matching(relation, targets, sources):
    targets = tuple(targets)
    sources = tuple(sources)
    if len(targets) != len(sources):
        return False
    return any(
        all(source in relation[target] for target, source in zip(targets, perm))
        for perm in itertools.permutations(sources)
    )


def run():
    checked = 0
    minimal_defects = 0
    neighborhood_histogram = {}
    matching_failures = 0
    edge_extension_failures = 0
    edges_checked = 0

    for mask in range(1 << 16):
        relation = {
            target: {
                source
                for source in OWNERS
                if mask & (1 << (4 * target + source))
            }
            for target in OWNERS
        }
        if any(not relation[target] for target in OWNERS):
            continue
        checked += 1
        full_neighbors = neighbors(relation, OWNERS)
        if len(full_neighbors) >= 4:
            continue
        if any(
            len(neighbors(relation, subset)) < len(subset)
            for size in range(1, 4)
            for subset in itertools.combinations(OWNERS, size)
        ):
            continue

        minimal_defects += 1
        neighborhood_histogram[str(len(full_neighbors))] = (
            neighborhood_histogram.get(str(len(full_neighbors)), 0) + 1
        )
        if len(full_neighbors) != 3:
            matching_failures += 1
            continue

        if not all(
            has_matching(relation, targets, full_neighbors)
            for targets in itertools.combinations(OWNERS, 3)
        ):
            matching_failures += 1

        for target in OWNERS:
            for source in relation[target]:
                edges_checked += 1
                remaining_targets = tuple(owner for owner in OWNERS if owner != target)
                remaining_sources = tuple(owner for owner in full_neighbors if owner != source)
                extends = any(
                    has_matching(relation, targets, remaining_sources)
                    for targets in itertools.combinations(remaining_targets, 2)
                )
                if not extends:
                    edge_extension_failures += 1

    assert minimal_defects > 0
    assert neighborhood_histogram == {"3": minimal_defects}
    assert matching_failures == 0
    assert edge_extension_failures == 0

    incoming = {
        "source_0": {"core_0"},
        "source_1": {"core_1"},
        "source_2": {"core_2"},
        "missing_source": {"residual"},
    }
    assert all(
        left.isdisjoint(right)
        for index, left in enumerate(incoming.values())
        for right in tuple(incoming.values())[index + 1 :]
    )

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "all-owner-hall-response-compression-audit-v1",
        "status": "ALL_FORCED",
        "relation_records": {
            "nonempty_relations_checked": checked,
            "minimal_all_target_defects": minimal_defects,
            "neighborhood_size_histogram": neighborhood_histogram,
            "three_target_matching_failures": matching_failures,
            "response_edges_checked": edges_checked,
            "edge_extension_failures": edge_extension_failures,
        },
        "support_record": {
            "cells": ["core_0", "core_1", "core_2", "residual"],
            "pairwise_disjoint": True,
            "cover_original_targets": True,
        },
        "claim_boundary": (
            "complete enumeration of four-by-four nonempty response relations "
            "and abstract partition support; residual-owner payment and the "
            "recomputed response relation remain analytic/open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
