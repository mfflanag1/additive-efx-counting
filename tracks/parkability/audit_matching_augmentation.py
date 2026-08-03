#!/usr/bin/env python3
"""Audit plateau augmentation of partition EFX-matching rank."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

try:
    from . import core
except ImportError:
    import core


def canonical_partition(
    bundles: list[list[int]],
) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))


def matching_rank(graph: tuple[tuple[bool, ...], ...]) -> int:
    n = len(graph)
    return max(
        sum(graph[agent][matching[agent]] for agent in range(n))
        for matching in itertools.permutations(range(n))
    )


def feasible_graph(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> tuple[tuple[bool, ...], ...]:
    n = len(values)
    return tuple(
        tuple(
            all(
                own_bundle == target
                or sum(values[agent][good] for good in partition[own_bundle])
                >= (
                    sum(values[agent][good] for good in partition[target])
                    - min(values[agent][good] for good in partition[target])
                )
                for target in range(n)
            )
            for own_bundle in range(n)
        )
        for agent in range(n)
    )


def transfer_neighbors(
    partition: tuple[tuple[int, ...], ...],
) -> set[tuple[tuple[int, ...], ...]]:
    result = set()
    n = len(partition)
    for source, target in itertools.permutations(range(n), 2):
        if len(partition[source]) == 1:
            continue
        for good in partition[source]:
            bundles = [list(bundle) for bundle in partition]
            bundles[source].remove(good)
            bundles[target].append(good)
            result.add(canonical_partition(bundles))
    return result


def audit(
    values: tuple[tuple[int, ...], ...],
    source: tuple[tuple[int, ...], ...] | None = None,
) -> dict:
    n = len(values)
    m = len(values[0])
    partitions = list(core.iter_unlabeled_nonempty_partitions(n, m))
    ranks = {
        partition: matching_rank(feasible_graph(values, partition))
        for partition in partitions
    }
    neighbors = {
        partition: transfer_neighbors(partition)
        for partition in partitions
    }
    seen = set()
    components = Counter()
    trapped = []
    exit_counts = []
    component_summaries = []
    for partition in partitions:
        rank = ranks[partition]
        if rank == n or partition in seen:
            continue
        component = {partition}
        stack = [partition]
        seen.add(partition)
        augmenting_exits = set()
        while stack:
            current = stack.pop()
            for neighbor in neighbors[current]:
                if ranks[neighbor] > rank:
                    augmenting_exits.add((current, neighbor))
                elif ranks[neighbor] == rank and neighbor not in seen:
                    seen.add(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components[rank] += 1
        exit_counts.append(len(augmenting_exits))
        component_summaries.append({
            "rank": rank,
            "component_size": len(component),
            "augmenting_exit_count": len(augmenting_exits),
            "partition_sample": [
                [list(bundle) for bundle in item]
                for item in sorted(component)[:3]
            ],
            "augmenting_exit_sample": [
                {
                    "source": [list(bundle) for bundle in source],
                    "target": [list(bundle) for bundle in target],
                    "target_rank": ranks[target],
                }
                for source, target in sorted(augmenting_exits)[:5]
            ],
        })
        if not augmenting_exits:
            trapped.append({
                "rank": rank,
                "component_size": len(component),
                "partition_sample": [
                    [list(bundle) for bundle in item]
                    for item in sorted(component)[:5]
                ],
            })
    source_profile = None
    if source is not None:
        if source not in ranks:
            raise ValueError("source must be a nonempty partition of all goods")
        distances = {source: 0}
        frontier = [source]
        while frontier:
            current = frontier.pop(0)
            for neighbor in neighbors[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    frontier.append(neighbor)
        source_profile = {
            "source_partition": [list(bundle) for bundle in source],
            "source_rank": ranks[source],
            "minimum_distance_to_perfect_rank": min(
                distance
                for partition, distance in distances.items()
                if ranks[partition] == n
            ),
            "rank_histogram_by_distance": {
                str(distance): {
                    str(rank): count
                    for rank, count in sorted(
                        Counter(
                            ranks[partition]
                            for partition, item_distance in distances.items()
                            if item_distance == distance
                        ).items()
                    )
                }
                for distance in sorted(set(distances.values()))
            },
        }
    return {
        "n": n,
        "m": m,
        "partition_count": len(partitions),
        "rank_histogram": {
            str(rank): count
            for rank, count in sorted(Counter(ranks.values()).items())
        },
        "nonperfect_plateau_component_count_by_rank": {
            str(rank): count for rank, count in sorted(components.items())
        },
        "trapped_component_count": len(trapped),
        "trapped_component_sample": trapped[:10],
        "minimum_augmenting_exit_count": min(exit_counts, default=None),
        "augmenting_exit_count_histogram": {
            str(count): frequency
            for count, frequency in sorted(Counter(exit_counts).items())
        },
        "narrowest_component_sample": sorted(
            component_summaries,
            key=lambda record: (
                record["augmenting_exit_count"],
                record["rank"],
                record["component_size"],
            ),
        )[:10],
        "perfect_partition_count": sum(rank == n for rank in ranks.values()),
        "source_radius_profile": source_profile,
    }


def run_random(
    n: int,
    m: int,
    samples: int,
    maximum: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    for index in range(samples):
        values = tuple(
            tuple(rng.randint(1, maximum) for _ in range(m))
            for _ in range(n)
        )
        result = audit(values)
        if result["trapped_component_count"]:
            return {
                "status": "COUNTEREXAMPLE",
                "instances_checked": index + 1,
                "maximum": maximum,
                "seed": seed,
                "values": [list(row) for row in values],
                **result,
            }
    return {
        "status": "NO_COUNTEREXAMPLE",
        "instances_checked": samples,
        "maximum": maximum,
        "seed": seed,
        "n": n,
        "m": m,
    }


def run_exhaustive(
    n: int,
    m: int,
    levels: tuple[int, ...],
) -> dict:
    if not levels or any(level < 1 for level in levels):
        raise ValueError("levels must be positive")
    checked = 0
    for flat in itertools.product(levels, repeat=n * m):
        values = tuple(
            tuple(flat[agent * m:(agent + 1) * m])
            for agent in range(n)
        )
        result = audit(values)
        checked += 1
        if result["trapped_component_count"]:
            return {
                "status": "COUNTEREXAMPLE",
                "mode": "exhaustive",
                "instances_checked": checked,
                "levels": list(levels),
                "values": [list(row) for row in values],
                **result,
            }
    return {
        "status": "EXHAUSTED_NO_COUNTEREXAMPLE",
        "mode": "exhaustive",
        "instances_checked": checked,
        "levels": list(levels),
        "n": n,
        "m": m,
    }


def parse_levels(raw: str) -> tuple[int, ...]:
    levels = tuple(int(item) for item in raw.split(","))
    if len(levels) != len(set(levels)):
        raise ValueError("levels must be distinct")
    return levels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--n", type=int)
    parser.add_argument("--m", type=int)
    parser.add_argument("--samples", type=int)
    parser.add_argument("--levels")
    parser.add_argument("--maximum", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--source",
        help="slash-separated bundles of comma-separated goods",
    )
    args = parser.parse_args()
    if args.instance is not None:
        raw = json.loads(args.instance.read_text())
        values = core.validate_values(raw["values"], lower=1)
        source = None
        if args.source is not None:
            source = canonical_partition([
                [int(good) for good in bundle.split(",") if good]
                for bundle in args.source.split("/")
            ])
        result = {
            "status": "AUDITED",
            "values": [list(row) for row in values],
            **audit(values, source),
        }
    elif args.levels is not None:
        if args.n is None or args.m is None:
            parser.error("exhaustive mode requires --n and --m")
        result = run_exhaustive(args.n, args.m, parse_levels(args.levels))
    else:
        if args.n is None or args.m is None or args.samples is None:
            parser.error("random mode requires --n, --m, and --samples")
        result = run_random(
            args.n,
            args.m,
            args.samples,
            args.maximum,
            args.seed,
        )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
