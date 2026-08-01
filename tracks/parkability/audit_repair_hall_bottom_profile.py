#!/usr/bin/env python3
"""Audit one profile against the repair/Hall-cell/common-bottom trichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_eight_orbit import branch_valid
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .run_distinct_half_full_cell_cegar import (
        FAVORITE,
        M,
        common_bottom_pairs,
        favorite_pair_universe,
        pairing_has_hall_matching,
    )
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_eight_orbit import branch_valid
    from decide_common_bottom_pairing_conversion import canonical_partition
    from run_distinct_half_full_cell_cegar import (
        FAVORITE,
        M,
        common_bottom_pairs,
        favorite_pair_universe,
        pairing_has_hall_matching,
    )
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "repair-hall-bottom-profile-audit-v1"


def load_values(path: Path):
    payload = json.loads(path.read_text())
    values = payload.get("values")
    if values is None:
        raise ValueError(f"no values in {path}")
    return payload, tuple(tuple(row) for row in values)


def conversions(lows, matching):
    return tuple(
        canonical_partition(
            (FAVORITE, high),
            (*edge, low),
            *(pair for pair in matching if pair != edge),
        )
        for high, low in (lows, tuple(reversed(lows)))
        for edge in matching
    )


def run(source: Path, output: Path):
    payload, values = load_values(source)
    if not branch_valid(values):
        raise AssertionError("profile is outside the exact hard branch")
    universe = tuple(favorite_pair_universe("all"))
    repairs = set(supported_partitions(values, list(universe)))
    cells = []
    full_cells = []
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        matchings = tuple(perfect_pairings(residual))
        hall_valid = tuple(
            matching
            for matching in matchings
            if pairing_has_hall_matching(values, lows, matching)
        )
        converted_failed = []
        for matching in matchings:
            if matching in hall_valid:
                continue
            images = tuple(
                partition
                for partition in conversions(lows, matching)
                if partition in repairs
            )
            if images:
                converted_failed.append(
                    {
                        "matching": [list(edge) for edge in matching],
                        "repair_count": len(images),
                    }
                )
        order_inequalities = sum(
            row[low] <= row[good]
            for row in values
            for low in lows
            for good in residual
        )
        cell = {
            "lows": list(lows),
            "hall_valid_pairing_count": len(hall_valid),
            "hall_failed_pairing_count": 15 - len(hall_valid),
            "failed_pairings_with_a_conversion_count": len(converted_failed),
            "bottom_order_inequalities_satisfied": order_inequalities,
            "common_bottom_pair": order_inequalities == 48,
            "converted_failed_pairings": converted_failed,
        }
        cells.append(cell)
        if len(hall_valid) == 15:
            full_cells.append(list(lows))

    literal_count = independent.count_complete_efx0(values)
    reported_literal_count = payload.get("literal_complete_efx_count")
    if reported_literal_count is not None and reported_literal_count != literal_count:
        raise AssertionError("reported literal EFX count changed")
    result = {
        "schema": SCHEMA,
        "status": "PROFILE_AUDITED",
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "favorite_pair_efx_partition_count": len(repairs),
        "full_hall_cells": full_cells,
        "common_bottom_pairs": [list(pair) for pair in common_bottom_pairs(values)],
        "literal_complete_efx_count": literal_count,
        "cells": sorted(
            cells,
            key=lambda cell: (
                -cell["hall_valid_pairing_count"],
                -cell["bottom_order_inequalities_satisfied"],
                cell["lows"],
            ),
        ),
        "claim_boundary": (
            "This is an exact census for one profile, not a proof of the "
            "repair/Hall-cell/common-bottom trichotomy."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
