#!/usr/bin/env python3
"""Mine a small radius-five rival menu covering stored Hall obstructions."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states
    from .audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        owner_vector,
        transfers,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states
    from audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        owner_vector,
        transfers,
    )


BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8


def run(source: Path, output: Path, radius: int) -> dict:
    document = json.loads(source.read_text())
    profiles = document["records"]
    base_owner = owner_vector(BASE_MASKS, BASE_FLOATER)
    coverage: dict[tuple[int, tuple[int, ...]], set[int]] = {}
    profile_improver_counts = []
    for profile_index, profile in enumerate(profiles):
        values = tuple(tuple(row) for row in profile["values"])
        row_totals = tuple(map(sum, values))
        base_score = sum(
            (
                Fraction(
                    sum(
                        values[agent][good]
                        for good in range(9)
                        if BASE_MASKS[agent] & (1 << good)
                    ),
                    row_totals[agent],
                )
                for agent in range(4)
            ),
            Fraction(),
        )
        improving = 0
        for state in enumerate_states(values):
            target_owner = owner_vector(state["masks"], state["floater"])
            distance = sum(
                left != right for left, right in zip(base_owner, target_owner)
            )
            if distance > radius:
                continue
            if sum(state["normalized"], Fraction()) <= base_score:
                continue
            improving += 1
            key = state["floater"], tuple(state["masks"])
            coverage.setdefault(key, set()).add(profile_index)
        if improving == 0:
            raise AssertionError(
                f"profile {profile['value_sha256']} has no radius-{radius} improver"
            )
        profile_improver_counts.append(improving)

    uncovered = set(range(len(profiles)))
    selected = []
    while uncovered:
        candidates = [
            (len(indices & uncovered), key, indices)
            for key, indices in coverage.items()
            if indices & uncovered
        ]
        _, key, indices = max(
            candidates,
            key=lambda item: (
                item[0],
                -sum(
                    left != right
                    for left, right in zip(
                        base_owner, owner_vector(item[1][1], item[1][0])
                    )
                ),
                -item[1][0],
                tuple(-mask for mask in item[1][1]),
            ),
        )
        newly_covered = sorted(indices & uncovered)
        target_owner = owner_vector(key[1], key[0])
        edge_list = transfers(base_owner, target_owner)
        selected.append(
            {
                "floater": key[0],
                "masks": list(key[1]),
                "owner_distance": len(edge_list),
                "transfer_component_count": component_count(edge_list),
                "newly_covered_profile_indices": newly_covered,
                "all_covered_profile_indices": sorted(indices),
                "newly_covered_value_sha256": [
                    profiles[index]["value_sha256"] for index in newly_covered
                ],
            }
        )
        uncovered -= indices

    coverage_histogram = {}
    for indices in coverage.values():
        key = str(len(indices))
        coverage_histogram[key] = coverage_histogram.get(key, 0) + 1
    artifact = {
        "schema": "partial-hall-rival-set-cover-v1",
        "status": "GREEDY_COVER",
        "meaning": (
            "Greedy set cover of exact stored canonical Hall obstructions by "
            "eligible normalized-utilitarian improving rivals within the stated "
            "owner distance. This is a corpus cover, not a symbolic theorem."
        ),
        "source": str(source),
        "profile_count": len(profiles),
        "radius": radius,
        "distinct_improving_rival_template_count": len(coverage),
        "profile_improver_counts": profile_improver_counts,
        "template_coverage_size_histogram": dict(sorted(coverage_histogram.items())),
        "selected_rival_count": len(selected),
        "selected_rivals": selected,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output, args.radius), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
