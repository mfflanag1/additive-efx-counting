#!/usr/bin/env python3
"""Enumerate the 35 ordered base-size cells in the 4x9 lex-max reduction."""

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


def compositions(total: int, parts: int):
    for cuts in itertools.combinations(range(1, total), parts - 1):
        boundaries = (0, *cuts, total)
        yield tuple(
            boundaries[index + 1] - boundaries[index]
            for index in range(parts)
        )


def canonical_base(sizes: tuple[int, ...]) -> list[int | None]:
    owners = []
    for agent, size in enumerate(sizes):
        owners.extend([agent] * size)
    return [*owners, None]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be new")
    records = []
    for sizes in compositions(8, 4):
        shape = "".join(map(str, sorted(sizes, reverse=True)))
        records.append({
            "ordered_bundle_sizes": list(sizes),
            "shape": shape,
            "candidate_base_owner": canonical_base(sizes),
            "floater": 8,
        })
    shape_counts = Counter(record["shape"] for record in records)
    if len(records) != 35 or shape_counts != {
        "5111": 4,
        "4211": 12,
        "3311": 6,
        "3221": 12,
        "2222": 1,
    }:
        raise AssertionError("4x9 lex-max cell census changed")
    result = {
        "schema": "lexmax-partial-cell-census-v1",
        "n": 4,
        "m": 9,
        "allocated_good_count": 8,
        "floater": 8,
        "agent_order": [0, 1, 2, 3],
        "cell_count": len(records),
        "cell_count_by_shape": dict(sorted(shape_counts.items())),
        "cells": records,
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
