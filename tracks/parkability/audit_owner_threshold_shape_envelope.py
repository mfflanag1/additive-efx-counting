#!/usr/bin/env python3
"""Audit exact owner-threshold optima for the 3+3+2 and 4+2+2 shapes."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
except ImportError:
    import core
    from anneal import atomic_json


SCHEMA = "owner-threshold-shape-envelope-audit-v1"


def shape(partition: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sorted(map(len, partition), reverse=True))


def threshold(
    values: tuple[int, ...],
    partition: tuple[tuple[int, ...], ...],
) -> int:
    return max(
        sum(values[good] for good in bundle)
        - min(values[good] for good in bundle)
        for bundle in partition
    )


def audit() -> dict:
    universe = tuple(core.iter_unlabeled_nonempty_partitions(3, 8))
    by_shape = {
        target: tuple(partition for partition in universe if shape(partition) == target)
        for target in ((3, 3, 2), (4, 2, 2))
    }
    if {target: len(partitions) for target, partitions in by_shape.items()} != {
        (3, 3, 2): 280,
        (4, 2, 2): 210,
    }:
        raise AssertionError("residual shape census changed")

    profiles = tuple(
        tuple(reversed(values))
        for values in itertools.combinations_with_replacement(range(5), 8)
    )
    universal = 0
    for values in profiles:
        optimum_332 = min(
            threshold(values, partition)
            for partition in by_shape[(3, 3, 2)]
        )
        formula_332 = max(
            values[0],
            values[2] + values[6],
            values[3] + values[4],
        )
        optimum_422 = min(
            threshold(values, partition)
            for partition in by_shape[(4, 2, 2)]
        )
        formula_422 = max(
            values[0],
            values[4] + values[5] + values[6],
        )
        if optimum_332 != formula_332 or optimum_422 != formula_422:
            raise AssertionError(
                (values, optimum_332, formula_332, optimum_422, formula_422)
            )
        for favorite in range(values[0], 9):
            literal_failure = all(
                threshold(values, partition) > favorite
                for partition in universe
            )
            formula_failure = (
                values[4] + values[5] + values[6] > favorite
                and (
                    values[2] + values[6] > favorite
                    or values[3] + values[4] > favorite
                )
            )
            if literal_failure != formula_failure:
                raise AssertionError(
                    (values, favorite, literal_failure, formula_failure)
                )
            universal += 1

    return {
        "schema": SCHEMA,
        "status": "OWNER_THRESHOLD_SHAPE_ENVELOPE_AUDIT_PASSED",
        "scope": {
            "residual_goods": 8,
            "residual_bundles": 3,
            "nonincreasing_value_grid": [0, 1, 2, 3, 4],
            "profile_count": len(profiles),
        },
        "shape_3+3+2": {
            "partition_count": len(by_shape[(3, 3, 2)]),
            "exact_minimum": "max(x1, x3+x7, x4+x5)",
            "attaining_partition": "{x1,x2}|{x3,x7,x8}|{x4,x5,x6}",
        },
        "shape_4+2+2": {
            "partition_count": len(by_shape[(4, 2, 2)]),
            "exact_minimum": "max(x1, x5+x6+x7)",
            "attaining_partition": "{x1,x2}|{x3,x4}|{x5,x6,x7,x8}",
        },
        "partition_profile_checks": len(profiles)
        * sum(map(len, by_shape.values())),
        "universal_threshold_checks": universal,
        "interpretation": (
            "If f is the owner's favorite, every residual partition fails "
            "if and only if x5+x6+x7>v(f) and either x3+x7>v(f) "
            "or x4+x5>v(f)."
        ),
        "limitations": [
            "The audit is a regression check; the accompanying proof is analytic.",
            "The shape reductions cover all 966 residual partitions.",
            "The result controls the singleton owner's threshold, not the resident Hall gate.",
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
