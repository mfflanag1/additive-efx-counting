#!/usr/bin/env python3
"""Independently audit a refutation of the rank-one bridge lemma."""

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
    from .audit_common_favorite_rank1_bridge_checkpoint import BRIDGE_ORBIT
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
    from audit_common_favorite_rank1_bridge_checkpoint import BRIDGE_ORBIT
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


SCHEMA = "common-favorite-rank1-bridge-refutation-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-bridge-singleton-optimization-cpsat-v1"
RESIDUAL_TYPES = ((1, 2, 3), (4, 5, 6), (7,), (8,))


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


def hall_failure_type(values, partition):
    graph = feasible_graph(values, partition)
    if graph[1] != graph[2] or graph[1] != graph[3]:
        raise AssertionError("resident feasibility rows ceased to be identical")
    resident_neighbors = {
        bundle for bundle, accepted in enumerate(graph[1]) if accepted
    }
    if len(resident_neighbors) <= 2:
        return "three_residents_have_at_most_two_neighbors"
    outside = set(range(N)) - resident_neighbors
    if len(resident_neighbors) == 3 and not any(
        graph[0][bundle] for bundle in outside
    ):
        return "all_agents_have_at_most_three_neighbors"
    raise AssertionError("unsupported partition escaped the two-row Hall census")


def degree_signature(values, partition):
    graph = feasible_graph(values, partition)
    return f"owner{sum(graph[0])}_resident{sum(graph[1])}"


def residual_type_signature(partition):
    return tuple(sorted(
        tuple(sum(good in goods for good in bundle) for goods in RESIDUAL_TYPES)
        for bundle in partition
        if bundle != (FAVORITE,)
    ))


def run(source_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status") != "BOUNDED_RANK1_BRIDGE_LEMMA_REFUTED"
        or source.get("terminal_status") != "OPTIMAL_FIXED_POINT"
        or source.get("exact_minimum_singleton_support_count") != 0
        or source.get("upper") != 6
    ):
        raise ValueError("source metadata changed")
    proto_path = Path(source["proto"])
    if (
        not proto_path.is_file()
        or sha256(proto_path) != source["proto_sha256"]
        or proto_path.stat().st_size != source["proto_bytes"]
    ):
        raise AssertionError("source proto hash or size changed")
    values = core.validate_values(
        source["best_values"], expected_n=4, expected_m=9, lower=1, upper=6
    )
    if (
        values[1] != values[2]
        or values[1] != values[3]
        or not all(row[FAVORITE] > max(row[1:]) for row in values)
        or not threshold_passes(values, 0, RESIDUAL)
        or resident_graph(values) != ((True, False, False),) * 3
    ):
        raise AssertionError("witness left the rank-one decision cell")

    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested = contested_family(neighborhood)
    bridge = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition) == BRIDGE_ORBIT
    )
    bridge_union = tuple(sorted(set(contested) | set(bridge)))
    if (
        len(neighborhood) != 63
        or len(contested) != 21
        or len(bridge) != 9
        or len(bridge_union) != 30
    ):
        raise AssertionError("bridge-family census changed")
    bridge_support = tuple(
        partition
        for partition in bridge_union
        if matching_rank(feasible_graph(values, partition)) == N
    )
    if bridge_support:
        raise AssertionError("witness gained a bridge-union repair")
    bridge_hall_failures = Counter(
        hall_failure_type(values, partition) for partition in bridge_union
    )
    bridge_degree_signatures = Counter(
        degree_signature(values, partition) for partition in bridge_union
    )

    singleton_universe = tuple(
        ((FAVORITE,),) + residual for residual in residual_partitions()
    )
    singleton_support = tuple(
        partition
        for partition in singleton_universe
        if matching_rank(feasible_graph(values, partition)) == N
    )
    if len(singleton_universe) != 966 or singleton_support:
        raise AssertionError("witness gained a favorite-singleton repair")
    singleton_hall_failures = Counter(
        hall_failure_type(values, partition) for partition in singleton_universe
    )
    singleton_degree_signatures = Counter(
        degree_signature(values, partition) for partition in singleton_universe
    )
    type_representatives = {}
    type_multiplicities = Counter()
    for partition in singleton_universe:
        signature = residual_type_signature(partition)
        type_representatives.setdefault(signature, partition)
        type_multiplicities[signature] += 1
    type_hall_failures = Counter(
        hall_failure_type(values, partition)
        for partition in type_representatives.values()
    )
    if sum(type_multiplicities.values()) != len(singleton_universe):
        raise AssertionError("typed residual partition census changed")

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
    if not supporting or literal_count == 0:
        raise AssertionError("local-lemma witness became an EFX counterexample")

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
        "status": "RANK1_BRIDGE_LEMMA_REFUTED_COMPLETE_EFX_REMAINS",
        "n": 4,
        "m": 9,
        "domain": "positive integer additive valuations in [1,6]",
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "source_proto": str(proto_path),
        "source_proto_sha256": sha256(proto_path),
        "values": [list(row) for row in values],
        "strict_common_favorite": FAVORITE,
        "selected_owner_threshold_pass": True,
        "resident_graph": [list(row) for row in resident_graph(values)],
        "favorite_singleton_partition_count": len(singleton_universe),
        "favorite_singleton_supporting_partition_count": 0,
        "contested_partner_partition_count": len(contested),
        "bridge_orbit_partition_count": len(bridge),
        "bridge_union_partition_count": len(bridge_union),
        "bridge_union_supporting_count": 0,
        "bridge_union_hall_failure_census": dict(sorted(bridge_hall_failures.items())),
        "bridge_union_degree_signature_census": dict(
            sorted(bridge_degree_signatures.items())
        ),
        "favorite_singleton_hall_failure_census": dict(
            sorted(singleton_hall_failures.items())
        ),
        "favorite_singleton_degree_signature_census": dict(
            sorted(singleton_degree_signatures.items())
        ),
        "favorite_singleton_residual_type_class_count": len(type_representatives),
        "favorite_singleton_type_class_hall_failure_census": dict(
            sorted(type_hall_failures.items())
        ),
        "favorite_singleton_type_class_multiplicity_histogram": dict(
            sorted(Counter(type_multiplicities.values()).items())
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
        "claim": (
            "The rank-one bridge lemma is false: this profile has neither a "
            "favorite-singleton EFX partition nor an EFX partition in the "
            "30-state contested-or-bridge family."
        ),
        "claim_boundary": (
            "The profile has complete EFX allocations outside the proposed "
            "local family, so it is not an additive EFX counterexample."
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
