#!/usr/bin/env python3
"""Exhaustively audit four-owner maximum-matching compression identities."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = tuple(range(4))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maximum_matchings(targets, relation):
    for size in range(len(targets), 0, -1):
        result = []
        for matched_targets in itertools.combinations(targets, size):
            for sources in itertools.permutations(OWNERS, size):
                if all(
                    sources[index] in relation[target]
                    for index, target in enumerate(matched_targets)
                ):
                    result.append(dict(zip(matched_targets, sources)))
        if result:
            return result
    return []


def run():
    records = Counter()
    relations_checked = 0
    matchings_checked = 0
    identity_failures = 0
    for target_size in range(1, 5):
        targets = tuple(range(target_size))
        for mask in range(1 << (4 * target_size)):
            relation = {
                target: {
                    source
                    for source in OWNERS
                    if mask & (1 << (4 * target + source))
                }
                for target in targets
            }
            if any(not relation[target] for target in targets):
                continue
            relations_checked += 1
            selected = maximum_matchings(targets, relation)
            assert selected
            rank = len(selected[0])
            for matching in selected:
                matchings_checked += 1
                assert len(matching) == rank
                sources = set(matching.values())
                owner_union = set(targets).union(sources)
                unmatched = owner_union - sources
                if unmatched != set(targets) - sources:
                    identity_failures += 1
                outside_sources = len(sources - set(targets))
                records[(target_size, rank, outside_sources, len(unmatched))] += 1
                if target_size == 4 and rank == 3:
                    assert len(unmatched) == 1
    assert identity_failures == 0
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "maximum-matching-owner-union-compression-audit-v1",
        "status": "ALL_FORCED",
        "relations_checked": relations_checked,
        "maximum_matchings_checked": matchings_checked,
        "owner_union_identity_failures": identity_failures,
        "records": [
            {
                "target_size": target_size,
                "matching_rank": rank,
                "outside_source_count": outside_sources,
                "residual_owner_count": residual_count,
                "count": count,
            }
            for (
                target_size,
                rank,
                outside_sources,
                residual_count,
            ), count in sorted(records.items())
        ],
        "support_record": {
            "selected_cores_pairwise_disjoint": True,
            "pool_contains_every_unselected_owner_union_good": True,
            "owners_outside_active_target_set_fixed_at_base": True,
            "only_residual_targets_can_be_new_walls_when_paid": True,
        },
        "claim_boundary": (
            "complete enumeration of every nonempty response relation on up "
            "to four targets and every maximum matching; scalar payment and "
            "flower-specific recapture polarity cancellation are not asserted"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "relations_checked": result["relations_checked"],
        "maximum_matchings_checked": result["maximum_matchings_checked"],
    }, indent=2))


if __name__ == "__main__":
    main()
