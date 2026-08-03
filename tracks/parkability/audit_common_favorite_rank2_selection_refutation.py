#!/usr/bin/env python3
"""Independently audit the cap-4 refutation of rank-two selection."""

from __future__ import annotations

import argparse
import hashlib
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
        SHAPES,
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
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
        transfer_distance,
    )


SCHEMA = "common-favorite-rank2-selection-refutation-audit-v1"
FOURTYPE_SCHEMA = "common-favorite-fourtype-rank2-refutation-audit-v1"
EXPECTED_VALUES = (
    (4, 3, 1, 1, 2, 2, 2, 3, 3),
    (4, 3, 1, 1, 3, 3, 3, 2, 2),
    (4, 3, 1, 1, 3, 3, 3, 2, 2),
    (4, 3, 1, 1, 3, 3, 3, 2, 2),
)
FOURTYPE_EXPECTED_VALUES = (
    (4, 2, 2, 2, 3, 1, 1, 3, 3),
    (4, 3, 1, 1, 2, 3, 3, 3, 2),
    (4, 1, 2, 2, 2, 3, 3, 3, 2),
    (4, 1, 2, 2, 2, 3, 3, 2, 3),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resident_graph(values, owner, partition):
    full_graph = feasible_graph(values, ((FAVORITE,),) + partition)
    return tuple(
        tuple(full_graph[agent][bundle] for bundle in range(1, N))
        for agent in range(N)
        if agent != owner
    )


def bundle_order_signature(row):
    groups = {}
    for mask in range(1 << len(row)):
        total = sum(
            row[good] for good in range(len(row)) if mask & (1 << good)
        )
        groups.setdefault(total, []).append(mask)
    return tuple(tuple(groups[total]) for total in sorted(groups))


def run(source_path, output_path, profile="unconditional"):
    if output_path.exists():
        raise ValueError("output path already exists")
    if profile not in {"unconditional", "fourtype"}:
        raise ValueError("unknown rank-two refutation profile")
    fourtype = profile == "fourtype"
    expected_values = FOURTYPE_EXPECTED_VALUES if fourtype else EXPECTED_VALUES
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != "common-favorite-mixed-selection-cegar-v1"
        or source.get("status")
        not in {"ZERO_NEIGHBOR_SELECTION_COUNTEREXAMPLE", "SELECTION_COUNTEREXAMPLE"}
        or source.get("selection_motif") != "rank_two"
        or source.get("upper") != 4
        or source.get("selected_residual_shape") != "332"
        or source.get("require_pairwise_nonproportional_rows", False)
        != fourtype
        or source.get("values") is None
    ):
        raise ValueError("rank-two refutation source metadata changed")
    proto_path = Path(source["proto"])
    if not proto_path.is_file() or sha256(proto_path) != source["proto_sha256"]:
        raise AssertionError("rank-two refutation proto changed")
    values = core.validate_values(
        source["values"],
        expected_n=N,
        expected_m=M,
        lower=1,
        upper=4,
    )
    if values != expected_values:
        raise AssertionError("rank-two refutation matrix changed")
    if any(row[FAVORITE] <= max(row[1:]) for row in values):
        raise AssertionError("rank-two refutation lost its strict common favorite")
    if not threshold_passes(values, 0, SHAPES["332"]):
        raise AssertionError("selected threshold premise failed")

    residual = tuple(residual_partitions())
    passes = []
    singleton_support = 0
    for partition_index, partition in enumerate(residual):
        full = ((FAVORITE,),) + partition
        singleton_support += matching_rank(feasible_graph(values, full)) == N
        for owner in range(N):
            if not threshold_passes(values, owner, partition):
                continue
            graph = resident_graph(values, owner, partition)
            passes.append({
                "owner": owner,
                "partition_index": partition_index,
                "partition": [list(bundle) for bundle in partition],
                "shape": "".join(
                    map(str, sorted(map(len, partition), reverse=True))
                ),
                "resident_graph": [list(row) for row in graph],
                "resident_matching_rank": matching_rank(graph),
            })
    if (
        len(residual) != 966
        or singleton_support != 0
        or len(passes) != 3
        or any(item["owner"] != 0 for item in passes)
        or any(item["shape"] != "332" for item in passes)
        or any(item["resident_matching_rank"] != 1 for item in passes)
    ):
        raise AssertionError("rank-two selection refutation census changed")

    selected_full = ((FAVORITE,),) + SHAPES["332"]
    radius_two = set(balanced_transfer_neighborhood(SHAPES["332"], 2))
    support = []
    partition_count = 0
    for partition in core.iter_unlabeled_nonempty_partitions(N, M):
        partition_count += 1
        if matching_rank(feasible_graph(values, partition)) == N:
            support.append(partition)
    if partition_count != 7770:
        raise AssertionError("complete partition universe changed")
    shape_count = Counter(
        "".join(map(str, sorted(map(len, partition), reverse=True)))
        for partition in support
    )
    distance_count = Counter(
        transfer_distance(selected_full, partition) for partition in support
    )
    allocation_count = core.count_efx0_allocations(values)
    independent_count = independent.count_complete_efx0(values)
    nearest = next(
        partition
        for partition in support
        if transfer_distance(selected_full, partition) == 1
    )
    nearest_graph = feasible_graph(values, nearest)
    nearest_assignment = tuple(
        owner
        for good in range(M)
        for owner, bundle in enumerate(nearest)
        if good in bundle
    )
    expected_support_count = 599 if fourtype else 195
    expected_distance_count = (
        {1: 3, 2: 16, 3: 112, 4: 286, 5: 182}
        if fourtype
        else {1: 3, 2: 15, 3: 57, 4: 90, 5: 30}
    )
    expected_radius_two_count = 19 if fourtype else 18
    expected_allocation_count = 3878 if fourtype else 3690
    expected_nearest_graph = (
        (
            (True, True, False, True),
            (True, True, True, True),
            (True, True, True, True),
            (True, True, True, True),
        )
        if fourtype
        else ((True,) * N,) * N
    )
    proportional_pairs = [
        [left, right]
        for left in range(N)
        for right in range(left + 1, N)
        if all(
            values[left][good] * values[right][FAVORITE]
            == values[right][good] * values[left][FAVORITE]
            for good in range(1, M)
        )
    ]
    bundle_order_signatures = [bundle_order_signature(row) for row in values]
    bundle_order_equivalent_pairs = [
        [left, right]
        for left in range(N)
        for right in range(left + 1, N)
        if bundle_order_signatures[left] == bundle_order_signatures[right]
    ]
    if (
        len(support) != expected_support_count
        or shape_count != {"3222": expected_support_count}
        or distance_count != expected_distance_count
        or sum(partition in radius_two for partition in support)
        != expected_radius_two_count
        or allocation_count != expected_allocation_count
        or independent_count != allocation_count
        or nearest != ((0, 4), (1, 2, 3), (5, 6), (7, 8))
        or nearest_graph != expected_nearest_graph
        or (fourtype and proportional_pairs)
        or (fourtype and bundle_order_equivalent_pairs)
        or not independent.is_complete_efx0(values, nearest_assignment)
    ):
        raise AssertionError("complete EFX replay changed")

    result = {
        "schema": FOURTYPE_SCHEMA if fourtype else SCHEMA,
        "status": (
            "FOUR_TYPE_RANK_TWO_SELECTION_LEMMA_REFUTED"
            if fourtype
            else "RANK_TWO_SELECTION_LEMMA_REFUTED"
        ),
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "proto": str(proto_path),
        "proto_sha256": source["proto_sha256"],
        "n": N,
        "m": M,
        "upper": 4,
        "values": [list(row) for row in values],
        "distinct_valuation_row_count": len(set(values)),
        "strict_common_favorite": FAVORITE,
        "selected_threshold_pass": True,
        "favorite_singleton_partition_count": len(residual),
        "favorite_singleton_supporting_partition_count": singleton_support,
        "threshold_pass_count": len(passes),
        "maximum_resident_matching_rank_over_threshold_passes": max(
            item["resident_matching_rank"] for item in passes
        ),
        "threshold_passes": passes,
        "complete_partition_count": partition_count,
        "complete_efx_supporting_partition_count": len(support),
        "complete_efx_supporting_partition_count_by_shape": dict(
            sorted(shape_count.items())
        ),
        "supporting_partition_transfer_distance_histogram": {
            str(distance): count
            for distance, count in sorted(distance_count.items())
        },
        "radius_two_supporting_partition_count": sum(
            partition in radius_two for partition in support
        ),
        "representative_one_transfer_repair": {
            "partition": [list(bundle) for bundle in nearest],
            "feasibility_graph": [list(row) for row in nearest_graph],
            "assignment": list(nearest_assignment),
        },
        "complete_efx_allocation_count": allocation_count,
        "independent_complete_efx_allocation_count": independent_count,
        "claim": (
            "Even with four pairwise bundle-order-inequivalent additive "
            "valuation rows, a mixed common-favorite profile need not have "
            "any threshold-passing owner/partition whose resident graph has "
            "matching rank two."
            if fourtype
            else "A mixed common-favorite profile need not have any "
            "threshold-passing owner/partition whose resident graph has "
            "matching rank two."
        ),
        "claim_boundary": (
            "This refutes the repaired four-preference-type rank-two "
            "selector. It is not an EFX counterexample: the profile has "
            "3,878 complete EFX allocations, all on balanced 3+2+2+2 "
            "partitions."
            if fourtype
            else "This refutes the rank-two selection lemma and its stronger "
            "zero-neighbor version. It is not an EFX counterexample: the "
            "profile has 3,690 complete EFX allocations, all on balanced "
            "3+2+2+2 partitions."
        ),
    }
    if fourtype:
        result["pairwise_proportional_valuation_row_pairs"] = proportional_pairs
        result["pairwise_bundle_order_equivalent_row_pairs"] = (
            bundle_order_equivalent_pairs
        )
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--profile",
        choices=("unconditional", "fourtype"),
        default="unconditional",
    )
    args = parser.parse_args()
    run(args.source, args.output, args.profile)


if __name__ == "__main__":
    main()
