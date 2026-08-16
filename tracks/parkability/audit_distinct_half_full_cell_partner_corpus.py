#!/usr/bin/env python3
"""Audit an empirical no-full-cell corpus against a partner family."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_full_cell_menu_cegis import load_profiles
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_full_cell_menu_cegis import load_profiles
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-partner-corpus-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_partitions(payload):
    return tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in payload["core_partitions"]
    )


def run(pool_path: Path, source_paths):
    pool_payload = json.loads(pool_path.read_text())
    pool = decode_partitions(pool_payload)
    universe = set(favorite_pair_balanced_universe())
    if len(pool) != len(set(pool)) or not set(pool) <= universe:
        raise ValueError("invalid partner-family pool")

    profiles = []
    profile_sources = []
    position = {}
    for source_path in source_paths:
        for values in load_profiles(source_path):
            if values not in position:
                position[values] = len(profiles)
                profiles.append(values)
                profile_sources.append([])
            profile_sources[position[values]].append(str(source_path))

    repair_counts = []
    for values in profiles:
        repairs = supported_partitions(values, list(pool))
        if not repairs:
            raise AssertionError("corpus contains a partner-family escape")
        repair_counts.append(len(repairs))

    return {
        "schema": SCHEMA,
        "status": "EMPIRICAL_PARTNER_FAMILY_SURVIVES",
        "pool": {
            "path": str(pool_path),
            "sha256": sha256(pool_path),
            "favorite_partners": pool_payload.get("favorite_partners"),
            "partition_count": len(pool),
        },
        "sources": [
            {"path": str(path), "sha256": sha256(path)}
            for path in source_paths
        ],
        "distinct_profile_count": len(profiles),
        "repair_count_minimum": min(repair_counts),
        "repair_count_maximum": max(repair_counts),
        "repair_counts": repair_counts,
        "profile_source_multiplicities": [
            len(sources) for sources in profile_sources
        ],
        "interpretation": (
            "Every audited no-full-cell profile has a repair in the selected "
            "favorite-partner family. This is empirical support only; it "
            "does not prove the cap-free selector lemma."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.pool, tuple(args.source))
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
