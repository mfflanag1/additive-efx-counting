#!/usr/bin/env python3
"""Audit partial-EFX entry states after an essential single-wall failure."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )


SCHEMA = "row-merge-partial-entry-audit-v1"
N = 4
MATCHINGS = tuple(itertools.permutations(range(N)))


def assignment_for_matching(partition, matching, m):
    assignment = [None] * m
    for agent, bundle_index in enumerate(matching):
        for good in partition[bundle_index]:
            assignment[good] = agent
    if any(owner is None for owner in assignment):
        raise AssertionError("the wall partition is not complete")
    return assignment


def partition_for_assignment(assignment):
    return canonical(
        tuple(
            tuple(good for good, owner in enumerate(assignment) if owner == agent)
            for agent in range(N)
        )
    )


def wall_matchings(source):
    graph = source["audit"]["wall_feasibility_graph"]
    return tuple(
        matching
        for matching in MATCHINGS
        if all(graph[agent][matching[agent]] for agent in range(N))
    )


def deleted_wall_partition(partition, deleted_good):
    return canonical(
        tuple(
            tuple(good for good in bundle if good != deleted_good)
            for bundle in partition
        )
    )


def audit_source(path: Path) -> dict:
    source = json.loads(path.read_text())
    if source.get("status") not in {
        "RADIUS_PIVOT_REFUTATION_FOUND",
        "PARTIAL_ENTRY_RADIUS_REFUTATION_FOUND",
    }:
        raise ValueError("a SAT single-wall refutation source is required")
    m = source["m"]
    values = source["post_wall_values"]
    partition = source["wall_partition"]
    matchings = wall_matchings(source)
    if not matchings:
        raise AssertionError("the wall partition has no supporting matching")

    direct_entries = []
    for matching in matchings:
        assignment = assignment_for_matching(partition, matching, m)
        for deleted_good in range(m):
            partial = assignment[:]
            partial[deleted_good] = None
            if independent.is_removed_good_efx0(values, partial, deleted_good):
                direct_entries.append({
                    "matching": list(matching),
                    "deleted_good": deleted_good,
                    "assignment": partial,
                })

    partition_support = Counter()
    distance_histogram = Counter()
    nearest = None
    for deleted_good in range(m):
        remaining = tuple(good for good in range(m) if good != deleted_good)
        origin = deleted_wall_partition(partition, deleted_good)
        seen = set()
        for owners in itertools.product(range(N), repeat=m - 1):
            assignment = [None] * m
            for good, owner in zip(remaining, owners):
                assignment[good] = owner
            if not independent.is_removed_good_efx0(
                values, assignment, deleted_good
            ):
                continue
            candidate = partition_for_assignment(assignment)
            partition_support[(deleted_good, candidate)] += 1
            if candidate in seen:
                continue
            seen.add(candidate)
            distance = transfer_distance(origin, candidate)
            distance_histogram[distance] += 1
            record = (distance, deleted_good, candidate, tuple(assignment))
            if nearest is None or record < nearest:
                nearest = record
    if nearest is None:
        raise AssertionError("the post-wall profile has no one-good partial EFX allocation")

    witness_size = source["minimal_hall_witness_size"]
    deficient_block_indices = tuple(range(witness_size))
    deficient_goods = tuple(
        good
        for bundle_index in deficient_block_indices
        for good in partition[bundle_index]
    )
    outside = tuple(
        tuple(partition[bundle_index])
        for bundle_index in range(witness_size, N)
    )
    restart_support = Counter()
    nearest_restart = None
    for deleted_good in deficient_goods:
        remaining = tuple(good for good in deficient_goods if good != deleted_good)
        origin = deleted_wall_partition(partition, deleted_good)
        internal_partitions = set()
        for labels in itertools.product(range(witness_size), repeat=len(remaining)):
            internal = canonical(
                tuple(
                    tuple(
                        good
                        for good, label in zip(remaining, labels)
                        if label == bundle
                    )
                    for bundle in range(witness_size)
                )
            )
            internal_partitions.add(internal)
        for internal in sorted(internal_partitions):
            candidate = canonical((*internal, *outside))
            count = matching_count(graph(values, candidate))
            if not count:
                continue
            restart_support[(deleted_good, candidate)] = count
            distance = transfer_distance(origin, candidate)
            record = (distance, deleted_good, candidate)
            if nearest_restart is None or record < nearest_restart:
                nearest_restart = record
    if nearest_restart is None:
        raise AssertionError("the recorded source has no deficient-block partial restart")

    (
        nearest_distance,
        nearest_deleted_good,
        nearest_partition,
        nearest_assignment,
    ) = nearest
    restart_distance, restart_good, restart_partition = nearest_restart
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "minimal_hall_witness_size": source["minimal_hall_witness_size"],
        "wall_supporting_matching_count": len(matchings),
        "direct_deletion_entry_count": len(direct_entries),
        "direct_deletion_entries": direct_entries,
        "partial_efx_allocation_count": sum(partition_support.values()),
        "partial_efx_partition_count": len(partition_support),
        "partial_efx_partition_distance_histogram": {
            str(distance): distance_histogram[distance]
            for distance in sorted(distance_histogram)
        },
        "minimum_partial_efx_transfer_distance": nearest_distance,
        "nearest_deleted_good": nearest_deleted_good,
        "nearest_partial_efx_partition": [
            list(bundle) for bundle in nearest_partition
        ],
        "nearest_partial_efx_assignment": list(nearest_assignment),
        "designated_deficient_block_bundle_indices": list(
            deficient_block_indices
        ),
        "deficient_block_restart_partition_count": len(restart_support),
        "deficient_block_restart_allocation_count": sum(restart_support.values()),
        "minimum_deficient_block_restart_transfer_distance": restart_distance,
        "nearest_deficient_block_restart_deleted_good": restart_good,
        "nearest_deficient_block_restart_partition": [
            list(bundle) for bundle in restart_partition
        ],
    }


def run(source_paths: list[Path], output_path: Path) -> dict:
    if output_path.exists():
        raise ValueError("output path must be new")
    records = [audit_source(path) for path in source_paths]
    result = {
        "schema": SCHEMA,
        "status": "PARTIAL_ENTRY_CENSUS_AUDITED",
        "records": records,
        "claim": (
            "A same-assignment one-good deletion need not enter the partial-EFX "
            "state space after an essential single-wall failure."
        ),
        "claim_boundary": (
            "This is an exact census of three recorded seven-good profiles. "
            "It does not rule out a different partial allocation, a longer "
            "exchange chain, or complete EFX continuation."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
