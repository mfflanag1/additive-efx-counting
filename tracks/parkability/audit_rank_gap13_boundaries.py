#!/usr/bin/env python3
"""Audit the cap-13 balanced-shape failures and favorite-singleton repairs."""

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


SCHEMA = "rank-gap13-efx-4x9-boundary-audit-v1"
CASES = {
    "31": {
        "source": (
            "efx49_rankgap13_shape3222_favorites31_"
            "matching_stabilized_session2.json"
        ),
        "favorite_pattern": [0, 0, 0, 1],
        "values": (
            (13, 9, 7, 6, 5, 4, 3, 2, 1),
            (13, 8, 7, 6, 4, 3, 1, 2, 5),
            (13, 8, 7, 6, 2, 4, 1, 3, 5),
            (8, 13, 7, 6, 5, 1, 2, 4, 3),
        ),
        "labeled_shapes": {
            (3, 3, 2, 1): 335,
            (4, 2, 2, 1): 110,
            (4, 3, 1, 1): 22,
        },
        "unlabeled_shapes": {
            (3, 3, 2, 1): 78,
            (4, 2, 2, 1): 21,
            (4, 3, 1, 1): 7,
        },
        "singleton_goods": {0: 82, 1: 31},
        "double_singleton_count": 7,
    },
    "22": {
        "source": (
            "efx49_rankgap13_shape3222_favorites22_"
            "matching_stabilized_session2.json"
        ),
        "favorite_pattern": [0, 0, 1, 1],
        "values": (
            (13, 8, 7, 6, 5, 4, 3, 2, 1),
            (13, 8, 6, 7, 5, 2, 1, 3, 4),
            (8, 13, 7, 6, 2, 1, 3, 4, 5),
            (8, 13, 6, 7, 5, 1, 3, 2, 4),
        ),
        "labeled_shapes": {
            (3, 3, 2, 1): 242,
            (4, 2, 2, 1): 80,
            (4, 3, 1, 1): 28,
        },
        "unlabeled_shapes": {
            (3, 3, 2, 1): 75,
            (4, 2, 2, 1): 18,
            (4, 3, 1, 1): 8,
        },
        "singleton_goods": {0: 55, 1: 54},
        "double_singleton_count": 8,
    },
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape_key(shape: tuple[int, ...]) -> str:
    return "+".join(map(str, shape))


def audit(results_dir: Path) -> dict:
    universe = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    shape_universe = [
        partition
        for partition in universe
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    ]
    audited_cases = []
    for name, expected in CASES.items():
        source_path = results_dir / expected["source"]
        source = json.loads(source_path.read_text())
        values = tuple(tuple(row) for row in source.get("values") or ())
        expected_source_fields = {
            "schema": "integer-partition-cp-sat-result-v1",
            "status": "ZERO_SUPPORTED_PARTITIONS",
            "n": 4,
            "m": 9,
            "upper": 13,
            "partition_shape": [3, 2, 2, 2],
            "require_distinct_item_values": True,
            "favorite_pattern": expected["favorite_pattern"],
            "favorite_pattern_stabilizer": True,
            "obstruction_encoding": "matching_clauses",
            "solver_status": "OPTIMAL",
        }
        mismatches = {
            key: {"expected": expected_value, "actual": source.get(key)}
            for key, expected_value in expected_source_fields.items()
            if source.get(key) != expected_value
        }
        if mismatches:
            raise AssertionError((source_path, mismatches))
        if values != expected["values"]:
            raise AssertionError(f"the frozen {name} boundary matrix changed")

        labeled_shapes: Counter[tuple[int, ...]] = Counter()
        for assignment in itertools.product(range(4), repeat=9):
            if independent.is_complete_efx0(values, assignment):
                labeled_shapes[
                    tuple(sorted(Counter(assignment).values(), reverse=True))
                ] += 1
        if dict(labeled_shapes) != expected["labeled_shapes"]:
            raise AssertionError((name, "labeled census", labeled_shapes))

        if supported_partitions(values, shape_universe):
            raise AssertionError(f"{name} unexpectedly supports a balanced partition")
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
        designated = set(expected["favorite_pattern"])
        double_singletons = sum(
            sum((good,) in partition for good in designated) == 2
            for partition in supported
        )
        if (
            dict(unlabeled_shapes) != expected["unlabeled_shapes"]
            or dict(singleton_goods) != expected["singleton_goods"]
            or double_singletons != expected["double_singleton_count"]
            or any(
                not any((good,) in partition for good in designated)
                for partition in supported
            )
        ):
            raise AssertionError((name, "unlabeled repair census changed"))

        audited_cases.append({
            "favorite_multiplicity": name,
            "favorite_pattern": expected["favorite_pattern"],
            "source_path": str(source_path.resolve()),
            "source_sha256": file_sha256(source_path),
            "values": [list(row) for row in values],
            "labeled_complete_efx_count": sum(labeled_shapes.values()),
            "labeled_shape_counts": {
                shape_key(shape): count
                for shape, count in sorted(labeled_shapes.items())
            },
            "unlabeled_supported_partition_count": len(supported),
            "unlabeled_shape_counts": {
                shape_key(shape): count
                for shape, count in sorted(unlabeled_shapes.items())
            },
            "singleton_good_counts": {
                str(good): count
                for good, count in sorted(singleton_goods.items())
            },
            "partitions_with_two_designated_singletons": double_singletons,
            "all_repairs_isolate_a_designated_favorite": True,
        })
    return {
        "schema": SCHEMA,
        "status": "BOUNDARY_AUDIT_PASSED",
        "claim": (
            "The frozen cap-13 3+1 and 2+2 favorite profiles have no "
            "(3,2,2,2) EFX allocation, while every complete-EFX repair "
            "isolates a designated favorite good."
        ),
        "all_nonempty_partitions": len(universe),
        "balanced_partitions": len(shape_universe),
        "cases": audited_cases,
        "interpretation": (
            "The cap-12 balanced-or-common-singleton mechanism generalizes "
            "at cap 13 to balanced-or-designated-favorite-singleton."
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
