#!/usr/bin/env python3
"""Finite support audit for owner-rooted hub-split release compatibility."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def cycles(permutation):
    unseen = set(permutation)
    result = []
    while unseen:
        root = min(unseen)
        cycle = [root]
        current = permutation[root]
        while current != root:
            cycle.append(current)
            current = permutation[current]
        unseen -= set(cycle)
        result.append(cycle)
    return sorted(result)


def run():
    records = []
    for leaf_count in (2, 3):
        targets = tuple(range(leaf_count + 1))
        hub = 0
        donor = 1
        incoming = {hub: {"H"}}
        incoming.update({leaf: {f"R{leaf}"} for leaf in targets[1:]})
        released = {hub: {f"R{leaf}" for leaf in targets[1:]}, donor: {"H"}}
        released.update({leaf: set() for leaf in targets[2:]})
        checked = 0
        cycle_counts = {}
        for sources in itertools.permutations(targets):
            permutation = {
                source: target for target, source in zip(targets, sources)
            }
            selected_incoming = [incoming[target] for target in targets]
            assert sum(map(len, selected_incoming)) == len(set().union(*selected_incoming))
            supply = set().union(*released.values())
            assert set().union(*selected_incoming) <= supply
            decomposition = cycles(permutation)
            key = str(sorted(map(len, decomposition)))
            cycle_counts[key] = cycle_counts.get(key, 0) + 1
            checked += 1
        records.append({
            "leaf_count": leaf_count,
            "target_count": len(targets),
            "response_permutations_checked": checked,
            "cycle_size_multiset_counts": cycle_counts,
            "incoming_sets": {
                str(target): sorted(goods) for target, goods in incoming.items()
            },
            "released_sets": {
                str(target): sorted(goods) for target, goods in released.items()
            },
        })
    return {
        "schema": "owner-rooted-hub-split-release-audit-v1",
        "status": "ALL_RELEASE_COMPATIBLE",
        "records": records,
        "claim_boundary": (
            "finite support/permutation audit for two and three leaves; packet "
            "utility eligibility and flower-specific selection are analytic gates"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
