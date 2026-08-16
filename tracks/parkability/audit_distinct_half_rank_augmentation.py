#!/usr/bin/env python3
"""Stress-test rank-plateau augmentation in the distinct-half EFX gate."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-rank-augmentation-audit-v1"
N = 4
M = 9
FAVORITE = 0
SOURCE_FILES = (
    "efx49_common_favorite_real_shape6111_session1.json",
    "efx49_universal_threshold_distinct_reps_cegar_session1.json",
    "efx49_universal_threshold_balanced_envelope_cegar_session1.json",
    "efx49_universal_threshold_balanced_cegar_session1.json",
)
NEGATIVE_CONTROL = "efx49_common_favorite_real_frontier_audit.json"


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def load_values(path: Path):
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        raw = payload["trace"][-1]["values"]
    return tuple(tuple(map(int, row)) for row in raw)


def universal_threshold_failure(row):
    favorite = row[FAVORITE]
    residual = sorted(row[1:], reverse=True)
    return (
        residual[4] + residual[5] + residual[6] > favorite
        and (
            residual[2] + residual[6] > favorite
            or residual[3] + residual[4] > favorite
        )
    )


def half_matching(values):
    return next(
        (
            goods
            for goods in itertools.permutations(range(1, M), N)
            if all(
                2 * values[agent][goods[agent]] > values[agent][FAVORITE]
                for agent in range(N)
            )
        ),
        None,
    )


def audit_branch(values):
    if any(
        row[FAVORITE] <= max(row[1:]) or not universal_threshold_failure(row)
        for row in values
    ):
        raise AssertionError("profile is outside the universal-threshold branch")
    representatives = half_matching(values)
    if representatives is None:
        raise AssertionError("profile is outside the distinct-representative branch")
    return representatives


def build_state_graph():
    universe = tuple(favorite_pair_balanced_universe())
    index = {partition: position for position, partition in enumerate(universe)}
    neighbors = []
    for partition in universe:
        adjacent = set()
        for left, right in itertools.combinations(range(N), 2):
            for left_good in partition[left]:
                for right_good in partition[right]:
                    bundles = [list(bundle) for bundle in partition]
                    bundles[left].remove(left_good)
                    bundles[left].append(right_good)
                    bundles[right].remove(right_good)
                    bundles[right].append(left_good)
                    candidate = canonical(bundles)
                    position = index.get(candidate)
                    if (
                        position is not None
                        and len(next(bundle for bundle in candidate if FAVORITE in bundle))
                        == 2
                    ):
                        adjacent.add(position)
        neighbors.append(tuple(sorted(adjacent)))
    if (
        len(universe) != 840
        or sum(map(len, neighbors)) != 2 * 8820
        or {len(items) for items in neighbors} != {21}
    ):
        raise AssertionError("favorite-pair single-swap graph census changed")
    return universe, tuple(neighbors)


def landscape(values, universe, neighbors):
    ranks = tuple(
        matching_rank(feasible_graph(values, partition))
        for partition in universe
    )
    seen = set()
    components = Counter()
    exits = []
    augmentation_lengths = []
    trapped = []
    for start, rank in enumerate(ranks):
        if rank == N or start in seen:
            continue
        component = []
        higher = set()
        boundary = set()
        stack = [start]
        seen.add(start)
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in neighbors[current]:
                if ranks[neighbor] > rank:
                    higher.add(neighbor)
                    boundary.add(current)
                elif ranks[neighbor] == rank and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components[rank] += 1
        exits.append(len(higher))
        if boundary:
            component_set = set(component)
            distances = {position: 0 for position in boundary}
            queue = list(boundary)
            while queue:
                current = queue.pop(0)
                for neighbor in neighbors[current]:
                    if (
                        neighbor in component_set
                        and neighbor not in distances
                        and ranks[neighbor] == rank
                    ):
                        distances[neighbor] = distances[current] + 1
                        queue.append(neighbor)
            if len(distances) != len(component):
                raise AssertionError("plateau distance traversal lost a state")
            augmentation_lengths.append(max(distances.values()) + 1)
        if not higher:
            trapped.append({
                "rank": rank,
                "component_size": len(component),
                "partition": [list(bundle) for bundle in universe[component[0]]],
            })
    return {
        "matching_rank_histogram": {
            str(rank): count for rank, count in sorted(Counter(ranks).items())
        },
        "nonperfect_plateau_components_by_rank": {
            str(rank): count for rank, count in sorted(components.items())
        },
        "minimum_higher_rank_exit_count": min(exits, default=None),
        "maximum_rank_preserving_path_then_exit_length": (
            max(augmentation_lengths, default=None)
        ),
        "trapped_nonperfect_plateau_count": len(trapped),
        "trapped_nonperfect_plateau_sample": trapped[:1],
        "perfect_partition_count": sum(rank == N for rank in ranks),
    }


def random_row(rng, maximum_favorite):
    while True:
        favorite = rng.randint(4, maximum_favorite)
        row = (favorite,) + tuple(
            rng.randint(1, favorite - 1) for _ in range(M - 1)
        )
        if universal_threshold_failure(row):
            return row


def random_profile(rng, maximum_favorite):
    while True:
        values = tuple(random_row(rng, maximum_favorite) for _ in range(N))
        if half_matching(values) is not None:
            return values


def audit(results_dir, random_profiles, seed, maximum_favorite):
    universe, neighbors = build_state_graph()
    source_records = []
    for filename in SOURCE_FILES:
        values = load_values(results_dir / filename)
        representatives = audit_branch(values)
        record = landscape(values, universe, neighbors)
        if record["trapped_nonperfect_plateau_count"]:
            raise AssertionError((filename, "source gained a trapped plateau"))
        source_records.append({
            "source": filename,
            "half_favorite_representatives": list(representatives),
            **record,
        })

    rng = random.Random(seed)
    minimum_random_exit = None
    maximum_random_path = None
    for profile_index in range(random_profiles):
        values = random_profile(rng, maximum_favorite)
        record = landscape(values, universe, neighbors)
        if record["trapped_nonperfect_plateau_count"]:
            raise AssertionError((profile_index, values, record))
        exit_count = record["minimum_higher_rank_exit_count"]
        if exit_count is not None:
            minimum_random_exit = (
                exit_count
                if minimum_random_exit is None
                else min(minimum_random_exit, exit_count)
            )
        path_length = record["maximum_rank_preserving_path_then_exit_length"]
        if path_length is not None:
            maximum_random_path = (
                path_length
                if maximum_random_path is None
                else max(maximum_random_path, path_length)
            )

    negative_values = load_values(results_dir / NEGATIVE_CONTROL)
    negative_record = landscape(negative_values, universe, neighbors)
    if (
        negative_record["perfect_partition_count"] != 0
        or negative_record["trapped_nonperfect_plateau_count"] == 0
    ):
        raise AssertionError("negative control no longer separates the candidate")

    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_RANK_AUGMENTATION_STRESS_AUDIT_PASSED",
        "state_graph": {
            "favorite_pair_balanced_partitions": len(universe),
            "undirected_single_good_swap_edges": sum(map(len, neighbors)) // 2,
            "degree": len(neighbors[0]),
        },
        "candidate": (
            "Every connected plateau of constant EFX-feasibility matching "
            "rank below four has a single-good-swap exit to a partition of "
            "higher rank in the universal-threshold distinct-half branch."
        ),
        "source_profile_records": source_records,
        "deterministic_random_profiles": random_profiles,
        "random_seed": seed,
        "maximum_random_favorite": maximum_favorite,
        "minimum_random_higher_rank_exit_count": minimum_random_exit,
        "maximum_random_rank_preserving_path_then_exit_length": (
            maximum_random_path
        ),
        "negative_control": {
            "source": NEGATIVE_CONTROL,
            "satisfies_universal_threshold_branch": all(
                universal_threshold_failure(row) for row in negative_values
            ),
            "has_half_favorite_matching": half_matching(negative_values) is not None,
            **negative_record,
        },
        "scope_warning": (
            "This finite deterministic audit can falsify the augmentation "
            "candidate but cannot prove its cap-free real-valued statement."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260731)
    parser.add_argument("--maximum-favorite", type=int, default=80)
    args = parser.parse_args()
    if args.random_profiles < 0 or args.maximum_favorite < 4:
        parser.error("invalid stress-test limits")
    result = audit(
        args.results_dir,
        args.random_profiles,
        args.seed,
        args.maximum_favorite,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
