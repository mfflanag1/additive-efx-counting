#!/usr/bin/env python3
"""Freeze the favorite-pair coverage frontier of two-core seed profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
    )
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
    )
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-two-core-seed-pool-analysis-v1"
FAVORITE = 0


def counter_json(counter):
    return {
        "+".join(map(str, key)) if isinstance(key, tuple) else str(key): value
        for key, value in sorted(counter.items())
    }


def analyze(seed_paths):
    universe = tuple(favorite_pair_balanced_universe())
    pool = set()
    seed_records = []
    for path in seed_paths:
        values = load_values(path)
        supported = tuple(supported_partitions(values, list(universe)))
        new = tuple(partition for partition in supported if partition not in pool)
        pool.update(supported)
        seed_records.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "supported_partition_count": len(supported),
                "new_partition_count": len(new),
                "cumulative_pool_size": len(pool),
            }
        )
    missing = tuple(partition for partition in universe if partition not in pool)
    partner_histogram = Counter()
    triple_histogram = Counter()
    triple_good_frequency = Counter()
    for partition in missing:
        favorite_pair = next(bundle for bundle in partition if FAVORITE in bundle)
        partner = next(good for good in favorite_pair if good != FAVORITE)
        triple = next(bundle for bundle in partition if len(bundle) == 3)
        partner_histogram[partner] += 1
        triple_histogram[triple] += 1
        triple_good_frequency.update(triple)
    serialized_missing = json.dumps(
        [[list(bundle) for bundle in partition] for partition in missing],
        separators=(",", ":"),
    ).encode()
    if len(universe) != 840:
        raise AssertionError("favorite-pair universe changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_TWO_CORE_SEED_POOL_ANALYSIS_PASSED",
        "favorite_pair_partition_count": len(universe),
        "seed_records": seed_records,
        "covered_partition_count": len(pool),
        "missing_partition_count": len(missing),
        "missing_favorite_partner_histogram": counter_json(partner_histogram),
        "missing_triple_histogram": counter_json(triple_histogram),
        "missing_triple_good_frequency": counter_json(triple_good_frequency),
        "missing_partitions_sha256": hashlib.sha256(
            serialized_missing
        ).hexdigest(),
        "interpretation": (
            "The union is an exact empirical obstruction pool, not a proof. "
            "Its complement is the smallest current partition frontier for "
            "the conditional no-two-core search."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(tuple(args.seed))
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
