#!/usr/bin/env python3
"""Select a deterministic subfamily of terminal radius-two targets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_terminal_exchange import (
        FAVORITE,
        TERMINAL_PARTITIONS,
        target_partitions,
    )
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_terminal_exchange import (
        FAVORITE,
        TERMINAL_PARTITIONS,
        target_partitions,
    )


SCHEMA = "distinct-half-terminal-target-pool-v1"


def favorite_partner(partition):
    return next(
        good
        for bundle in partition
        if FAVORITE in bundle
        for good in bundle
        if good != FAVORITE
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument(
        "--family", choices=("unrepresented_new_partner",), required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    terminal = TERMINAL_PARTITIONS[args.case]
    terminal_triple = next(bundle for bundle in terminal if len(bundle) == 3)
    universe = target_partitions("radius2_new_favorite_partner", terminal)
    selected = tuple(
        partition
        for partition in universe
        if favorite_partner(partition) not in terminal_triple
    )
    encoded = json.dumps(
        [[list(bundle) for bundle in partition] for partition in selected],
        separators=(",", ":"),
    ).encode()
    result = {
        "schema": SCHEMA,
        "status": "TARGET_POOL_SELECTED",
        "case": args.case,
        "family": args.family,
        "parent_family": "radius2_new_favorite_partner",
        "parent_partition_count": len(universe),
        "core_partition_count": len(selected),
        "core_partitions_sha256": hashlib.sha256(encoded).hexdigest(),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in selected
        ],
    }
    expected = 36 if args.case == "R" else 39
    if len(selected) != expected:
        raise AssertionError("unrepresented-partner target count changed")
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
