#!/usr/bin/env python3
"""Add complete bundle-shape classes to an exact partition pool."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .run_generic_partition_cegar import load_pool, pool_document
except ImportError:
    import core
    from anneal import atomic_json
    from run_generic_partition_cegar import load_pool, pool_document


def partition_shape(partition: tuple[tuple[int, ...], ...]) -> str:
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


def eligible_partition(
    partition: tuple[tuple[int, ...], ...],
    requested_shapes: set[str],
    singleton_goods: set[int],
    required_bundle_sizes: dict[int, int],
) -> bool:
    return (
        partition_shape(partition) in requested_shapes
        or any((good,) in partition for good in singleton_goods)
    ) and all(
        len(next(bundle for bundle in partition if good in bundle)) == size
        for good, size in required_bundle_sizes.items()
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--m", type=int, required=True)
    parser.add_argument("--shape", action="append", default=[])
    parser.add_argument("--singleton-good", type=int, action="append", default=[])
    parser.add_argument(
        "--require-bundle-good-size",
        action="append",
        default=[],
        metavar="GOOD:SIZE",
    )
    parser.add_argument("--filter-input", action="store_true")
    args = parser.parse_args()
    if not args.input.is_file() or args.output.exists():
        parser.error("an existing input and new output are required")
    requested = set(args.shape)
    singleton_goods = set(args.singleton_good)
    try:
        required_bundle_sizes = {
            int(raw.split(":", 1)[0]): int(raw.split(":", 1)[1])
            for raw in args.require_bundle_good_size
        }
    except (TypeError, ValueError):
        parser.error("required bundle sizes must use GOOD:SIZE")
    if (
        not requested
        and not singleton_goods
        or any(not 0 <= good < args.m for good in singleton_goods)
        or len(required_bundle_sizes) != len(args.require_bundle_good_size)
        or any(
            not 0 <= good < args.m or not 1 <= size <= args.m
            for good, size in required_bundle_sizes.items()
        )
    ):
        parser.error("invalid shape, singleton good, or required bundle size")
    universe = list(core.iter_unlabeled_nonempty_partitions(args.n, args.m))
    valid_shapes = set(map(partition_shape, universe))
    if not requested <= valid_shapes:
        parser.error("requested shape is invalid for the cell")
    pool = load_pool(args.input, args.n, args.m)
    pool_set = set(pool)
    eligible = [
        partition
        for partition in universe
        if eligible_partition(
            partition,
            requested,
            singleton_goods,
            required_bundle_sizes,
        )
    ]
    if args.filter_input:
        eligible_set = set(eligible)
        result_pool = [partition for partition in pool if partition in eligible_set]
        added = []
    else:
        added = [partition for partition in eligible if partition not in pool_set]
        result_pool = pool + added
    atomic_json(
        args.output,
        pool_document(args.n, args.m, result_pool),
    )
    result = {
        "schema": "partition-pool-shape-augmentation-v1",
        "n": args.n,
        "m": args.m,
        "input": str(args.input.resolve()),
        "output": str(args.output.resolve()),
        "requested_shapes": sorted(requested),
        "singleton_goods": sorted(singleton_goods),
        "required_bundle_sizes": {
            str(good): required_bundle_sizes[good]
            for good in sorted(required_bundle_sizes)
        },
        "input_pool_size": len(pool),
        "eligible_partition_count": len(eligible),
        "new_partition_count": len(added),
        "output_pool_size": len(result_pool),
        "filter_input": args.filter_input,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
