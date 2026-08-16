#!/usr/bin/env python3
"""Audit the exhaustive four-agent bottom-pair multigraph census."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        multiplicity_signature,
    )
except ImportError:
    from anneal import atomic_json
    from run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        multiplicity_signature,
    )


SCHEMA = "bottom-pair-pattern-census-audit-v1"


def canonical(pattern):
    vertices = sorted({vertex for edge in pattern for vertex in edge})
    degree = Counter(vertex for edge in pattern for vertex in edge)
    degree_groups = []
    target_start = 0
    for value in sorted(set(degree.values()), reverse=True):
        group = tuple(vertex for vertex in vertices if degree[vertex] == value)
        targets = tuple(range(target_start, target_start + len(group)))
        degree_groups.append((group, targets))
        target_start += len(group)
    signatures = []
    for group_orders in itertools.product(
        *(itertools.permutations(group) for group, _ in degree_groups)
    ):
        mapping = {}
        for order, (_, targets) in zip(group_orders, degree_groups):
            mapping.update(zip(order, targets))
        signatures.append(
            tuple(
                sorted(
                    tuple(sorted((mapping[left], mapping[right])))
                    for left, right in pattern
                )
            )
        )
    return min(signatures)


def run(output: Path):
    residual_edges = tuple(itertools.combinations(range(8), 2))
    raw_count = 0
    signatures = set()
    for pattern in itertools.combinations_with_replacement(residual_edges, 4):
        if max(Counter(pattern).values()) > 2:
            continue
        raw_count += 1
        signatures.add(canonical(pattern))

    listed = tuple(canonical(pattern) for pattern in CANONICAL_PATTERNS)
    if len(set(listed)) != len(listed):
        raise AssertionError("listed bottom-pair patterns are not distinct")
    if signatures != set(listed):
        raise AssertionError("listed bottom-pair patterns are not exhaustive")
    census = Counter(
        multiplicity_signature(pattern) for pattern in CANONICAL_PATTERNS
    )
    result = {
        "schema": SCHEMA,
        "status": "BOTTOM_PAIR_PATTERN_CENSUS_AUDITED",
        "agent_count": 4,
        "available_residual_goods": 8,
        "raw_labeled_edge_multisets": raw_count,
        "canonical_pattern_count": len(signatures),
        "maximum_edge_multiplicity": 2,
        "multiplicity_census": {
            "+".join(map(str, signature)): count
            for signature, count in sorted(census.items(), reverse=True)
        },
        "canonical_patterns": [
            [list(edge) for edge in pattern]
            for pattern in CANONICAL_PATTERNS
        ],
        "claim_boundary": (
            "This is only the unlabeled multigraph census for four selected "
            "bottom pairs with multiplicity at most two. It proves no EFX "
            "selection statement."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))


if __name__ == "__main__":
    main()
