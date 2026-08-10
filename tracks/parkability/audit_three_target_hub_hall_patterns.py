#!/usr/bin/env python3
"""Exact census of internal blocker graphs for a hub with two leaves."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


VERTICES = ("h", "r", "s")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(values):
    values = tuple(values)
    return tuple(
        frozenset(choice)
        for size in range(len(values) + 1)
        for choice in itertools.combinations(values, size)
    )


def has_perfect_matching(neighborhoods) -> bool:
    return any(
        all(source in neighborhoods[target] for target, source in zip(VERTICES, permutation))
        for permutation in itertools.permutations(VERTICES)
    )


def minimal_hall_witnesses(neighborhoods):
    witnesses = []
    for size in range(1, len(VERTICES) + 1):
        for targets in itertools.combinations(VERTICES, size):
            neighborhood = set().union(*(neighborhoods[target] for target in targets))
            if len(neighborhood) < len(targets):
                if not any(set(old).issubset(targets) for old in witnesses):
                    witnesses.append(targets)
    return witnesses


def directed_two_cycle(neighborhoods, left, right) -> bool:
    return right in neighborhoods[left] and left in neighborhoods[right]


def run() -> dict:
    choices = {target: powerset(vertex for vertex in VERTICES if vertex != target) for target in VERTICES}
    counts = Counter()
    size_three_patterns = []

    for selected in itertools.product(*(choices[target] for target in VERTICES)):
        neighborhoods = dict(zip(VERTICES, selected))
        if has_perfect_matching(neighborhoods):
            counts["perfect_matching"] += 1
            continue

        witnesses = minimal_hall_witnesses(neighborhoods)
        minimum_size = min(map(len, witnesses))
        counts[f"minimum_hall_size_{minimum_size}"] += 1

        if minimum_size == 3:
            union = set().union(*neighborhoods.values())
            missing_source = next(vertex for vertex in VERTICES if vertex not in union)
            cycle_avoids_hub = directed_two_cycle(neighborhoods, "r", "s")
            cycle_contains_hub = (
                directed_two_cycle(neighborhoods, "h", "r")
                or directed_two_cycle(neighborhoods, "h", "s")
            )
            size_three_patterns.append(
                {
                    "missing_source": missing_source,
                    "neighborhoods": {
                        target: sorted(neighborhoods[target]) for target in VERTICES
                    },
                    "two_cycle_avoids_hub": cycle_avoids_hub,
                    "two_cycle_contains_hub": cycle_contains_hub,
                }
            )

    assert len(size_three_patterns) == 3
    assert {entry["missing_source"] for entry in size_three_patterns} == set(VERTICES)
    hard = [entry for entry in size_three_patterns if not entry["two_cycle_contains_hub"]]
    assert len(hard) == 1
    assert hard[0]["missing_source"] == "h"
    assert hard[0]["two_cycle_avoids_hub"]

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "three-target-hub-hall-pattern-audit-v1",
        "status": "CLASSIFIED",
        "target_order": list(VERTICES),
        "graph_count": sum(counts.values()),
        "counts": dict(sorted(counts.items())),
        "minimum_size_three_patterns": size_three_patterns,
        "pi_free_size_three_remainder": hard[0],
        "claim_boundary": (
            "finite directed-incidence census for one hub and two leaves; it classifies the internal "
            "Hall remainder but does not prove that flower inequalities select a hub split"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
