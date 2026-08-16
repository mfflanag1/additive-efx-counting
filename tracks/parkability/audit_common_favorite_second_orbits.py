#!/usr/bin/env python3
"""Audit the second-favorite orbit split inside the common-favorite cell."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "common-favorite-second-orbits-4x9-audit-v1"
REPRESENTATIVES = {
    "4": [1, 1, 1, 1],
    "31": [1, 1, 1, 2],
    "22": [1, 1, 2, 2],
    "211": [1, 1, 2, 3],
    "1111": [1, 2, 3, 4],
}
EXPECTED_RAW_COUNTS = {
    "4": 8,
    "31": 224,
    "22": 168,
    "211": 2016,
    "1111": 1680,
}


def signature(vector: tuple[int, ...]) -> str:
    return "".join(
        map(str, sorted(Counter(vector).values(), reverse=True))
    )


def audit() -> dict:
    counts = Counter(
        signature(vector)
        for vector in itertools.product(range(1, 9), repeat=4)
    )
    if dict(counts) != EXPECTED_RAW_COUNTS or sum(counts.values()) != 8**4:
        raise AssertionError("second-favorite orbit census changed")
    if any(signature(tuple(vector)) != name for name, vector in REPRESENTATIVES.items()):
        raise AssertionError("an orbit representative has the wrong signature")
    return {
        "schema": SCHEMA,
        "status": "SECOND_FAVORITE_ORBIT_AUDIT_PASSED",
        "scope": {
            "agents": 4,
            "goods": 9,
            "fixed_common_favorite": 0,
            "second_favorite_choices_per_agent": 8,
            "raw_vectors": 8**4,
        },
        "orbit_count": len(REPRESENTATIVES),
        "orbits": [
            {
                "multiplicity": name,
                "representative": vector,
                "raw_vector_count": counts[name],
            }
            for name, vector in REPRESENTATIVES.items()
        ],
        "meaning": (
            "Agent permutations and permutations of goods 1,...,8 reduce "
            "all strict second-favorite vectors to these five cells."
        ),
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
