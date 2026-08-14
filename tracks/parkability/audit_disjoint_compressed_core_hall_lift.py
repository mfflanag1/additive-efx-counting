#!/usr/bin/env python3
"""Exhaustive graph audit for the disjoint compressed-core Hall lift."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def has_perfect_matching(rows, size):
    for permutation in itertools.permutations(range(size)):
        if all(permutation[row] in rows[row] for row in range(size)):
            return True
    return False


def hall_deficiencies(rows, size):
    deficiencies = []
    for mask in range(1, 1 << size):
        targets = tuple(index for index in range(size) if mask & (1 << index))
        neighbors = set().union(*(rows[index] for index in targets))
        if len(neighbors) < len(targets):
            deficiencies.append((targets, tuple(sorted(neighbors))))
    return tuple(deficiencies)


def can_saturate(rows, targets, size):
    for sources in itertools.permutations(range(size), len(targets)):
        if all(source in rows[target] for target, source in zip(targets, sources)):
            return True
    return False


def inclusion_minimal_deficiencies(deficiencies):
    return tuple(
        (left, right) for left, right in deficiencies
        if not any(set(other_left) < set(left) for other_left, _ in deficiencies)
    )


def audit_size(size):
    nonempty_rows = tuple(
        frozenset(index for index in range(size) if mask & (1 << index))
        for mask in range(1, 1 << size)
    )
    graph_count = 0
    perfect_count = 0
    deficient_count = 0
    deficiency_shapes = set()
    minimal_deficiency_checks = 0
    for rows in itertools.product(nonempty_rows, repeat=size):
        graph_count += 1
        perfect = has_perfect_matching(rows, size)
        deficiencies = hall_deficiencies(rows, size)
        assert perfect == (not deficiencies)
        if perfect:
            perfect_count += 1
        else:
            deficient_count += 1
            deficiency_shapes.update((len(left), len(right)) for left, right in deficiencies)
            for left, right in inclusion_minimal_deficiencies(deficiencies):
                assert len(right) == len(left) - 1
                assert all(
                    can_saturate(
                        rows,
                        tuple(target for target in left if target != removed),
                        size,
                    )
                    for removed in left
                )
                minimal_deficiency_checks += 1
    return {
        "owner_count": size,
        "nonempty_response_graph_count": graph_count,
        "perfect_matching_count": perfect_count,
        "hall_deficient_count": deficient_count,
        "deficiency_shapes": [list(shape) for shape in sorted(deficiency_shapes)],
        "minimal_deficiency_one_hole_checks": minimal_deficiency_checks,
    }


def run(output: Path):
    checks = [audit_size(size) for size in (3, 4)]
    result = {
        "schema": "disjoint-compressed-core-hall-lift-audit-v1",
        "status": "ALL_NONEMPTY_RESPONSE_GRAPHS_MATCH_OR_HAVE_HALL_DEFICIENCY",
        "checks": checks,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exhaustive response-incidence audit for three and four labeled "
            "bundles/sources. The analytic minimal-core argument supplies "
            "nonempty rows; converting the surviving Hall deficiency through "
            "GG supplier and priority structure remains open."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    output = ROOT / "results" / "disjoint_compressed_core_hall_lift_audit.json"
    print(json.dumps(run(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
