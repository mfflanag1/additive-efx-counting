#!/usr/bin/env python3
"""Audit and aggregate exhaustive two-anchor decision shards."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from .run_fixed_u_full_packet_terminal_cegar import OWNERS


def run(shard_paths, output_path):
    shards = [json.loads(path.read_text()) for path in shard_paths]
    assert shards
    profile_hashes = {shard["profile_sha256"] for shard in shards}
    eligible_sets = {tuple(shard["eligible_roles"]) for shard in shards}
    edge_caps = {shard["edge_cap"] for shard in shards}
    moduli = {shard["pair_modulus"] for shard in shards}
    assert len(profile_hashes) == len(eligible_sets) == len(edge_caps) == len(moduli) == 1
    modulus = next(iter(moduli))
    assert sorted(shard["pair_remainder"] for shard in shards) == list(range(modulus))

    eligible = next(iter(eligible_sets))
    expected = {
        "|".join((f"{left}:{a}", f"{right}:{b}"))
        for left, right in itertools.combinations(eligible, 2)
        for a, b in itertools.product(OWNERS, repeat=2)
    }
    records = [record for shard in shards for record in shard["records"]]
    keys = [record["key"] for record in records]
    assert len(keys) == len(set(keys))
    assert set(keys) == expected
    unknowns = [record for record in records if record["status"] == "unknown"]
    sats = [record for record in records if record["status"] == "sat"]
    result = {
        "schema": "fixed-u-two-anchor-shard-aggregate-v1",
        "status": (
            "UNKNOWN_TWO_ANCHOR_DECISION" if unknowns
            else "SAT_TWO_ANCHOR_CERTIFICATE" if sats
            else "UNSAT_NO_UNIVERSAL_TWO_ANCHOR_CERTIFICATE"
        ),
        "profile_sha256": next(iter(profile_hashes)),
        "edge_cap": next(iter(edge_caps)),
        "eligible_roles": list(eligible),
        "role_pair_count": len(tuple(itertools.combinations(eligible, 2))),
        "anchor_observer_pair_count_per_role_pair": len(OWNERS) ** 2,
        "expected_lane_count": len(expected),
        "audited_lane_count": len(records),
        "sat_count": len(sats),
        "unknown_count": len(unknowns),
        "shards": [
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "pair_remainder": shard["pair_remainder"],
                "lane_count": len(shard["records"]),
            }
            for path, shard in zip(shard_paths, shards)
        ],
        "claim_boundary": (
            "This exhausts the universal two-anchor endpoint mechanism on one "
            "admissible form-2 profile. The independent physical witness is the "
            "stronger refutation of arbitrary allocations with at most two split roles."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.shard, args.output)
    print(json.dumps({
        key: result[key] for key in (
            "status", "role_pair_count", "expected_lane_count",
            "audited_lane_count", "sat_count", "unknown_count",
        )
    }, indent=2))


if __name__ == "__main__":
    main()
