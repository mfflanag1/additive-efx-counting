#!/usr/bin/env python3
"""Audit exact boundaries for the mixed owner-threshold/Hall branch."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        deficient_bundle_sets,
        residual_partitions,
        threshold_passes,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        deficient_bundle_sets,
        residual_partitions,
        threshold_passes,
    )


SCHEMA = "common-favorite-mixed-hall-boundaries-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(partition):
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


def resident_graph(values, owner, partition):
    graph = feasible_graph(values, ((FAVORITE,),) + partition)
    return tuple(
        tuple(graph[agent][bundle] for bundle in range(1, N))
        for agent in range(N)
        if agent != owner
    )


def transfer_distance(left, right):
    overlap = max(
        sum(
            len(set(left[index]) & set(right[matching[index]]))
            for index in range(N)
        )
        for matching in itertools.permutations(range(N))
    )
    return M - overlap


def audit_case(path):
    source = json.loads(path.read_text())
    if (
        source.get("schema")
        != "common-favorite-threshold-pass-hall-cpsat-v1"
        or source.get("status") != "THRESHOLD_PASS_WITHOUT_SINGLETON_EFX"
        or source.get("values") is None
    ):
        raise ValueError("source is not a mixed-branch boundary")
    values = core.validate_values(
        source["values"],
        expected_n=N,
        expected_m=M,
        lower=1,
        upper=source["upper"],
    )
    if any(
        values[agent][FAVORITE] <= max(values[agent][1:])
        for agent in range(N)
    ):
        raise AssertionError("source lost its strict common favorite")

    pass_by_owner = Counter()
    pass_by_shape = Counter()
    rank_by_owner = Counter()
    rank_by_shape = Counter()
    witness_size = Counter()
    zero_neighbor_bundles = Counter()
    threshold_pass_count = 0
    first_pass = None
    for partition in residual_partitions():
        partition_shape = shape(partition)
        for owner in range(N):
            if not threshold_passes(values, owner, partition):
                continue
            threshold_pass_count += 1
            pass_by_owner[owner] += 1
            pass_by_shape[partition_shape] += 1
            graph = resident_graph(values, owner, partition)
            rank = matching_rank(graph)
            if rank >= N - 1:
                raise AssertionError("threshold pass gained a resident matching")
            rank_by_owner[(owner, rank)] += 1
            rank_by_shape[(partition_shape, rank)] += 1
            witnesses = deficient_bundle_sets(graph)
            minimum_size = min(len(item["bundles"]) for item in witnesses)
            witness_size[minimum_size] += 1
            zero_neighbor_bundles[sum(not any(row[b] for row in graph) for b in range(3))] += 1
            if first_pass is None:
                first_pass = {
                    "owner": owner,
                    "partition": [list(bundle) for bundle in partition],
                    "resident_graph": [list(row) for row in graph],
                    "resident_matching_rank": rank,
                    "deficient_bundle_sets": witnesses,
                }
    if threshold_pass_count == 0:
        raise AssertionError("boundary has no owner-threshold pass")

    support_shapes = Counter()
    distance_histogram = Counter()
    support_by_distance = {}
    support_count = 0
    singleton_support_count = 0
    selected_full = ((FAVORITE,),) + tuple(
        tuple(bundle) for bundle in source["selected_residual_partition"]
    )
    for partition in core.iter_unlabeled_nonempty_partitions(N, M):
        if matching_rank(feasible_graph(values, partition)) != N:
            continue
        support_count += 1
        support_shapes[shape(partition)] += 1
        singleton_support_count += (FAVORITE,) in partition
        distance = transfer_distance(selected_full, partition)
        distance_histogram[distance] += 1
        support_by_distance.setdefault(distance, []).append(partition)
    if singleton_support_count or set(support_shapes) != {"3222"}:
        raise AssertionError("boundary no longer has balanced-only EFX support")

    literal_count = independent.count_complete_efx0(values)
    source_audit = source["candidate_audit"]
    if (
        source_audit["favorite_singleton_supporting_partition_count"] != 0
        or source_audit["all_supporting_partition_count"] != support_count
        or source_audit["complete_efx_allocation_count"] != literal_count
    ):
        raise AssertionError("source candidate audit changed")

    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "upper": source["upper"],
        "selected_residual_shape": source["selected_residual_shape"],
        "values": [list(row) for row in values],
        "threshold_pass_count": threshold_pass_count,
        "threshold_pass_count_by_owner": {
            str(key): value for key, value in sorted(pass_by_owner.items())
        },
        "threshold_pass_count_by_residual_shape": dict(sorted(pass_by_shape.items())),
        "resident_rank_count_by_owner": {
            f"owner{owner}_rank{rank}": value
            for (owner, rank), value in sorted(rank_by_owner.items())
        },
        "resident_rank_count_by_residual_shape": {
            f"{partition_shape}_rank{rank}": value
            for (partition_shape, rank), value in sorted(rank_by_shape.items())
        },
        "minimum_deficient_bundle_set_size_count": {
            str(key): value for key, value in sorted(witness_size.items())
        },
        "zero_neighbor_bundle_count_histogram": {
            str(key): value for key, value in sorted(zero_neighbor_bundles.items())
        },
        "first_threshold_pass": first_pass,
        "favorite_singleton_supporting_partition_count": 0,
        "all_supporting_partition_count": support_count,
        "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
        "supporting_partition_transfer_distance_histogram": {
            str(key): value for key, value in sorted(distance_histogram.items())
        },
        "minimum_transfer_distance_to_efx_partition": min(distance_histogram),
        "nearest_efx_partition_count": distance_histogram[min(distance_histogram)],
        "nearest_efx_partition_sample": [
            [list(bundle) for bundle in partition]
            for partition in support_by_distance[min(distance_histogram)][:5]
        ],
        "complete_efx_allocation_count": literal_count,
    }


def run(paths, output):
    if len(paths) < 2 or output.exists():
        raise ValueError("at least two sources and a new output are required")
    cases = [audit_case(path) for path in paths]
    if len({case["selected_residual_shape"] for case in cases}) != len(cases):
        raise AssertionError("boundary shapes must be distinct")
    result = {
        "schema": SCHEMA,
        "status": "THRESHOLD_PASS_SHORTCUT_EXACTLY_REFUTED",
        "n": N,
        "m": M,
        "domain": "positive additive valuations",
        "strict_common_favorite": FAVORITE,
        "cases": cases,
        "claim": (
            "A residual partition may pass a prospective singleton owner's "
            "scalar threshold even though no partition isolating the common "
            "favorite supports EFX. In both exact boundaries every complete "
            "EFX-supporting partition instead has shape 3+2+2+2."
        ),
        "claim_boundary": (
            "These are positive witnesses against a singleton-only shortcut, "
            "not EFX counterexamples. They preserve hundreds of balanced EFX "
            "partitions and do not resolve the full common-favorite cell."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
