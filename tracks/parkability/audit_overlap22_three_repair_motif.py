#!/usr/bin/env python3
"""Audit the replicated three-repair motif in the overlap-2+2 branch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_eight_orbit import branch_valid
    from .audit_matching_augmentation import feasible_graph
    from .audit_repair_hall_bottom_profile import conversions
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
        three_agent_bottom_pairs,
    )
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_eight_orbit import branch_valid
    from audit_matching_augmentation import feasible_graph
    from audit_repair_hall_bottom_profile import conversions
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
        three_agent_bottom_pairs,
    )
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "overlap22-three-repair-motif-audit-v1"
PRIMARY_LOWS = (5, 7)
SECONDARY_LOWS = (3, 7)
AGENT_BOTTOM_PAIRS = (PRIMARY_LOWS, SECONDARY_LOWS, PRIMARY_LOWS, SECONDARY_LOWS)


def cell_pairings(values, lows):
    residual = tuple(good for good in range(1, 9) if good not in lows)
    matchings = tuple(perfect_pairings(residual))
    valid = tuple(
        matching
        for matching in matchings
        if pairing_has_hall_matching(values, lows, matching)
    )
    return matchings, valid


def audit_source(path: Path):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    if not branch_valid(values):
        raise AssertionError("profile left the exact hard branch")
    if full_hall_cells(values):
        raise AssertionError("profile gained a full Hall cell")
    if three_agent_bottom_pairs(values):
        raise AssertionError("profile gained a three-agent bottom pair")
    for agent, lows in enumerate(AGENT_BOTTOM_PAIRS):
        if max(values[agent][low] for low in lows) > min(
            values[agent][good]
            for good in range(1, 9)
            if good not in lows
        ):
            raise AssertionError("profile lost the overlap bottom pattern")

    repairs = tuple(
        supported_partitions(
            values, list(favorite_pair_universe("all"))
        )
    )
    if len(repairs) != 3:
        raise AssertionError("three-repair count changed")
    primary_matchings, primary_valid = cell_pairings(values, PRIMARY_LOWS)
    secondary_matchings, secondary_valid = cell_pairings(values, SECONDARY_LOWS)
    failed = tuple(
        matching
        for matching in primary_matchings
        if matching not in primary_valid
    )
    if len(primary_valid) != 12 or len(failed) != 3 or secondary_valid:
        raise AssertionError("12+3 / 0 Hall census changed")
    common_edges = set(failed[0]).intersection(*map(set, failed[1:]))
    if len(common_edges) != 1:
        raise AssertionError("failed matchings lost their common edge")
    converted = set()
    conversion_counts = []
    for matching in failed:
        images = tuple(
            partition
            for partition in conversions(PRIMARY_LOWS, matching)
            if partition in repairs
        )
        if len(images) != 1:
            raise AssertionError("failed matching lost its unique conversion")
        converted.update(images)
        conversion_counts.append(len(images))
    if converted != set(repairs):
        raise AssertionError("repairs are no longer exactly the conversions")
    graphs = tuple(feasible_graph(values, partition) for partition in repairs)
    literal_count = independent.count_complete_efx0(values)
    if literal_count != 180:
        raise AssertionError("literal EFX count changed")
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "primary_hall_valid_pairing_count": len(primary_valid),
        "primary_hall_failed_pairing_count": len(failed),
        "secondary_hall_valid_pairing_count": len(secondary_valid),
        "common_failed_edge": list(next(iter(common_edges))),
        "failed_pairings": [
            [list(edge) for edge in matching] for matching in failed
        ],
        "favorite_pair_repairs": [
            [list(bundle) for bundle in partition] for partition in repairs
        ],
        "repair_feasibility_graphs": [
            [[bool(entry) for entry in row] for row in graph]
            for graph in graphs
        ],
        "literal_complete_efx_count": literal_count,
        "values": [list(row) for row in values],
    }


def run(sources, output):
    if len(sources) < 2:
        raise ValueError("at least two independent sources are required")
    records = [audit_source(path) for path in sources]
    graph_signatures = {
        json.dumps(record["repair_feasibility_graphs"], sort_keys=True)
        for record in records
    }
    if len(graph_signatures) != 1:
        raise AssertionError("replicated repair graph signature changed")
    if len({json.dumps(record["values"]) for record in records}) != len(records):
        raise AssertionError("sources are not distinct profiles")
    result = {
        "schema": SCHEMA,
        "status": "OVERLAP22_THREE_REPAIR_MOTIF_AUDITED",
        "profile_count": len(records),
        "agent_bottom_pairs": [list(pair) for pair in AGENT_BOTTOM_PAIRS],
        "favorite_pair_repair_count_per_profile": 3,
        "primary_cell_hall_split": [12, 3],
        "secondary_cell_hall_split": [0, 15],
        "repairs_are_exactly_failed_pairing_conversions": True,
        "repair_feasibility_graph_signature_shared": True,
        "literal_complete_efx_count_per_profile": 180,
        "profiles": records,
        "claim_boundary": (
            "This is an exact replicated positive-boundary audit. It does "
            "not prove a three-repair floor or rule out a zero-repair "
            "profile."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(tuple(args.source), args.output), indent=2))


if __name__ == "__main__":
    main()
