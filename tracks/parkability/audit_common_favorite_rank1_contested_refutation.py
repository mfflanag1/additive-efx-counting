#!/usr/bin/env python3
"""Audit the cap-6 refutation of the 21-state contested-partner lemma."""

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
        conversion_partitions,
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
        conversion_partitions,
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


SCHEMA = "common-favorite-rank1-contested-refutation-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def zero_neighbor_count(values, partition):
    graph = feasible_graph(values, partition)
    return sum(not any(row[bundle] for row in graph) for bundle in range(N))


def bridge_family(neighborhood):
    return tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition) == "partnerB_tripleABB_pairsAA_CC"
    )


def validate_cell(values, blocked):
    return (
        all(row[FAVORITE] > max(row[1:]) for row in values)
        and threshold_passes(values, 0, RESIDUAL)
        and resident_graph(values) == ((True, False, False),) * 3
        and all(matching_rank(feasible_graph(values, part)) < N for part in blocked)
        and all(zero_neighbor_count(values, part) >= 1 for part in blocked)
    )


def add_supported_singletons(values, pool, pool_set):
    survivors = []
    for residual in residual_partitions():
        partition = ((FAVORITE,),) + residual
        key = canonical(partition)
        if key in pool_set:
            continue
        if matching_rank(feasible_graph(values, partition)) == N:
            survivors.append(partition)
    for partition in survivors:
        pool.append(partition)
        pool_set.add(canonical(partition))
    return survivors


def replay_trace(source, blocked, pool, pool_set):
    sequence = []
    for expected_iteration, record in enumerate(source["cegar_trace"], 1):
        values = tuple(tuple(row) for row in record["values"])
        if (
            record["iteration"] != expected_iteration
            or record["singleton_pool_size_before"] != len(pool)
            or not validate_cell(values, blocked)
        ):
            raise AssertionError("CEGAR trace left the decision cell")
        survivors = add_supported_singletons(values, pool, pool_set)
        if len(survivors) != record[
            "supported_unpooled_singleton_partition_count"
        ]:
            raise AssertionError("CEGAR singleton census changed")
        sequence.append(len(survivors))
    return sequence


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
        raise AssertionError("graph matching failed literal EFX replay")


def validate_source(source, upper, scope, hall_obstruction="zero_neighbor"):
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("upper") != upper
        or source.get("conversion_scope") != scope
        or source.get("hall_obstruction") != hall_obstruction
        or source.get("cell_symmetry") is not True
        or source.get("cegar_singletons") is not True
    ):
        raise ValueError("source metadata changed")
    proto = Path(source["proto"])
    if not proto.is_file() or sha256(proto) != source["proto_sha256"]:
        raise AssertionError("source CP-SAT proto changed")


def run(session1_path, session2_path, bridge_boundary_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested = contested_family(neighborhood)
    bridge = bridge_family(neighborhood)
    if len(neighborhood) != 63 or len(contested) != 21 or len(bridge) != 9:
        raise AssertionError("radius-two family census changed")

    session1 = json.loads(session1_path.read_text())
    validate_source(session1, 6, "radius2_contested")
    if session1.get("status") != "ITERATION_LIMIT":
        raise ValueError("session-one endpoint changed")
    pool = []
    pool_set = set()
    sequence1 = replay_trace(session1, contested, pool, pool_set)
    if sequence1 != [290, 13, 6] or len(pool) != 309:
        raise AssertionError("session-one CEGAR boundary changed")

    session2 = json.loads(session2_path.read_text())
    validate_source(session2, 6, "radius2_contested")
    if (
        session2.get("status") != "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
        or session2.get("solver_status") != "OPTIMAL"
        or len(session2.get("seed_imports", [])) != 1
        or session2["seed_imports"][0]["source_sha256"] != sha256(session1_path)
        or session2["seed_imports"][0]["new_singleton_count"] != len(pool)
    ):
        raise ValueError("session-two endpoint changed")
    sequence2 = replay_trace(session2, contested, pool, pool_set)
    if sequence2 != [4, 0] or len(pool) != 313:
        raise AssertionError("session-two CEGAR closure changed")

    values = core.validate_values(
        session2["values"], expected_n=4, expected_m=9, lower=1, upper=6
    )
    if values != tuple(tuple(row) for row in session2["cegar_trace"][-1]["values"]):
        raise AssertionError("terminal candidate changed")
    if not validate_cell(values, contested):
        raise AssertionError("terminal candidate left the decision cell")
    singleton_support = sum(
        matching_rank(feasible_graph(values, ((FAVORITE,),) + residual)) == N
        for residual in residual_partitions()
    )
    if singleton_support:
        raise AssertionError("terminal candidate gained singleton EFX")

    supporting = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, 9)
        if matching_rank(feasible_graph(values, partition)) == N
    )
    for partition in supporting:
        literal_matching_witness(values, partition)
    literal_count = independent.count_complete_efx0(values)
    if len(supporting) != 285 or literal_count != 3168:
        raise AssertionError("terminal EFX census changed")

    radius_support = tuple(
        partition
        for partition in neighborhood
        if matching_rank(feasible_graph(values, partition)) == N
    )
    if set(radius_support) != set(bridge):
        raise AssertionError("nearest bridge orbit changed")
    if any(
        feasible_graph(values, partition) != ((True,) * N,) * N
        for partition in bridge
    ):
        raise AssertionError("bridge orbit lost universal feasibility")

    bridge_boundary = json.loads(bridge_boundary_path.read_text())
    validate_source(bridge_boundary, 6, "radius2_bridge", "any")
    if (
        bridge_boundary.get("status") != "MASTER_UNKNOWN"
        or bridge_boundary.get("solver_status") != "UNKNOWN"
        or bridge_boundary.get("hall_obstruction") != "any"
        or bridge_boundary.get("blocked_partition_count") != 30
        or bridge_boundary.get("singleton_obstruction_pool_size") != 313
        or bridge_boundary.get("cegar_iterations") != 0
        or bridge_boundary.get("values") is not None
        or [seed["source_sha256"] for seed in bridge_boundary["seed_imports"]]
        != [sha256(session1_path), sha256(session2_path)]
        or [
            seed["new_singleton_count"]
            for seed in bridge_boundary["seed_imports"]
        ]
        != [309, 4]
    ):
        raise ValueError("bridge-union boundary changed")

    source_partition = ((FAVORITE,),) + RESIDUAL
    distance_histogram = Counter(
        transfer_distance(source_partition, partition) for partition in supporting
    )
    orbit_census = Counter(orbit_signature(partition) for partition in radius_support)
    zero_histogram = Counter(
        zero_neighbor_count(values, partition) for partition in contested
    )
    local_ranks = [
        matching_rank(feasible_graph(values, partition))
        for partition in conversion_partitions()
    ]
    result = {
        "schema": SCHEMA,
        "status": "CONTESTED_PARTNER_LEMMA_REFUTED_BRIDGE_ORBIT_OPEN",
        "n": 4,
        "m": 9,
        "domain": "positive integer additive valuations in [1,6]",
        "values": [list(row) for row in values],
        "strict_common_favorite": FAVORITE,
        "selected_owner_threshold_pass": True,
        "resident_graph": [list(row) for row in resident_graph(values)],
        "favorite_singleton_supporting_partition_count": singleton_support,
        "local_conversion_ranks": local_ranks,
        "contested_partner_partition_count": len(contested),
        "contested_partner_supporting_count": 0,
        "contested_partner_zero_neighbor_count_histogram": {
            str(key): value for key, value in sorted(zero_histogram.items())
        },
        "radius_two_partition_count": len(neighborhood),
        "radius_two_supporting_count": len(radius_support),
        "radius_two_supporting_orbit_census": dict(sorted(orbit_census.items())),
        "bridge_orbit_partition_count": len(bridge),
        "bridge_orbit_supporting_count": len(bridge),
        "bridge_orbit_all_feasibility_graphs_complete": True,
        "bridge_union_boundary": {
            "partition_count": len(contested) + len(bridge),
            "source": str(bridge_boundary_path),
            "source_sha256": sha256(bridge_boundary_path),
            "proto_sha256": bridge_boundary["proto_sha256"],
            "singleton_obstruction_pool_size": bridge_boundary[
                "singleton_obstruction_pool_size"
            ],
            "solver_status": bridge_boundary["solver_status"],
            "solver_wall_seconds": bridge_boundary["solver_wall_seconds"],
        },
        "all_supporting_partition_count": len(supporting),
        "supporting_partition_count_by_shape": {"3222": len(supporting)},
        "supporting_partition_transfer_distance_histogram": {
            str(key): value for key, value in sorted(distance_histogram.items())
        },
        "minimum_transfer_distance_to_efx_partition": min(distance_histogram),
        "complete_efx_allocation_count": literal_count,
        "cegar": {
            "session1": str(session1_path),
            "session1_sha256": sha256(session1_path),
            "session1_proto_sha256": session1["proto_sha256"],
            "session1_supported_singleton_sequence": sequence1,
            "session2": str(session2_path),
            "session2_sha256": sha256(session2_path),
            "session2_proto_sha256": session2["proto_sha256"],
            "session2_supported_singleton_sequence": sequence2,
            "terminal_singleton_pool_size": len(pool),
        },
        "claim": (
            "The 21-state contested-partner exchange implication is false, "
            "even when every blocked state has a zero-neighbor Hall witness."
        ),
        "claim_boundary": (
            "This profile is not an EFX counterexample. Its nine nearest "
            "repairs form the partner-B/triple-ABB bridge orbit, so the "
            "30-state union remains open after the recorded cap-6 UNKNOWN "
            "boundary."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session1", type=Path, required=True)
    parser.add_argument("--session2", type=Path, required=True)
    parser.add_argument("--bridge-boundary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.session1, args.session2, args.bridge_boundary, args.output)


if __name__ == "__main__":
    main()
