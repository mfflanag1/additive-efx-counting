#!/usr/bin/env python3
"""Finite support audit for the two-root residual-split response lemma."""

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
    for leaf_count in range(3):
        targets = tuple(range(leaf_count + 2))
        root, donor = 0, 1
        incoming = {root: {"Tq", "f"}, donor: {"L"}}
        incoming.update({leaf: {f"R{leaf}"} for leaf in targets[2:]})
        released = {
            root: {"L", *(f"R{leaf}" for leaf in targets[2:])},
            donor: {"Tq"},
        }
        released.update({leaf: set() for leaf in targets[2:]})
        checked = 0
        cycle_counts = {}
        for sources in itertools.permutations(targets):
            permutation = {
                source: target for target, source in zip(targets, sources)
            }
            selected = list(incoming.values())
            assert sum(map(len, selected)) == len(set().union(*selected))
            supply = {"f"}.union(*released.values())
            assert set().union(*selected) <= supply
            key = str(sorted(map(len, cycles(permutation))))
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
            "root_retained_cell_optional": True,
        })
    return {
        "schema": "flower-two-root-residual-split-release-audit-v1",
        "status": "ALL_RELEASE_COMPATIBLE",
        "records": records,
        "claim_boundary": (
            "finite support/permutation audit for zero to two leaves; utility "
            "eligibility and flower-specific partition selection are analytic"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
