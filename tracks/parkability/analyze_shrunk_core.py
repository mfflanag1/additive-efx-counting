#!/usr/bin/env python3
"""Audit the exact combinatorial structure of a deletion-shrinking checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .run_lra_cegar import atomic_json
    from .run_partition_core import partition_shape
    from .shrink_partition_core import (
        canonical_partition,
        global_partition_indices,
    )
except ImportError:
    import core
    from run_lra_cegar import atomic_json
    from run_partition_core import partition_shape
    from shrink_partition_core import (
        canonical_partition,
        global_partition_indices,
    )


SCHEMA = "partition-core-structure-audit-v1"
CHECKPOINT_SCHEMA = "partition-lra-deletion-shrink-v1"
N = 4
M = 8
FAVORITE_GOODS = frozenset({0, 1, 2})
NONFAVORITE_GOODS = frozenset(range(3, M))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_of(
    partition: tuple[tuple[int, ...], ...],
    good: int,
) -> tuple[int, ...]:
    matches = [bundle for bundle in partition if good in bundle]
    if len(matches) != 1:
        raise ValueError("partition does not contain a good exactly once")
    return matches[0]


def favorite_goods_separate(
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    return len({bundle_of(partition, good) for good in FAVORITE_GOODS}) == 3


def no_nonfavorite_singleton(
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    return all(
        len(bundle) != 1 or bundle[0] not in NONFAVORITE_GOODS
        for bundle in partition
    )


def singleton_zero_anchor(
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    return (
        bundle_of(partition, 0) == (0,)
        and favorite_goods_separate(partition)
        and no_nonfavorite_singleton(partition)
    )


def anchored_pair_boundary(
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    return (
        favorite_goods_separate(partition)
        and partition_shape(partition) == "2222"
        and len(bundle_of(partition, 0)) == 2
    )


def run(checkpoint_path: Path, output_path: Path) -> dict:
    checkpoint_bytes = checkpoint_path.read_bytes()
    checkpoint = json.loads(checkpoint_bytes)
    if (
        checkpoint.get("schema") != CHECKPOINT_SCHEMA
        or checkpoint.get("status")
        not in {"ACTIVE_UNSAT_CORE", "SHRUNK_CORE_UNSAT"}
        or checkpoint.get("n") != N
        or checkpoint.get("m") != M
        or checkpoint.get("favorite_pattern") != [0, 0, 1, 2]
    ):
        raise ValueError("not a verified favorite-211 shrinking checkpoint")

    source_path = Path(checkpoint["input"])
    if sha256(source_path) != checkpoint.get("input_sha256"):
        raise ValueError("checkpoint source hash mismatch")
    source = json.loads(source_path.read_text())
    partitions = [
        canonical_partition(partition)
        for partition in source["core_partitions"]
    ]
    active_positions = checkpoint["active_source_positions"]
    source_global_indices = global_partition_indices(partitions)
    if (
        active_positions != sorted(set(active_positions))
        or any(not 0 <= position < len(partitions) for position in active_positions)
        or len(active_positions) != checkpoint.get("active_partition_count")
        or checkpoint.get("active_global_partition_indices")
        != [source_global_indices[position] for position in active_positions]
    ):
        raise ValueError("invalid active source positions")

    active = {partitions[position] for position in active_positions}
    if len(active) != len(active_positions):
        raise ValueError("active partitions are not unique")
    universe = {
        canonical_partition([list(bundle) for bundle in partition])
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
    }
    if len(universe) != 1_701 or not active <= universe:
        raise ValueError("invalid partition universe or active subset")

    singleton_family = {partition for partition in universe if singleton_zero_anchor(partition)}
    pair_boundary_universe = {
        partition for partition in universe if anchored_pair_boundary(partition)
    }
    active_singletons = {
        partition for partition in active if singleton_zero_anchor(partition)
    }
    active_pair_boundary = {
        partition for partition in active if anchored_pair_boundary(partition)
    }
    active_other = active - active_singletons - active_pair_boundary
    source_shapes = Counter(map(partition_shape, partitions))
    active_shapes = Counter(map(partition_shape, active))
    removed_shapes = source_shapes - active_shapes
    all_favorites_separate = all(map(favorite_goods_separate, active))
    active_global_indices = set(
        checkpoint["active_global_partition_indices"]
    )
    sat_single_deletions = {
        check["requested_removed_global_indices"][0]
        for check in checkpoint.get("checks", [])
        if (
            check.get("phase") == "delete-1"
            and check.get("status") == "sat"
            and check.get("requested_removed_count") == 1
            and len(check.get("requested_removed_global_indices", [])) == 1
        )
    }
    deletion_covered = active_global_indices & sat_single_deletions
    deletion_missing = active_global_indices - sat_single_deletions

    payload = {
        "schema": SCHEMA,
        "meaning": (
            "exact descriptive and partition-deletion-minimality audit of "
            "a verified UNSAT core; not a minimum-cardinality certificate"
        ),
        "checkpoint": str(checkpoint_path.resolve()),
        "checkpoint_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
        "checkpoint_status": checkpoint["status"],
        "checkpoint_check_count": checkpoint["check_count"],
        "source": str(source_path.resolve()),
        "source_sha256": checkpoint["input_sha256"],
        "n": N,
        "m": M,
        "favorite_pattern": checkpoint["favorite_pattern"],
        "partition_universe_count": len(universe),
        "source_partition_count": len(partitions),
        "active_partition_count": len(active),
        "source_count_by_shape": dict(sorted(source_shapes.items())),
        "active_count_by_shape": dict(sorted(active_shapes.items())),
        "removed_count_by_shape": dict(sorted(removed_shapes.items())),
        "all_active_favorite_goods_separate": all_favorites_separate,
        "singleton_zero_anchor": {
            "universe_family_count": len(singleton_family),
            "active_family_count": len(active_singletons),
            "all_universe_family_present": active_singletons == singleton_family,
        },
        "anchored_pair_boundary": {
            "universe_family_count": len(pair_boundary_universe),
            "active_family_count": len(active_pair_boundary),
            "active_is_subset_of_universe_family": (
                active_pair_boundary <= pair_boundary_universe
            ),
        },
        "active_outside_two_piece_description_count": len(active_other),
        "two_piece_description_exact": (
            active == active_singletons | active_pair_boundary
        ),
        "partition_deletion_minimality": {
            "meaning": (
                "a SAT deletion test on an earlier active superset remains "
                "SAT after later constraint deletion"
            ),
            "active_survivor_count": len(active_global_indices),
            "sat_single_deletion_covered_count": len(deletion_covered),
            "missing_global_partition_indices": sorted(deletion_missing),
            "all_survivors_individually_indispensable": not deletion_missing,
        },
    }
    atomic_json(output_path, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.checkpoint, args.output)


if __name__ == "__main__":
    main()
