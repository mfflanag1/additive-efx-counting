#!/usr/bin/env python3
"""Audit exact distances from deficient to perfect-rank bundle partitions."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import (
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import (
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )


Partition = tuple[tuple[int, ...], ...]


def perfect_matching_count(
    graph: tuple[tuple[bool, ...], ...],
) -> int:
    n = len(graph)
    return sum(
        all(graph[agent][matching[agent]] for agent in range(n))
        for matching in itertools.permutations(range(n))
    )


def run(values_path: Path, literal_audit: bool) -> dict:
    raw = json.loads(values_path.read_text())
    values = core.validate_values(raw["values"], lower=1)
    n = len(values)
    m = len(values[0])
    partitions = list(core.iter_unlabeled_nonempty_partitions(n, m))
    graphs = {
        partition: feasible_graph(values, partition)
        for partition in partitions
    }
    ranks = {
        partition: matching_rank(graph)
        for partition, graph in graphs.items()
    }
    perfect = [partition for partition in partitions if ranks[partition] == n]
    if not perfect:
        literal_count = independent.count_complete_efx0(values)
        if literal_count:
            raise AssertionError("matching and literal EFX enumerators disagree")
        return {
            "schema": "matching-radius-landscape-v1",
            "status": "ZERO_COMPLETE_EFX",
            "n": n,
            "m": m,
            "source": str(values_path.resolve()),
            "source_sha256": hashlib.sha256(values_path.read_bytes()).hexdigest(),
            "values": [list(row) for row in values],
            "partition_count": len(partitions),
            "perfect_partition_count": 0,
            "complete_efx0_count": 0,
        }

    distances = {partition: 0 for partition in perfect}
    next_step: dict[Partition, Partition] = {}
    queue = deque(perfect)
    while queue:
        current = queue.popleft()
        for neighbor in transfer_neighbors(current):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[current] + 1
            next_step[neighbor] = current
            queue.append(neighbor)
    if len(distances) != len(partitions):
        raise AssertionError("partition-transfer graph is disconnected")

    rank_distance_histogram = {
        str(rank): {
            str(distance): count
            for distance, count in sorted(Counter(
                distances[partition]
                for partition in partitions
                if ranks[partition] == rank
            ).items())
        }
        for rank in sorted(set(ranks.values()))
    }
    target_rank = n - 1
    target_partitions = [
        partition for partition in partitions if ranks[partition] == target_rank
    ]
    maximum = max(
        (distances[partition] for partition in target_partitions),
        default=None,
    )
    witness = (
        next(
            partition
            for partition in target_partitions
            if distances[partition] == maximum
        )
        if maximum is not None
        else None
    )
    path = []
    current = witness
    while current is not None:
        path.append(current)
        current = next_step.get(current)

    matching_allocation_count = sum(
        perfect_matching_count(graphs[partition])
        for partition in perfect
    )
    literal_count = (
        independent.count_complete_efx0(values)
        if literal_audit
        else None
    )
    if literal_count is not None and literal_count != matching_allocation_count:
        raise AssertionError("matching and literal EFX counts disagree")
    return {
        "schema": "matching-radius-landscape-v1",
        "status": "AUDITED",
        "n": n,
        "m": m,
        "source": str(values_path.resolve()),
        "source_sha256": hashlib.sha256(values_path.read_bytes()).hexdigest(),
        "values": [list(row) for row in values],
        "partition_count": len(partitions),
        "rank_histogram": {
            str(rank): count
            for rank, count in sorted(Counter(ranks.values()).items())
        },
        "rank_distance_histogram": rank_distance_histogram,
        "perfect_partition_count": len(perfect),
        "matching_complete_efx0_count": matching_allocation_count,
        "literal_complete_efx0_count": literal_count,
        "target_rank": target_rank,
        "maximum_target_rank_distance_to_perfect": maximum,
        "maximum_distance_witness": (
            [list(bundle) for bundle in witness]
            if witness is not None
            else None
        ),
        "witness_path_to_perfect": [
            [list(bundle) for bundle in partition]
            for partition in path
        ],
        "witness_path_ranks": [ranks[partition] for partition in path],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--literal-audit", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.values.is_file() or args.output.exists():
        parser.error("an existing values file and new output are required")
    result = run(args.values, args.literal_audit)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
