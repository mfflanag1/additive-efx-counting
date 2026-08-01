#!/usr/bin/env python3
"""Audit strict generic boundaries to two distinct-half proof shortcuts."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_favorite_singleton_hall_boundaries import residual_partitions
    from .audit_matching_augmentation import feasible_graph, matching_rank
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_favorite_singleton_hall_boundaries import residual_partitions
    from audit_matching_augmentation import feasible_graph, matching_rank


SCHEMA = "distinct-half-normal-form-boundaries-audit-v1"
N = 4
M = 9
FAVORITE = 0
REPRESENTATIVES = (1, 2, 3, 4)

PAIR_COVER_PROFILE = (
    (216, 115, 114, 113, 112, 111, 96, 95, 94),
    (216, 111, 115, 114, 113, 112, 94, 96, 95),
    (216, 112, 111, 115, 114, 113, 95, 94, 96),
    (216, 113, 112, 111, 115, 114, 96, 94, 95),
)

FAVORITE_DOMINATED_PROFILE = (
    (89, 53, 75, 74, 73, 72, 71, 70, 69),
    (43, 16, 38, 37, 36, 35, 34, 33, 32),
    (43, 16, 32, 38, 37, 36, 35, 34, 33),
    (43, 16, 33, 32, 38, 37, 36, 35, 34),
)


def balanced_universe():
    result = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    )
    if len(result) != 1260:
        raise AssertionError("balanced universe changed")
    return result


def pair_state_universe():
    result = []
    for partition in core.iter_unlabeled_nonempty_partitions(5, M):
        if tuple(sorted(map(len, partition), reverse=True)) == (2, 2, 2, 2, 1):
            result.append(tuple(bundle for bundle in partition if len(bundle) == 2))
    if len(result) != 945:
        raise AssertionError("pair-state universe changed")
    return tuple(result)


def has_matching(graph: tuple[tuple[bool, ...], ...]) -> bool:
    return any(
        all(graph[observer][matching[observer]] for observer in range(N))
        for matching in itertools.permutations(range(N))
    )


def pair_state_supported(values, state) -> bool:
    return has_matching(
        tuple(
            tuple(
                sum(row[good] for good in pair) >= row[FAVORITE]
                for pair in state
            )
            for row in values
        )
    )


def favorite_dominated(values, partition) -> bool:
    if any(
        sum(row[good] for good in bundle if good != removed) > row[FAVORITE]
        for row in values
        for bundle in partition
        for removed in bundle
    ):
        return False
    return has_matching(
        tuple(
            tuple(
                sum(row[good] for good in bundle) >= row[FAVORITE]
                for bundle in partition
            )
            for row in values
        )
    )


def audit_branch(values) -> dict:
    if len(set(values)) != N or any(len(set(row)) != M for row in values):
        raise AssertionError("profile is not strict and row-distinct")
    row_conditions = []
    for observer, row in enumerate(values):
        favorite = row[FAVORITE]
        representative = REPRESENTATIVES[observer]
        if any(favorite <= row[good] for good in range(1, M)):
            raise AssertionError("favorite is not strict")
        if 2 * row[representative] <= favorite:
            raise AssertionError("fixed representative is not a half-favorite")
        residual = sorted(row[1:], reverse=True)
        envelope = (
            residual[4] + residual[5] + residual[6] > favorite
            and (
                residual[2] + residual[6] > favorite
                or residual[3] + residual[4] > favorite
            )
        )
        literal = all(
            max(
                sum(row[good] for good in bundle)
                - min(row[good] for good in bundle)
                for bundle in partition
            )
            > favorite
            for partition in residual_partitions()
        )
        if not envelope or not literal:
            raise AssertionError("profile lost universal threshold failure")
        row_conditions.append({
            "observer": observer,
            "favorite": favorite,
            "representative": representative,
            "sorted_residual": residual,
            "envelope_holds": envelope,
            "literal_966_partition_failure": literal,
        })
    return {
        "strict_common_favorite": True,
        "pairwise_distinct_rows": True,
        "distinct_item_values_per_row": True,
        "distinct_half_favorite_representatives": list(REPRESENTATIVES),
        "rows": row_conditions,
    }


def supported_balanced(values, universe):
    return tuple(
        partition
        for partition in universe
        if matching_rank(feasible_graph(values, partition)) == N
    )


def profile_record(name, values, balanced, pairs) -> dict:
    branch = audit_branch(values)
    supported = supported_balanced(values, balanced)
    if not supported:
        raise AssertionError("boundary profile lost all balanced EFX")
    favorite_bundle_sizes = {
        len(next(bundle for bundle in partition if FAVORITE in bundle))
        for partition in supported
    }
    if favorite_bundle_sizes != {2}:
        raise AssertionError("favorite-pair census changed")
    if name == "pair_cover":
        target_count = sum(
            pair_state_supported(values, state)
            for state in pairs
        )
    else:
        target_count = sum(
            favorite_dominated(values, partition)
            for partition in balanced
        )
    if target_count:
        raise AssertionError("refuted normal form gained a witness")
    return {
        "values": [list(row) for row in values],
        "branch_audit": branch,
        "refuted_target_count": target_count,
        "balanced_efx_partition_count": len(supported),
        "literal_complete_efx_allocation_count": (
            independent.count_complete_efx0(values)
        ),
        "favorite_bundle_sizes_in_balanced_efx": sorted(favorite_bundle_sizes),
        "example_balanced_efx_partition": [
            list(bundle) for bundle in supported[0]
        ],
    }


def audit() -> dict:
    balanced = balanced_universe()
    pairs = pair_state_universe()
    pair_record = profile_record(
        "pair_cover",
        PAIR_COVER_PROFILE,
        balanced,
        pairs,
    )
    dominated_record = profile_record(
        "favorite_dominated",
        FAVORITE_DOMINATED_PROFILE,
        balanced,
        pairs,
    )
    if (
        pair_record["balanced_efx_partition_count"] != 60
        or pair_record["literal_complete_efx_allocation_count"] != 1440
        or dominated_record["balanced_efx_partition_count"] != 240
        or dominated_record["literal_complete_efx_allocation_count"] != 2537
    ):
        raise AssertionError("boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_NORMAL_FORM_BOUNDARIES_AUDIT_PASSED",
        "scope": {
            "balanced_partition_count": len(balanced),
            "four_pair_state_count": len(pairs),
            "residual_partitions_per_owner": len(residual_partitions()),
        },
        "four_favorite_dominating_pairs_boundary": pair_record,
        "globally_favorite_dominated_balanced_boundary": dominated_record,
        "interpretation": (
            "Both profiles are strict, row-distinct, universally "
            "owner-threshold-obstructed, and have four distinct "
            "half-favorite representatives. The first has no four-pair "
            "favorite-floor cover; the second has no balanced partition "
            "whose deletion remainders are globally favorite-bounded. "
            "Both nevertheless have many complete balanced EFX allocations."
        ),
        "limitations": [
            "These are counterexamples only to two sufficient normal forms, not to EFX.",
            "The favorite-pair balanced EFX target survives both profiles.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
