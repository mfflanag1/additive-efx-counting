#!/usr/bin/env python3
"""Exhaustively audit minimal-Hall owner-union compression for four owners."""

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


def neighbors(relation, targets):
    return set().union(*(relation[target] for target in targets))


def has_matching(relation, targets, sources):
    targets = tuple(targets)
    sources = tuple(sources)
    if len(targets) != len(sources):
        return False
    return any(
        all(source in relation[target] for target, source in zip(targets, perm))
        for perm in itertools.permutations(sources)
    )


def is_minimal_defect(relation, targets):
    targets = tuple(targets)
    if len(neighbors(relation, targets)) >= len(targets):
        return False
    return all(
        len(neighbors(relation, subset)) >= len(subset)
        for size in range(1, len(targets))
        for subset in itertools.combinations(targets, size)
    )


def run():
    nonempty_relations = 0
    defect_counts = Counter()
    edges_checked = 0
    deficiency_failures = 0
    matching_failures = 0
    edge_extension_failures = 0

    for mask in range(1 << 16):
        relation = {
            target: {
                source
                for source in OWNERS
                if mask & (1 << (4 * target + source))
            }
            for target in OWNERS
        }
        if any(not relation[target] for target in OWNERS):
            continue
        nonempty_relations += 1
        for size in range(2, 5):
            for targets in itertools.combinations(OWNERS, size):
                if not is_minimal_defect(relation, targets):
                    continue
                sources = neighbors(relation, targets)
                defect_counts[(size, len(set(targets) & sources))] += 1
                if len(sources) != size - 1:
                    deficiency_failures += 1
                    continue

                if not all(
                    has_matching(
                        relation,
                        tuple(target for target in targets if target != omitted),
                        sources,
                    )
                    for omitted in targets
                ):
                    matching_failures += 1

                for target in targets:
                    for source in relation[target]:
                        edges_checked += 1
                        other_targets = tuple(
                            owner for owner in targets if owner != target
                        )
                        matching = None
                        for perm in itertools.permutations(sources):
                            if all(
                                candidate in relation[other]
                                for other, candidate in zip(other_targets, perm)
                            ):
                                matching = dict(zip(other_targets, perm))
                                break
                        assert matching is not None
                        matched_target = next(
                            other
                            for other, candidate in matching.items()
                            if candidate == source
                        )
                        matching.pop(matched_target)
                        matching[target] = source
                        if len(set(matching.values())) != size - 1:
                            edge_extension_failures += 1
                        if not all(
                            candidate in relation[other]
                            for other, candidate in matching.items()
                        ):
                            edge_extension_failures += 1

    assert defect_counts
    assert deficiency_failures == 0
    assert matching_failures == 0
    assert edge_extension_failures == 0

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "minimal-hall-owner-union-compression-audit-v1",
        "status": "ALL_FORCED",
        "relation_records": {
            "nonempty_relations_checked": nonempty_relations,
            "minimal_defects_by_target_size_and_overlap": [
                {
                    "target_size": size,
                    "target_source_overlap": overlap,
                    "count": count,
                }
                for (size, overlap), count in sorted(defect_counts.items())
            ],
            "response_edges_checked": edges_checked,
            "deficiency_one_failures": deficiency_failures,
            "near_perfect_matching_failures": matching_failures,
            "edge_extension_failures": edge_extension_failures,
        },
        "support_record": {
            "selected_cells": ["desired_core_for_each_source"],
            "residual_pool": "all_unselected_goods_in_owner_union",
            "outside_owner_targets_fixed": True,
            "complete_after_residual_partition": True,
        },
        "claim_boundary": (
            "complete enumeration of all nonempty four-by-four response "
            "relations and every inclusion-minimal deficient target subset; "
            "existence of a flower-specific residual payment/EFX partition "
            "is not asserted"
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
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
