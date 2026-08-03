#!/usr/bin/env python3
"""Audit the six-singleton extended rank-one bridge checkpoint."""

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
    from .audit_common_favorite_rank1_bridge_checkpoint import (
        BRIDGE_ORBIT,
        OUTSIDE_REPAIR_ORBIT,
    )
    from .audit_common_favorite_rank1_radius2_orbits import (
        contested_family,
        orbit_signature,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
        transfer_distance,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_common_favorite_rank1_bridge_checkpoint import (
        BRIDGE_ORBIT,
        OUTSIDE_REPAIR_ORBIT,
    )
    from audit_common_favorite_rank1_radius2_orbits import (
        contested_family,
        orbit_signature,
    )
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
        transfer_distance,
    )


SCHEMA = "common-favorite-rank1-extended-bridge-checkpoint-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-extended-bridge-search-checkpoint-v1"
SECOND_OUTSIDE_REPAIR_ORBIT = "partnerB_tripleACC_pairsAA_BB"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal_matching_witness(values, partition):
    graph = feasible_graph(values, partition)
    matching = next(
        matching
        for matching in itertools.permutations(range(N))
        if all(graph[agent][matching[agent]] for agent in range(N))
    )
    assignment = [-1] * len(values[0])
    for agent, bundle_index in enumerate(matching):
        for good in partition[bundle_index]:
            assignment[good] = agent
    if not independent.is_complete_efx0(values, assignment):
        raise AssertionError("matching failed literal EFX replay")


def run(source_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status")
        != "EXTENDED_BRIDGE45_BLOCKED_WITH_SINGLETON_REPAIRS"
        or source.get("upper") != 6
    ):
        raise ValueError("source metadata changed")
    values = core.validate_values(
        source["values"], expected_n=4, expected_m=9, lower=1, upper=6
    )
    if (
        values[1] != values[2]
        or values[1] != values[3]
        or not all(row[FAVORITE] > max(row[1:]) for row in values)
        or not threshold_passes(values, 0, RESIDUAL)
        or resident_graph(values) != ((True, False, False),) * 3
    ):
        raise AssertionError("checkpoint left the rank-one decision cell")

    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested = contested_family(neighborhood)
    bridge30 = tuple(sorted(
        set(contested)
        | {
            partition
            for partition in neighborhood
            if orbit_signature(partition) == BRIDGE_ORBIT
        }
    ))
    outside = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition)
        in {OUTSIDE_REPAIR_ORBIT, SECOND_OUTSIDE_REPAIR_ORBIT}
    )
    extended = tuple(sorted(set(bridge30) | set(outside)))
    if (
        len(neighborhood) != 63
        or len(contested) != 21
        or len(bridge30) != 30
        or len(outside) != 15
        or len(extended) != 45
    ):
        raise AssertionError("extended bridge-family census changed")
    if any(
        matching_rank(feasible_graph(values, partition)) == N
        for partition in extended
    ):
        raise AssertionError("checkpoint gained an extended-bridge repair")

    singleton_support = tuple(
        ((FAVORITE,),) + residual
        for residual in residual_partitions()
        if matching_rank(
            feasible_graph(values, ((FAVORITE,),) + residual)
        )
        == N
    )
    if len(singleton_support) != 6:
        raise AssertionError("six-singleton checkpoint census changed")
    singleton_shapes = Counter(
        "".join(map(str, sorted(map(len, partition[1:]), reverse=True)))
        for partition in singleton_support
    )

    supporting = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, 9)
        if matching_rank(feasible_graph(values, partition)) == N
    )
    for partition in supporting:
        literal_matching_witness(values, partition)
    support_shapes = Counter(
        "".join(map(str, sorted(map(len, partition), reverse=True)))
        for partition in supporting
    )
    literal_count = independent.count_complete_efx0(values)
    radius_support = tuple(
        partition
        for partition in neighborhood
        if matching_rank(feasible_graph(values, partition)) == N
    )
    radius_orbits = Counter(orbit_signature(partition) for partition in radius_support)
    source_partition = ((FAVORITE,),) + RESIDUAL
    distance_histogram = Counter(
        transfer_distance(source_partition, partition) for partition in supporting
    )
    result = {
        "schema": SCHEMA,
        "status": "EXTENDED_BRIDGE45_BLOCKED_SINGLETON6_CHECKPOINT",
        "n": 4,
        "m": 9,
        "domain": "positive integer additive valuations in [1,6]",
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "values": [list(row) for row in values],
        "strict_common_favorite": FAVORITE,
        "selected_owner_threshold_pass": True,
        "resident_graph": [list(row) for row in resident_graph(values)],
        "extended_bridge_partition_count": len(extended),
        "extended_bridge_supporting_count": 0,
        "favorite_singleton_supporting_partition_count": len(singleton_support),
        "favorite_singleton_supporting_count_by_residual_shape": dict(
            sorted(singleton_shapes.items())
        ),
        "favorite_singleton_supporting_partitions": [
            [list(bundle) for bundle in partition] for partition in singleton_support
        ],
        "radius_two_partition_count": len(neighborhood),
        "radius_two_supporting_count": len(radius_support),
        "radius_two_supporting_orbit_census": dict(sorted(radius_orbits.items())),
        "all_supporting_partition_count": len(supporting),
        "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
        "supporting_partition_transfer_distance_histogram": {
            str(key): value for key, value in sorted(distance_histogram.items())
        },
        "complete_efx_allocation_count": literal_count,
        "discovery": source["discovery"],
        "claim": (
            "This cap-6 rank-one profile blocks the 45-state extended bridge "
            "family and has exactly six favorite-singleton EFX partitions."
        ),
        "claim_boundary": (
            "This is an upper bound and exact local checkpoint, not a positive "
            "global singleton floor or a complete-EFX result."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
