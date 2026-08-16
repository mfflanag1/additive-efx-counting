#!/usr/bin/env python3
"""Exactly audit the owner-minimum substitution conversion counterexample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import core
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .audit_partial_hall_completion import perfect_matchings
    from .search_partial_hall_pair_extraction import candidate_partitions
except ImportError:
    import core
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from audit_partial_hall_completion import perfect_matchings
    from search_partial_hall_pair_extraction import candidate_partitions


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_vector(masks, m):
    vector = [-1] * m
    for owner, mask in enumerate(masks):
        for good in range(m):
            if mask & (1 << good):
                vector[good] = owner
    return tuple(vector)


def partial_eligible(values, masks, floater, permutation):
    totals, thresholds = core._subset_tables(values)
    for agent in range(4):
        own_label = permutation[agent]
        own = totals[agent][masks[own_label]]
        if own < values[agent][floater]:
            return False
        for target in range(4):
            if target != own_label and own < thresholds[agent][masks[target]]:
                return False
    return True


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    values = core.validate_values(document["values"], expected_n=4, lower=1)
    base_masks = tuple(document["base_masks"])
    floater = document["floater"]
    m = len(values[0])
    row_totals = tuple(map(sum, values))
    states = enumerate_states(values)
    base_state = next(
        state
        for state in states
        if state["floater"] == floater and state["masks"] == base_masks
    )
    base_potential = sum(base_state["normalized"], Fraction())

    owner_minima = {}
    for owner, mask in enumerate(base_masks):
        goods = [good for good in range(m) if mask & (1 << good)]
        least = min(values[owner][good] for good in goods)
        owner_minima[owner] = [
            good for good in goods if values[owner][good] == least
        ]

    complete_candidates = [
        candidate
        for candidate in candidate_partitions(base_state, m)
        if candidate[1]["moved_good"] is None
        or candidate[1]["moved_good"]
        in owner_minima[candidate[1]["move_source"]]
    ]
    completion_witnesses = []
    pair_roles = []
    for masks, operation in complete_candidates:
        graph, matchings = perfect_matchings(values, masks)
        if matchings:
            completion_witnesses.append(
                {
                    "operation": operation,
                    "masks": list(masks),
                    "matching": list(matchings[0]),
                }
            )
        for first, second in itertools.combinations(range(4), 2):
            neighbors = set(graph[first]) | set(graph[second])
            if len(neighbors) == 1:
                pair_roles.append(
                    {
                        "operation": operation,
                        "agents": [first, second],
                        "neighbor": next(iter(neighbors)),
                        "graph": [list(row) for row in graph],
                    }
                )

    improving_substitutions = []
    eligible_substitution_count = 0
    for host in range(4):
        for source_owner, goods in owner_minima.items():
            for good in goods:
                masks = list(base_masks)
                masks[host] |= 1 << floater
                masks[source_owner] ^= 1 << good
                if not all(masks):
                    continue
                for permutation in itertools.permutations(range(4)):
                    if not partial_eligible(values, tuple(masks), good, permutation):
                        continue
                    eligible_substitution_count += 1
                    potential = sum(
                        Fraction(
                            sum(
                                values[agent][item]
                                for item in range(m)
                                if masks[permutation[agent]] & (1 << item)
                            ),
                            row_totals[agent],
                        )
                        for agent in range(4)
                    )
                    if potential > base_potential:
                        improving_substitutions.append(
                            {
                                "host": host,
                                "source": source_owner,
                                "new_floater": good,
                                "permutation": list(permutation),
                                "potential_gain": {
                                    "numerator": (potential - base_potential).numerator,
                                    "denominator": (potential - base_potential).denominator,
                                },
                            }
                        )

    maximum_potential = max(
        sum(state["normalized"], Fraction()) for state in states
    )
    higher_states = [
        state
        for state in states
        if sum(state["normalized"], Fraction()) > base_potential
    ]
    base_owner_vector = owner_vector(base_masks, m)
    nearest_higher = min(
        higher_states,
        key=lambda state: sum(
            first != second
            for first, second in zip(
                base_owner_vector,
                owner_vector(state["masks"], m),
            )
        ),
        default=None,
    )
    nearest_distance = (
        sum(
            first != second
            for first, second in zip(
                base_owner_vector,
                owner_vector(nearest_higher["masks"], m),
            )
        )
        if nearest_higher is not None
        else None
    )
    artifact = {
        "schema": "partial-hall-owner-minimum-substitution-counterexample-audit-v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "base_is_eligible_one_floater_efx": True,
        "base_potential": {
            "numerator": base_potential.numerator,
            "denominator": base_potential.denominator,
        },
        "owner_minimum_goods": owner_minima,
        "selected_complete_candidate_count": len(complete_candidates),
        "selected_completion_count": len(completion_witnesses),
        "pair_witness_count": len(pair_roles),
        "designated_pair_role_present": any(
            record["operation"]
            == {
                "floater_host": 0,
                "moved_good": owner_minima[0][0],
                "move_source": 0,
                "move_destination": 1,
            }
            and record["agents"] == [0, 1]
            and record["neighbor"] == 1
            for record in pair_roles
        ),
        "eligible_substitution_allocation_count": eligible_substitution_count,
        "improving_substitution_count": len(improving_substitutions),
        "substitution_conversion_refuted": (
            not completion_witnesses and not improving_substitutions
        ),
        "eligible_state_count": len(states),
        "base_is_globally_utilitarian_maximal": not higher_states,
        "higher_eligible_state_count": len(higher_states),
        "maximum_potential": {
            "numerator": maximum_potential.numerator,
            "denominator": maximum_potential.denominator,
        },
        "nearest_higher_state": (
            {
                "floater": nearest_higher["floater"],
                "masks": list(nearest_higher["masks"]),
                "owner_distance": nearest_distance,
                "potential_gain": {
                    "numerator": (
                        sum(nearest_higher["normalized"], Fraction())
                        - base_potential
                    ).numerator,
                    "denominator": (
                        sum(nearest_higher["normalized"], Fraction())
                        - base_potential
                    ).denominator,
                },
            }
            if nearest_higher is not None
            else None
        ),
        "claim_boundary": (
            "The profile refutes conversion by one owner-minimum substitution. "
            "It refutes global normalized-utilitarian selection only if the "
            "separately reported global-maximality flag is true."
        ),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
