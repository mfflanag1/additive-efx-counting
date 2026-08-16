#!/usr/bin/env python3
"""Audit the first failure of the 4x9 Borda shape generalization."""

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


SCHEMA = "rank-gap-efx-4x9-boundary-audit-v1"
EXPECTED_VALUES = (
    (12, 8, 7, 6, 5, 4, 3, 2, 1),
    (12, 8, 7, 6, 5, 4, 1, 3, 2),
    (12, 8, 7, 5, 6, 4, 2, 3, 1),
    (12, 8, 7, 5, 6, 4, 1, 3, 2),
)
EXPECTED_SHAPE_COUNTS = {
    (3, 3, 2, 1): 636,
    (4, 2, 2, 1): 202,
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_path: Path) -> dict:
    source = json.loads(source_path.read_text())
    values = tuple(tuple(row) for row in source.get("values") or ())
    expected_source_fields = {
        "schema": "integer-partition-cp-sat-result-v1",
        "status": "ZERO_SUPPORTED_PARTITIONS",
        "n": 4,
        "m": 9,
        "upper": 12,
        "partition_shape": [3, 2, 2, 2],
        "require_distinct_item_values": True,
        "favorite_pattern": [0, 0, 0, 0],
        "favorite_pattern_stabilizer": True,
        "obstruction_encoding": "matching_clauses",
        "solver_status": "OPTIMAL",
    }
    mismatches = {
        key: {"expected": expected, "actual": source.get(key)}
        for key, expected in expected_source_fields.items()
        if source.get(key) != expected
    }
    if mismatches:
        raise AssertionError((source_path, mismatches))
    if values != EXPECTED_VALUES:
        raise AssertionError("the frozen boundary matrix changed")
    if any(
        len(set(row)) != 9
        or min(row) < 1
        or max(row) > 12
        or any(row[0] <= row[good] for good in range(1, 9))
        for row in values
    ):
        raise AssertionError("the boundary matrix is outside the claimed domain")

    shape_counts: Counter[tuple[int, ...]] = Counter()
    examples: dict[tuple[int, ...], tuple[int, ...]] = {}
    for assignment in itertools.product(range(4), repeat=9):
        if independent.is_complete_efx0(values, assignment):
            shape = tuple(sorted(Counter(assignment).values(), reverse=True))
            shape_counts[shape] += 1
            examples.setdefault(shape, assignment)
    if dict(shape_counts) != EXPECTED_SHAPE_COUNTS:
        raise AssertionError(("unexpected literal EFX census", shape_counts))

    universe = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    shape_universe = [
        partition
        for partition in universe
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    ]
    supported_shape = supported_partitions(values, shape_universe)
    supported_all = supported_partitions(values, universe)
    supported_shape_counts = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in supported_all
    )
    if supported_shape or len(supported_all) != 48:
        raise AssertionError("the partition census does not match the boundary claim")
    if supported_shape_counts != Counter({
        (3, 3, 2, 1): 37,
        (4, 2, 2, 1): 11,
    }):
        raise AssertionError(("unexpected unlabeled shape census", supported_shape_counts))
    if any((0,) not in partition for partition in supported_all):
        raise AssertionError("a supported partition does not isolate the common favorite")

    return {
        "schema": SCHEMA,
        "status": "BOUNDARY_AUDIT_PASSED",
        "claim": (
            "The frozen cap-12 common-favorite profile has complete EFX "
            "allocations, but none of bundle shape (3,2,2,2)."
        ),
        "source_path": str(source_path.resolve()),
        "source_sha256": file_sha256(source_path),
        "values": [list(row) for row in values],
        "domain": {
            "agents": 4,
            "goods": 9,
            "value_lower": 1,
            "value_upper": 12,
            "distinct_values_per_row": 9,
            "common_unique_favorite": 0,
        },
        "literal_labeled_allocation_census": {
            "complete_efx_count": sum(shape_counts.values()),
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(shape_counts.items())
            },
            "example_assignments": {
                "+".join(map(str, shape)): list(examples[shape])
                for shape in sorted(examples)
            },
        },
        "unlabeled_partition_census": {
            "all_nonempty_partitions": len(universe),
            "shape_3+2+2+2_partitions": len(shape_universe),
            "supported_partitions": len(supported_all),
            "partitions_isolating_common_favorite": len(supported_all),
            "supported_shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(supported_shape_counts.items())
            },
        },
        "interpretation": (
            "This refutes only the fixed (3,2,2,2)-shape extension, not "
            "complete EFX. Every EFX allocation in the literal census has "
            "a singleton bundle."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "results/"
            "efx49_rankgap12_shape3222_favorites4_"
            "matching_stabilized_session2.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
