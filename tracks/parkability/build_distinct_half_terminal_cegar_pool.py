#!/usr/bin/env python3
"""Build a deterministic terminal-exchange obstruction pool from witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_terminal_exchange import (
        TERMINAL_PARTITIONS,
        supported,
        target_partitions,
    )
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_terminal_exchange import (
        TERMINAL_PARTITIONS,
        supported,
        target_partitions,
    )


SCHEMA = "distinct-half-terminal-exchange-pool-v1"


def load_values(path):
    payload = json.loads(path.read_text())
    values = payload.get("values")
    if values is None:
        raise ValueError(f"seed has no valuation profile: {path}")
    return tuple(tuple(row) for row in values)


def run(case, target, base_target, seed_paths, output):
    terminal = TERMINAL_PARTITIONS[case]
    universe = target_partitions(target, terminal)
    pool = set(target_partitions(base_target, terminal)) if base_target else set()
    seed_records = []
    for path in seed_paths:
        values = load_values(path)
        repairs = tuple(partition for partition in universe if supported(values, partition))
        pool.update(repairs)
        seed_records.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "target_repairs": len(repairs),
            }
        )
    if not pool or not pool.issubset(universe):
        raise ValueError("constructed pool is not a nonempty target subset")
    result = {
        "schema": SCHEMA,
        "case": case,
        "target": target,
        "base_target": base_target,
        "target_partition_count": len(universe),
        "pool_size": len(pool),
        "seed_sources": seed_records,
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in sorted(pool)
        ],
        "warning": (
            "This is a deterministic CEGAR pool, not an UNSAT core or theorem."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument(
        "--target", choices=("radius2", "eight_orbit"), required=True
    )
    parser.add_argument(
        "--base-target",
        choices=(
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
        ),
    )
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.seed and args.base_target is None:
        parser.error("a base target or seed is required")
    result = run(
        args.case,
        args.target,
        args.base_target,
        tuple(args.seed),
        args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
