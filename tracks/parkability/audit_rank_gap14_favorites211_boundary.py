#!/usr/bin/env python3
"""Audit the cap-14 favorite-211 balanced failure and singleton repairs."""

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
    from .run_integer_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from run_integer_partition_cegar import supported_partitions


SCHEMA = "rank-gap14-favorites211-boundary-audit-v1"
SOURCE = "efx49_rankgap14_shape3222_favorites211_matching_session2.json"
VALUES = (
    (14, 7, 8, 6, 5, 4, 3, 2, 1),
    (14, 7, 8, 6, 5, 4, 1, 3, 2),
    (7, 14, 12, 13, 6, 1, 3, 2, 4),
    (12, 13, 14, 9, 2, 6, 3, 4, 1),
)
FAVORITE_PATTERN = (0, 0, 1, 2)
LABELED_SHAPES = {
    (3, 3, 2, 1): 183,
    (4, 2, 2, 1): 115,
}
UNLABELED_SHAPES = {
    (3, 3, 2, 1): 55,
    (4, 2, 2, 1): 30,
}
SINGLETON_GOODS = {0: 74, 1: 5, 2: 6}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape_key(shape: tuple[int, ...]) -> str:
    return "+".join(map(str, shape))


def audit(results_dir: Path) -> dict:
    source_path = results_dir / SOURCE
    source = json.loads(source_path.read_text())
    expected_fields = {
        "schema": "integer-partition-cp-sat-result-v1",
        "status": "ZERO_SUPPORTED_PARTITIONS",
        "n": 4,
        "m": 9,
        "upper": 14,
        "partition_shape": [3, 2, 2, 2],
        "partition_singleton_goods": [],
        "require_distinct_item_values": True,
        "favorite_pattern": list(FAVORITE_PATTERN),
        "favorite_pattern_stabilizer": True,
        "obstruction_encoding": "matching_clauses",
        "solver_status": "OPTIMAL",
    }
    mismatches = {
        key: {"expected": expected, "actual": source.get(key)}
        for key, expected in expected_fields.items()
        if source.get(key) != expected
    }
    if mismatches:
        raise AssertionError((source_path, mismatches))
    values = tuple(tuple(row) for row in source.get("values") or ())
    if values != VALUES:
        raise AssertionError("the frozen cap-14 boundary matrix changed")

    universe = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    balanced = [
        partition
        for partition in universe
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    ]
    if supported_partitions(values, balanced):
        raise AssertionError("the boundary unexpectedly supports a balanced partition")

    supported = supported_partitions(values, universe)
    unlabeled_shapes = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in supported
    )
    singleton_goods = Counter(
        bundle[0]
        for partition in supported
        for bundle in partition
        if len(bundle) == 1
    )
    designated = set(FAVORITE_PATTERN)
    if (
        dict(unlabeled_shapes) != UNLABELED_SHAPES
        or dict(singleton_goods) != SINGLETON_GOODS
        or any(
            not any((good,) in partition for good in designated)
            for partition in supported
        )
    ):
        raise AssertionError("the favorite-singleton repair census changed")

    labeled_shapes: Counter[tuple[int, ...]] = Counter()
    for assignment in itertools.product(range(4), repeat=9):
        if independent.is_complete_efx0(values, assignment):
            labeled_shapes[
                tuple(sorted(Counter(assignment).values(), reverse=True))
            ] += 1
    if dict(labeled_shapes) != LABELED_SHAPES:
        raise AssertionError(("labeled census", labeled_shapes))

    return {
        "schema": SCHEMA,
        "status": "BOUNDARY_AUDIT_PASSED",
        "claim": (
            "The frozen cap-14 favorite-211 profile has no balanced EFX "
            "allocation, but all of its complete-EFX repairs isolate one "
            "of the three designated favorite goods."
        ),
        "source_path": str(source_path.resolve()),
        "source_sha256": sha256(source_path),
        "favorite_pattern": list(FAVORITE_PATTERN),
        "values": [list(row) for row in values],
        "all_nonempty_partitions": len(universe),
        "balanced_partitions": len(balanced),
        "unlabeled_supported_partition_count": len(supported),
        "unlabeled_shape_counts": {
            shape_key(shape): count
            for shape, count in sorted(unlabeled_shapes.items())
        },
        "singleton_good_counts": {
            str(good): count
            for good, count in sorted(singleton_goods.items())
        },
        "labeled_complete_efx_count": sum(labeled_shapes.values()),
        "labeled_shape_counts": {
            shape_key(shape): count
            for shape, count in sorted(labeled_shapes.items())
        },
        "all_repairs_isolate_a_designated_favorite": True,
        "interpretation": (
            "This refutes the balanced-only cap-14 ladder in the 2+1+1 "
            "favorite orbit, while preserving the broader balanced-or-"
            "designated-favorite-singleton target."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.results_dir)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
