#!/usr/bin/env python3
"""Audit the sorting-free pair-degree encoding of the threshold envelope."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "owner-threshold-pair-degree-encoding-audit-v1"


def sorted_formula(values, favorite):
    x = sorted(values, reverse=True)
    return (
        x[4] + x[5] + x[6] > favorite
        and (x[2] + x[6] > favorite or x[3] + x[4] > favorite)
    )


def cardinal_formula(values, favorite):
    four_set_condition = all(
        any(
            sum(values[index] for index in four_set if index != removed) > favorite
            for removed in four_set
        )
        for four_set in itertools.combinations(range(8), 4)
    )
    degrees = tuple(
        sum(
            values[good] + values[other] > favorite
            for other in range(8)
            if other != good
        )
        for good in range(8)
    )
    return four_set_condition and (
        sum(degree >= 6 for degree in degrees) >= 3
        or sum(degree >= 4 for degree in degrees) >= 4
    )


def audit():
    profiles = tuple(itertools.combinations_with_replacement(range(5), 8))
    checks = 0
    true_profiles = 0
    for values in profiles:
        for favorite in range(max(values), 9):
            expected = sorted_formula(values, favorite)
            observed = cardinal_formula(values, favorite)
            if expected != observed:
                raise AssertionError((values, favorite, expected, observed))
            checks += 1
            true_profiles += int(expected)
    return {
        "schema": SCHEMA,
        "status": "OWNER_THRESHOLD_PAIR_DEGREE_ENCODING_AUDIT_PASSED",
        "residual_value_grid": [0, 1, 2, 3, 4],
        "nondecreasing_multiset_profiles": len(profiles),
        "favorite_range": "max(residual),...,8",
        "equivalence_checks": checks,
        "universal_threshold_failure_checks": true_profiles,
        "sorting_free_formula": {
            "four_set_condition": (
                "every four residual goods contain a triple worth more than F"
            ),
            "pair_degree_disjunction": (
                "at least three vertices have degree >=6 or at least four "
                "vertices have degree >=4 in the graph xy>F"
            ),
        },
        "scope_warning": (
            "The audit is a finite regression check; the order-statistic "
            "equivalence has a separate analytic proof."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
