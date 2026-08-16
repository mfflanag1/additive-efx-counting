#!/usr/bin/env python3
"""Add scoped EFX-supporting partitions from frozen valuation models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .run_generic_partition_cegar import (
        load_pool,
        pool_document,
        supported_partitions,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from run_generic_partition_cegar import (
        load_pool,
        pool_document,
        supported_partitions,
    )


def parse_shape(raw: str, n: int, m: int) -> tuple[int, ...]:
    shape = tuple(map(int, raw.split(",")))
    if (
        len(shape) != n
        or tuple(sorted(shape, reverse=True)) != shape
        or any(size < 1 for size in shape)
        or sum(shape) != m
    ):
        raise ValueError("shape must be a descending composition of m")
    return shape


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--m", type=int, required=True)
    parser.add_argument("--input-pool", type=Path, required=True)
    parser.add_argument("--output-pool", type=Path, required=True)
    parser.add_argument("--model", type=Path, action="append", required=True)
    parser.add_argument("--partition-shape", action="append", default=[])
    parser.add_argument(
        "--partition-singleton-good",
        type=int,
        action="append",
        default=[],
    )
    parser.add_argument("--max-add-per-model", type=int)
    args = parser.parse_args()
    if (
        args.n < 2
        or args.m < args.n
        or not args.input_pool.is_file()
        or args.output_pool.exists()
        or (
            args.max_add_per_model is not None
            and args.max_add_per_model < 1
        )
    ):
        parser.error("invalid cell, paths, or addition limit")
    shapes = tuple(
        parse_shape(raw, args.n, args.m)
        for raw in args.partition_shape
    )
    singleton_goods = set(args.partition_singleton_good)
    if (
        len(set(shapes)) != len(shapes)
        or len(singleton_goods) != len(args.partition_singleton_good)
        or any(not 0 <= good < args.m for good in singleton_goods)
    ):
        parser.error("duplicate or invalid scope filters")
    universe = [
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(args.n, args.m)
        if (not shapes and not singleton_goods)
        or tuple(sorted(map(len, partition), reverse=True)) in shapes
        or any((good,) in partition for good in singleton_goods)
    ]
    pool = load_pool(args.input_pool, args.n, args.m)
    if any(partition not in universe for partition in pool):
        parser.error("input pool contains a partition outside the target scope")
    pool_set = set(pool)
    imports = []
    for model_path in args.model:
        raw = json.loads(model_path.read_text())
        candidates = []
        if raw.get("values") is not None:
            candidates.append(raw["values"])
        candidates.extend(
            record["values"]
            for record in raw.get("trace", [])
            if record.get("values") is not None
        )
        if not candidates:
            parser.error(f"model has no valuation matrix: {model_path}")
        for candidate in candidates:
            values = core.validate_values(
                candidate,
                expected_n=args.n,
                expected_m=args.m,
                lower=1,
            )
            supported = supported_partitions(values, universe)
            new = [partition for partition in supported if partition not in pool_set]
            if args.max_add_per_model is not None:
                new = new[:args.max_add_per_model]
            pool.extend(new)
            pool_set.update(new)
            imports.append({
                "model": str(model_path.resolve()),
                "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
                "supported_partition_count": len(supported),
                "new_partition_count": len(new),
            })
    atomic_json(args.output_pool, pool_document(args.n, args.m, pool))
    result = {
        "schema": "partition-pool-model-augmentation-v1",
        "n": args.n,
        "m": args.m,
        "input_pool": str(args.input_pool.resolve()),
        "output_pool": str(args.output_pool.resolve()),
        "partition_shapes": [list(shape) for shape in shapes],
        "partition_singleton_goods": sorted(singleton_goods),
        "partition_universe_size": len(universe),
        "input_pool_size": len(load_pool(args.input_pool, args.n, args.m)),
        "output_pool_size": len(pool),
        "imports": imports,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
