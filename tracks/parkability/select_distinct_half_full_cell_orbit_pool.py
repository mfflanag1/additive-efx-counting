#!/usr/bin/env python3
"""Materialize a symmetry-orbit favorite-pair partition family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_distinct_half_full_cell_cegar import favorite_pair_universe
except ImportError:
    from anneal import atomic_json
    from run_distinct_half_full_cell_cegar import favorite_pair_universe


SCHEMA = "distinct-half-full-cell-orbit-pool-v1"


def run(output: Path, family: str):
    universe = favorite_pair_universe(family)
    result = {
        "schema": SCHEMA,
        "status": "PROOF_MINING_POOL",
        "family": family,
        "universe_size": len(favorite_pair_universe("all")),
        "core_size": len(universe),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in universe
        ],
        "interpretation": (
            "This is a syntactic partition family for an exact selection "
            "test, not a theorem or solver result."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--family", choices=("six_orbit", "eight_orbit"), required=True
    )
    args = parser.parse_args()
    result = run(args.output, args.family)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
