#!/usr/bin/env python3
"""Relabel an overlap-2+2 profile into bottom-pattern zero coordinates."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import audit_threshold_failure
except ImportError:
    import independent
    from anneal import atomic_json
    from run_bottom_pair_pattern_selector_cegar import goods_pattern
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import audit_threshold_failure


SCHEMA = "canonical-overlap-bottom-profile-v1"
AGENT_ORDER = (0, 2, 1, 3)
GOOD_ORDER = (0, 7, 5, 3, 1, 2, 4, 6, 8)


def run(source: Path, output: Path):
    payload = json.loads(source.read_text())
    raw_values = payload["values"]
    values = tuple(
        tuple(raw_values[old_agent][old_good] for old_good in GOOD_ORDER)
        for old_agent in AGENT_ORDER
    )
    if any(row[0] <= max(row[1:]) for row in values):
        raise AssertionError("strict common favorite was not preserved")
    audit_threshold_failure(values)
    pattern = goods_pattern(0)
    for agent, lows in enumerate(pattern):
        if max(values[agent][low] for low in lows) > min(
            values[agent][good]
            for good in range(1, 9)
            if good not in lows
        ):
            raise AssertionError("canonical bottom pattern was not preserved")
    if full_hall_cells(values):
        raise AssertionError("canonical profile gained a full Hall cell")
    if three_agent_bottom_pairs(values):
        raise AssertionError("canonical profile gained a three-agent bottom pair")
    repairs = supported_partitions(
        values, list(favorite_pair_universe("all"))
    )
    literal_count = independent.count_complete_efx0(values)
    if (
        payload.get("favorite_pair_repair_count") is not None
        and payload["favorite_pair_repair_count"] != len(repairs)
    ):
        raise AssertionError("favorite-pair repair count changed")
    if (
        payload.get("literal_complete_efx_count") is not None
        and payload["literal_complete_efx_count"] != literal_count
    ):
        raise AssertionError("literal EFX count changed")
    result = {
        "schema": SCHEMA,
        "status": "OVERLAP_BOTTOM_PROFILE_CANONICALIZED",
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "agent_order_new_to_old": list(AGENT_ORDER),
        "good_order_new_to_old": list(GOOD_ORDER),
        "pattern_index": 0,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "favorite_pair_repair_count": len(repairs),
        "favorite_pair_repairs": [
            [list(bundle) for bundle in partition]
            for partition in repairs
        ],
        "full_hall_cells": [],
        "three_agent_bottom_pairs": [],
        "literal_complete_efx_count": literal_count,
        "values": [list(row) for row in values],
        "claim_boundary": (
            "This is a symmetry relabeling of one positive profile, not a "
            "selector proof or an EFX counterexample."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
