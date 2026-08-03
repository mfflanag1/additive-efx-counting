#!/usr/bin/env python3
"""Reconstruct and analyze a distinct-half conversion-dichotomy CEGAR pool."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .run_distinct_half_conversion_dichotomy_cegar import (
        FAVORITE,
        load_values,
        repair_holds,
        repair_universe,
        select_survivors,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    from anneal import atomic_json
    from run_distinct_half_conversion_dichotomy_cegar import (
        FAVORITE,
        load_values,
        repair_holds,
        repair_universe,
        select_survivors,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-conversion-dichotomy-pool-analysis-v1"


def partition_json(partition):
    return [list(bundle) for bundle in partition]


def repair_slack(values, partition):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
    pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
    witnesses = tuple(
        (
            sum(row[good] for good in pair)
            - row[FAVORITE]
            - max(row[good] for good in low_goods),
            observer,
            pair,
        )
        for observer, row in enumerate(values)
        for pair in pairs
    )
    slack, observer, pair = min(witnesses)
    return slack, observer, pair, low_goods


def best_repair_record(values, triples):
    records = tuple(
        (repair_slack(values, partition), partition) for partition in triples
    )
    (slack, observer, pair, low_goods), partition = max(
        records,
        key=lambda item: item[0][0],
    )
    return {
        "repair_count": sum(item[0][0] >= 0 for item in records),
        "best_minimum_slack": slack,
        "best_parked_goods": list(low_goods),
        "best_partition": partition_json(partition),
        "blocking_observer": observer,
        "blocking_pair": list(pair),
    }


def reconstruct(result_path, seed_paths, add_partitions, add_repairs, selection):
    source = json.loads(result_path.read_text())
    pair_universe = tuple(favorite_pair_balanced_universe())
    triples = repair_universe()
    pair_pool = set()
    repair_pool = set()

    for seed_path in seed_paths:
        values = load_values(seed_path)
        pair_pool.update(supported_partitions(values, list(pair_universe)))
        repair_pool.update(
            partition for partition in triples if repair_holds(values, partition)
        )

    model_records = []
    for trace in source["trace"]:
        values = core.validate_values(
            trace["values"], expected_n=4, expected_m=9, lower=1
        )
        pair_survivors = tuple(
            partition
            for partition in supported_partitions(values, list(pair_universe))
            if partition not in pair_pool
        )
        repair_survivors = tuple(
            partition
            for partition in triples
            if partition not in repair_pool and repair_holds(values, partition)
        )
        if (
            len(pair_survivors) != trace["favorite_pair_efx_survivors"]
            or len(repair_survivors)
            != trace["common_low_triple_repair_survivors"]
            or len(pair_pool) != trace["pair_pool_before"]
            or len(repair_pool) != trace["repair_pool_before"]
        ):
            raise AssertionError("CEGAR trace replay changed")
        model_records.append({
            "iteration": trace["iteration"],
            "favorite_pair_efx_survivors": len(pair_survivors),
            **best_repair_record(values, triples),
        })
        pair_pool.update(
            select_survivors(pair_survivors, add_partitions, "pair", selection)
        )
        repair_pool.update(
            select_survivors(repair_survivors, add_repairs, "repair", selection)
        )

    if (
        len(pair_pool) != source["favorite_pair_pool_size"]
        or len(repair_pool) != source["common_low_triple_repair_pool_size"]
    ):
        raise AssertionError("reconstructed pool size changed")

    favorite_partner_counts = Counter()
    triple_counts = Counter()
    for partition in pair_pool:
        favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
        favorite_partner = next(good for good in favorite_bundle if good != FAVORITE)
        triple = next(bundle for bundle in partition if len(bundle) == 3)
        favorite_partner_counts[favorite_partner] += 1
        triple_counts[triple] += 1

    parked_pair_counts = Counter()
    for partition in repair_pool:
        favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
        parked_pair_counts[tuple(g for g in favorite_bundle if g != FAVORITE)] += 1

    return {
        "schema": SCHEMA,
        "status": "DICHOTOMY_POOL_REPLAY_PASSED",
        "source": str(result_path.resolve()),
        "source_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "seed_sources": [str(path.resolve()) for path in seed_paths],
        "add_partitions_per_iteration": add_partitions,
        "add_repairs_per_iteration": add_repairs,
        "survivor_selection": selection,
        "favorite_pair_pool_size": len(pair_pool),
        "common_low_triple_repair_pool_size": len(repair_pool),
        "favorite_pair_pool": [
            partition_json(partition) for partition in sorted(pair_pool)
        ],
        "common_low_triple_repair_pool": [
            partition_json(partition) for partition in sorted(repair_pool)
        ],
        "favorite_partner_counts": {
            str(good): count for good, count in sorted(favorite_partner_counts.items())
        },
        "distinct_triple_count_in_pair_pool": len(triple_counts),
        "most_common_triples": [
            {"triple": list(triple), "count": count}
            for triple, count in triple_counts.most_common(10)
        ],
        "parked_pair_counts_in_repair_pool": [
            {"parked_goods": list(goods), "count": count}
            for goods, count in sorted(parked_pair_counts.items())
        ],
        "trace_model_records": model_records,
        "interpretation": (
            "The reconstructed pool is a deterministic proof-mining boundary, "
            "not a theorem or a dichotomy counterexample. Each trace model "
            "has no common-low repair and many favorite-pair EFX witnesses."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--add-partitions", type=int, default=8)
    parser.add_argument("--add-repairs", type=int, default=8)
    parser.add_argument(
        "--selection", choices=("first", "diverse"), default="first"
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = reconstruct(
        args.result,
        tuple(args.seed),
        args.add_partitions,
        args.add_repairs,
        args.selection,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
