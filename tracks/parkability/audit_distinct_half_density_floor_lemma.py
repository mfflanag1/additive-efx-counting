#!/usr/bin/env python3
"""Exhaustively audit the combinatorial density-floor construction lemma."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "distinct-half-density-floor-lemma-audit-v1"
GOODS = tuple(range(8))
TRIPLES = tuple(
    sum(1 << good for good in goods)
    for goods in itertools.combinations(GOODS, 3)
)
NORMALIZED_FIRST = (1 << 0) | (1 << 1) | (1 << 2)


def pair_masks(triple, excluded):
    available = tuple(
        good
        for good in GOODS
        if triple & (1 << good) and good != excluded
    )
    return tuple(
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(available, 2)
    )


PAIR_MASKS = {
    (triple, excluded): pair_masks(triple, excluded)
    for triple in TRIPLES
    for excluded in GOODS
}


def pairable(left, right, excluded, must_cover=None):
    required = 0 if must_cover is None else 1 << must_cover
    return any(
        left_pair & right_pair == 0
        and (
            required == 0
            or (left_pair | right_pair) & required
        )
        for left_pair in PAIR_MASKS[left, excluded]
        for right_pair in PAIR_MASKS[right, excluded]
    )


def has_bad_ordered_low_pair(family, owner):
    outside = tuple(
        good
        for good in GOODS
        if not family[owner] & (1 << good)
    )
    others = tuple(agent for agent in range(4) if agent != owner)
    agent_pairs = tuple(itertools.combinations(others, 2))
    for second_least, least in itertools.permutations(outside, 2):
        least_construction = any(
            pairable(family[left], family[right], least)
            for left, right in agent_pairs
        )
        second_least_construction = any(
            pairable(
                family[left],
                family[right],
                second_least,
                must_cover=least,
            )
            for left, right in agent_pairs
        )
        if not least_construction and not second_least_construction:
            return True
    return False


def audit():
    checked_sdr_families = 0
    for rest in itertools.product(TRIPLES, repeat=3):
        family = (NORMALIZED_FIRST,) + rest
        if (family[0] | family[1] | family[2] | family[3]).bit_count() < 4:
            continue
        checked_sdr_families += 1
        if all(
            has_bad_ordered_low_pair(family, owner)
            for owner in range(4)
        ):
            raise AssertionError(("combinatorial counterexample", family))
    if checked_sdr_families != 175_615:
        raise AssertionError("normalized SDR-family census changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_DENSITY_FLOOR_LEMMA_AUDIT_PASSED",
        "residual_good_count": len(GOODS),
        "half_favorite_set_size": 3,
        "normalized_first_set": [0, 1, 2],
        "normalized_sdr_family_count": checked_sdr_families,
        "claim": (
            "For four three-element sets with an SDR and an ordered pair "
            "of outside goods (second least, least) for each agent, some "
            "agent admits either the least-good construction or the "
            "second-least construction with the least good absorbed by "
            "one of two disjoint set-contained pairs."
        ),
        "scope_warning": (
            "This exhaustive finite audit is a regression check for the "
            "separately written analytic proof."
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
