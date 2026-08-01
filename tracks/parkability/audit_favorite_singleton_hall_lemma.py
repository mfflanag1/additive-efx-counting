#!/usr/bin/env python3
"""Exhaustive small-grid audit of the favorite-singleton Hall lemma."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
except ImportError:
    import independent
    from anneal import atomic_json


SCHEMA = "favorite-singleton-hall-lemma-audit-v1"


def residual_partitions(goods: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    partitions = set()
    for owners in itertools.product(range(2), repeat=len(goods)):
        if set(owners) != {0, 1}:
            continue
        bundles = tuple(
            sorted(
                tuple(good for good, owner in zip(goods, owners) if owner == slot)
                for slot in range(2)
            )
        )
        partitions.add(bundles)
    return tuple(sorted(partitions))


def bundle_threshold(row: tuple[int, ...], bundle: tuple[int, ...]) -> int:
    if not bundle:
        return 0
    return sum(row[good] for good in bundle) - min(row[good] for good in bundle)


def resident_edge(
    values: tuple[tuple[int, ...], ...],
    resident: int,
    own_index: int,
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    own = sum(values[resident][good] for good in partition[own_index])
    return all(
        own >= bundle_threshold(values[resident], target)
        for target_index, target in enumerate(partition)
        if target_index != own_index
    )


def hall_conditions(
    values: tuple[tuple[int, ...], ...],
    owner: int,
    favorite: int,
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    owner_threshold = max(
        bundle_threshold(values[owner], bundle)
        for bundle in partition
    )
    if values[owner][favorite] < owner_threshold:
        return False
    residents = tuple(agent for agent in range(3) if agent != owner)
    return any(
        all(
            resident_edge(values, resident, own_index, partition)
            for resident, own_index in zip(residents, matching)
        )
        for matching in itertools.permutations(range(2))
    )


def literal_completion_exists(
    values: tuple[tuple[int, ...], ...],
    owner: int,
    favorite: int,
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    residents = tuple(agent for agent in range(3) if agent != owner)
    for matching in itertools.permutations(range(2)):
        assignment = [owner] * 4
        assignment[favorite] = owner
        for resident, bundle_index in zip(residents, matching):
            for good in partition[bundle_index]:
                assignment[good] = resident
        if independent.is_complete_efx0(values, assignment):
            return True
    return False


def audit() -> dict:
    n = 3
    m = 4
    favorite = 0
    partitions = residual_partitions(tuple(range(1, m)))
    profile_count = 0
    owner_partition_checks = 0
    positive_cases = 0
    for flat in itertools.product((1, 2), repeat=n * m):
        values = tuple(
            tuple(flat[agent * m:(agent + 1) * m])
            for agent in range(n)
        )
        profile_count += 1
        for owner in range(n):
            for partition in partitions:
                encoded = hall_conditions(values, owner, favorite, partition)
                literal = literal_completion_exists(
                    values,
                    owner,
                    favorite,
                    partition,
                )
                if encoded != literal:
                    raise AssertionError((values, owner, partition, encoded, literal))
                owner_partition_checks += 1
                positive_cases += int(encoded)
    return {
        "schema": SCHEMA,
        "status": "EXHAUSTIVE_SMALL_GRID_AUDIT_PASSED",
        "n": n,
        "m": m,
        "value_domain": [1, 2],
        "fixed_singleton_good": favorite,
        "valuation_profile_count": profile_count,
        "residual_partition_count": len(partitions),
        "owner_partition_checks": owner_partition_checks,
        "positive_condition_count": positive_cases,
        "claim": (
            "For every audited owner and residual partition, the scalar "
            "owner threshold plus resident perfect-matching condition is "
            "equivalent to literal complete EFX with the fixed singleton."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
