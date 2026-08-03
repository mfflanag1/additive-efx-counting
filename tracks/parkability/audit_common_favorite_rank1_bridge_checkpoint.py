#!/usr/bin/env python3
"""Audit the rank-one 30-state bridge search checkpoint."""

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


SCHEMA = "common-favorite-rank1-bridge-checkpoint-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-bridge-search-checkpoint-v1"
THREE_ORBITS = {
    "partnerA_tripleAAB_pairsBB_CC",
    "partnerA_tripleBCC_pairsAA_BB",
    "partnerB_tripleABB_pairsAA_CC",
}
BRIDGE_ORBIT = "partnerB_tripleABB_pairsAA_CC"
OUTSIDE_REPAIR_ORBIT = "partnerC_tripleBBB_pairsAA_AC"


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
        or source.get("status") != "BRIDGE30_BLOCKED_WITH_SINGLETON_REPAIRS"
        or source.get("upper") != 6
    ):
        raise ValueError("source metadata changed")
    values = core.validate_values(
        source["values"], expected_n=4, expected_m=9, lower=1, upper=6
    )
    if (
        not all(row[FAVORITE] > max(row[1:]) for row in values)
        or not threshold_passes(values, 0, RESIDUAL)
        or resident_graph(values) != ((True, False, False),) * 3
    ):
        raise AssertionError("checkpoint left the rank-one decision cell")

    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested = contested_family(neighborhood)
    three_orbit = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition) in THREE_ORBITS
    )
    bridge = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition) == BRIDGE_ORBIT
    )
    bridge_union = tuple(sorted(set(contested) | set(bridge)))
    if (
        len(neighborhood) != 63
        or len(contested) != 21
        or len(three_orbit) != 27
        or len(bridge) != 9
        or len(bridge_union) != 30
    ):
        raise AssertionError("radius-two family census changed")
    if any(
        matching_rank(feasible_graph(values, partition)) == N
        for partition in bridge_union
    ):
        raise AssertionError("checkpoint gained a bridge-union repair")

    singleton_support = tuple(
        ((FAVORITE,),) + residual
        for residual in residual_partitions()
        if matching_rank(
            feasible_graph(values, ((FAVORITE,),) + residual)
        )
        == N
    )
    singleton_shapes = Counter(
        "".join(map(str, sorted(map(len, partition[1:]), reverse=True)))
        for partition in singleton_support
    )
    if len(singleton_support) != 30 or singleton_shapes != {"332": 15, "422": 15}:
        raise AssertionError("favorite-singleton census changed")

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
    if (
        len(supporting) != 213
        or support_shapes != {"3222": 183, "3321": 15, "4221": 15}
        or literal_count != 1414
    ):
        raise AssertionError("complete EFX census changed")

    radius_support = tuple(
        partition
        for partition in neighborhood
        if matching_rank(feasible_graph(values, partition)) == N
    )
    radius_orbits = Counter(orbit_signature(partition) for partition in radius_support)
    if len(radius_support) != 6 or radius_orbits != {OUTSIDE_REPAIR_ORBIT: 6}:
        raise AssertionError("radius-two outside-repair orbit changed")

    source_partition = ((FAVORITE,),) + RESIDUAL
    distance_histogram = Counter(
        transfer_distance(source_partition, partition) for partition in supporting
    )
    if distance_histogram != {1: 1, 2: 10, 3: 50, 4: 90, 5: 62}:
        raise AssertionError("transfer-distance census changed")

    result = {
        "schema": SCHEMA,
        "status": "BRIDGE30_BLOCKED_SINGLETON30_CHECKPOINT",
        "n": 4,
        "m": 9,
        "domain": "positive integer additive valuations in [1,6]",
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "values": [list(row) for row in values],
        "strict_common_favorite": FAVORITE,
        "selected_owner_threshold_pass": True,
        "resident_graph": [list(row) for row in resident_graph(values)],
        "three_orbit_partition_count": len(three_orbit),
        "three_orbit_supporting_count": 0,
        "contested_partner_partition_count": len(contested),
        "contested_partner_supporting_count": 0,
        "bridge_union_partition_count": len(bridge_union),
        "bridge_union_supporting_count": 0,
        "favorite_singleton_supporting_partition_count": len(singleton_support),
        "favorite_singleton_supporting_count_by_residual_shape": dict(
            sorted(singleton_shapes.items())
        ),
        "radius_two_partition_count": len(neighborhood),
        "radius_two_supporting_count": len(radius_support),
        "radius_two_supporting_orbit_census": dict(sorted(radius_orbits.items())),
        "all_supporting_partition_count": len(supporting),
        "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
        "supporting_partition_transfer_distance_histogram": {
            str(key): value for key, value in sorted(distance_histogram.items())
        },
        "complete_efx_allocation_count": literal_count,
        "discovery_singleton_support_count_sequence": source["discovery"][
            "singleton_support_count_sequence"
        ],
        "claim": (
            "The 30-state contested-or-bridge family can be blocked inside "
            "the cap-6 rank-one cell, but this exact profile retains 30 "
            "favorite-singleton EFX partitions."
        ),
        "claim_boundary": (
            "This is not a counterexample to the singleton-or-exchange lemma "
            "or to complete EFX. It is a seed for minimizing singleton "
            "support subject to all 30 exchange obstructions."
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
