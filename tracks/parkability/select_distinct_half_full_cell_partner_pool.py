#!/usr/bin/env python3
"""Select favorite-pair balanced partitions by the favorite's partner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-full-cell-favorite-partner-pool-v1"


def favorite_partner(partition):
    bundle = next(bundle for bundle in partition if 0 in bundle)
    return next(good for good in bundle if good != 0)


def run(output: Path, partners):
    universe = tuple(favorite_pair_balanced_universe())
    selected = tuple(
        partition
        for partition in universe
        if favorite_partner(partition) in partners
    )
    result = {
        "schema": SCHEMA,
        "status": "PROOF_MINING_POOL",
        "favorite_partners": sorted(partners),
        "universe_size": len(universe),
        "core_size": len(selected),
        "core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in selected
        ],
        "interpretation": (
            "This is a syntactic partition family for an exact-real "
            "selection test, not a theorem or solver result."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--partner",
        type=int,
        action="append",
        required=True,
        choices=range(1, 9),
    )
    args = parser.parse_args()
    result = run(args.output, frozenset(args.partner))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
