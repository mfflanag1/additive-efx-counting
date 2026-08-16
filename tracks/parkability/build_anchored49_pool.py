#!/usr/bin/env python3
"""Build the anchored favorite-211 partition family for the 4x9 cell."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .run_generic_partition_cegar import pool_document
except ImportError:
    import core
    from anneal import atomic_json
    from run_generic_partition_cegar import pool_document


N = 4
M = 9
FAVORITES = frozenset({0, 1, 2})
NONFAVORITES = frozenset(range(3, M))


def bundle_of(
    partition: tuple[tuple[int, ...], ...],
    good: int,
) -> tuple[int, ...]:
    return next(bundle for bundle in partition if good in bundle)


def favorites_separate(partition: tuple[tuple[int, ...], ...]) -> bool:
    return len({bundle_of(partition, good) for good in FAVORITES}) == 3


def singleton_anchor(partition: tuple[tuple[int, ...], ...]) -> bool:
    return (
        bundle_of(partition, 0) == (0,)
        and favorites_separate(partition)
        and all(
            len(bundle) != 1 or bundle[0] not in NONFAVORITES
            for bundle in partition
        )
    )


def balanced_boundary(partition: tuple[tuple[int, ...], ...]) -> bool:
    return (
        sorted(map(len, partition), reverse=True) == [3, 2, 2, 2]
        and favorites_separate(partition)
        and len(bundle_of(partition, 0)) == 2
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.pool.exists() or args.audit.exists():
        parser.error("pool and audit outputs must be new")
    universe = list(core.iter_unlabeled_nonempty_partitions(N, M))
    singleton = [partition for partition in universe if singleton_anchor(partition)]
    balanced = [partition for partition in universe if balanced_boundary(partition)]
    family = sorted(set(singleton) | set(balanced))
    atomic_json(args.pool, pool_document(N, M, family))
    result = {
        "schema": "anchored-favorite-211-family-v1",
        "meaning": (
            "candidate analytic family, not a theorem: shared favorite 0 is "
            "either a protected singleton or lies on the balanced 3222 boundary"
        ),
        "n": N,
        "m": M,
        "favorite_pattern": [0, 0, 1, 2],
        "partition_universe_count": len(universe),
        "singleton_anchor_count": len(singleton),
        "balanced_boundary_count": len(balanced),
        "family_count": len(family),
        "branch_overlap_count": len(set(singleton) & set(balanced)),
        "family_count_by_shape": dict(sorted(Counter(
            "".join(map(str, sorted(map(len, partition), reverse=True)))
            for partition in family
        ).items())),
        "pool": str(args.pool.resolve()),
    }
    if (
        len(universe) != 7770
        or len(singleton) != 473
        or len(balanced) != 480
        or len(family) != 953
    ):
        raise AssertionError("anchored 4x9 family census changed")
    atomic_json(args.audit, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
