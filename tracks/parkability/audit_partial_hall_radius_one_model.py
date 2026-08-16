#!/usr/bin/env python3
"""Solver-independent replay of a fixed-base radius-one Hall obstruction."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from fractions import Fraction

try:
    from . import core
    from .anneal import atomic_json
    from .audit_partial_hall_completion import hall_witnesses, perfect_matchings
    from .analyze_partial_state_potentials import enumerate_states
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    import core
    from anneal import atomic_json
    from audit_partial_hall_completion import hall_witnesses, perfect_matchings
    from analyze_partial_state_potentials import enumerate_states
    from decide_partial_hall_radius_one import candidate_partitions


SCHEMA = "partial-hall-radius-one-model-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_efx(values, bundles):
    for agent in range(len(values)):
        own = sum(values[agent][good] for good in bundles[agent])
        for target, bundle in enumerate(bundles):
            if target == agent:
                continue
            for removed in bundle:
                residual = sum(
                    values[agent][good] for good in bundle if good != removed
                )
                if own < residual:
                    return False
    return True


def owner_vector(masks, floater, m):
    owners = [-1] * m
    for owner, mask in enumerate(masks):
        for good in range(m):
            if mask & (1 << good):
                owners[good] = owner
    owners[floater] = -1
    return tuple(owners)


def run(source):
    document = json.loads(source.read_text())
    values = core.validate_values(document["values"], expected_n=4, expected_m=9, lower=1)
    base = tuple(tuple(bundle) for bundle in document["base_bundles"])
    floater = document["floater"]
    if not is_efx(values, base):
        raise AssertionError("fixed base is not EFX")
    if any(
        sum(values[agent][good] for good in base[agent])
        < values[agent][floater]
        for agent in range(4)
    ):
        raise AssertionError("fixed base fails floater nonenvy")

    partitions = list(candidate_partitions(base, floater))
    completable = []
    graph_signatures = set()
    primary_hall_types = Counter()
    minimal_hall_types = Counter()
    move_family_hall_types = Counter()
    for move in partitions:
        partition = move["partition"]
        masks = tuple(sum(1 << good for good in bundle) for bundle in partition)
        graph, matchings = perfect_matchings(values, masks)
        graph_signatures.add(graph)
        if matchings:
            completable.append(
                {
                    **move,
                    "partition": [list(bundle) for bundle in partition],
                    "graph": [list(row) for row in graph],
                    "matching": list(matchings[0]),
                }
            )
            continue
        witnesses = hall_witnesses(graph)
        primary = witnesses[0]
        primary_type = f"{len(primary[0])}->{len(primary[1])}"
        primary_hall_types[primary_type] += 1
        move_family = (
            "radius0"
            if move["moved_good"] is None
            else f"{move['move_source']}->{move['move_destination']}"
        )
        move_family_hall_types[f"{move_family}:{primary_type}"] += 1
        witness_agent_sets = {frozenset(agents) for agents, _ in witnesses}
        for agents, neighbors in witnesses:
            agent_set = frozenset(agents)
            if any(
                proper < agent_set for proper in witness_agent_sets
            ):
                continue
            minimal_hall_types[f"{len(agents)}->{len(neighbors)}"] += 1
    if completable:
        raise AssertionError("claimed radius-one obstruction has a completion")
    base_masks = tuple(sum(1 << good for good in bundle) for bundle in base)
    base_utilities = tuple(
        sum(values[agent][good] for good in base[agent]) for agent in range(4)
    )
    base_owner = owner_vector(base_masks, floater, 9)
    dominators = []
    row_totals = tuple(map(sum, values))
    base_utilitarian = sum(
        Fraction(base_utilities[agent], row_totals[agent])
        for agent in range(4)
    )
    utilitarian_improvers = []
    for state in enumerate_states(values):
        state_utilitarian = sum(state["normalized"], Fraction())
        if state_utilitarian > base_utilitarian:
            target_owner = owner_vector(state["masks"], state["floater"], 9)
            gain = state_utilitarian - base_utilitarian
            utilitarian_improvers.append(
                {
                    "floater": state["floater"],
                    "base_index": state["base_index"],
                    "utilities": list(state["utilities"]),
                    "masks": list(state["masks"]),
                    "owner_distance": sum(
                        left != right
                        for left, right in zip(base_owner, target_owner)
                    ),
                    "normalized_utilitarian_gain": {
                        "numerator": gain.numerator,
                        "denominator": gain.denominator,
                    },
                }
            )
        if not (
            all(state["utilities"][agent] >= base_utilities[agent] for agent in range(4))
            and state["utilities"] != base_utilities
        ):
            continue
        target_owner = owner_vector(state["masks"], state["floater"], 9)
        dominators.append(
            {
                "floater": state["floater"],
                "base_index": state["base_index"],
                "utilities": list(state["utilities"]),
                "masks": list(state["masks"]),
                "owner_distance": sum(
                    left != right for left, right in zip(base_owner, target_owner)
                ),
            }
        )
    dominators.sort(
        key=lambda record: (
            record["owner_distance"],
            -sum(record["utilities"]),
            record["floater"],
            record["base_index"],
        )
    )
    utilitarian_improvers.sort(
        key=lambda record: (
            record["owner_distance"],
            -Fraction(
                record["normalized_utilitarian_gain"]["numerator"],
                record["normalized_utilitarian_gain"]["denominator"],
            ),
            record["floater"],
            record["base_index"],
        )
    )
    return {
        "schema": SCHEMA,
        "status": "VERIFIED_RADIUS_ONE_HALL_OBSTRUCTION",
        "meaning": (
            "The displayed eligible partial EFX state has no Hall-completable "
            "partition after assigning the floater and moving at most one old good."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "n": 4,
        "m": 9,
        "floater": floater,
        "base_bundles": [list(bundle) for bundle in base],
        "base_efx": True,
        "floater_nonenvy": True,
        "candidate_partition_count": len(partitions),
        "matching_count_per_partition": math_factorial(4),
        "checked_partition_matching_pairs": len(partitions) * math_factorial(4),
        "distinct_feasibility_graph_count": len(graph_signatures),
        "primary_hall_type_histogram": dict(sorted(primary_hall_types.items())),
        "inclusion_minimal_hall_type_histogram": dict(
            sorted(minimal_hall_types.items())
        ),
        "move_family_primary_hall_type_histogram": dict(
            sorted(move_family_hall_types.items())
        ),
        "hall_completable_partition_count": 0,
        "base_utilities": list(base_utilities),
        "pareto_dominator_count": len(dominators),
        "nearest_pareto_dominator": dominators[0] if dominators else None,
        "normalized_utilitarian_improver_count": len(utilitarian_improvers),
        "nearest_normalized_utilitarian_improver": (
            utilitarian_improvers[0] if utilitarian_improvers else None
        ),
    }


def math_factorial(value):
    result = 1
    for factor in range(2, value + 1):
        result *= factor
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
