#!/usr/bin/env python3
"""Audit one-floater completion by Hall rematching of the enlarged bundles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from . import core
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
except ImportError:
    import core
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json


SCHEMA = "partial-hall-completion-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perfect_matchings(values, masks):
    totals, thresholds = core._subset_tables(values)
    n = len(values)
    graph = []
    for agent in range(n):
        neighbors = []
        for owned in range(n):
            own = totals[agent][masks[owned]]
            if all(
                target == owned or own >= thresholds[agent][masks[target]]
                for target in range(n)
            ):
                neighbors.append(owned)
        graph.append(tuple(neighbors))
    matchings = [
        permutation
        for permutation in itertools.permutations(range(n))
        if all(permutation[agent] in graph[agent] for agent in range(n))
    ]
    return tuple(graph), tuple(matchings)


def hall_witnesses(graph):
    n = len(graph)
    witnesses = []
    for size in range(1, n + 1):
        for agents in itertools.combinations(range(n), size):
            neighbors = sorted({bundle for agent in agents for bundle in graph[agent]})
            if len(neighbors) < size:
                witnesses.append((agents, tuple(neighbors)))
    return tuple(witnesses)


def one_old_good_move_completion(values, state):
    """Find a Hall completion after assigning f and moving at most one old good."""
    n = len(values)
    old_owner = {}
    for bundle, mask in enumerate(state["masks"]):
        for good in range(len(values[0])):
            if mask & (1 << good):
                old_owner[good] = bundle
    moves = [(None, None)] + [
        (good, destination)
        for good, source in old_owner.items()
        for destination in range(n)
        if destination != source
    ]
    for floater_host in range(n):
        for good, destination in moves:
            masks = list(state["masks"])
            masks[floater_host] |= 1 << state["floater"]
            if good is not None:
                source = old_owner[good]
                masks[source] ^= 1 << good
                masks[destination] |= 1 << good
            if any(mask == 0 for mask in masks):
                continue
            graph, matchings = perfect_matchings(values, tuple(masks))
            if matchings:
                return {
                    "floater_host": floater_host,
                    "moved_good": good,
                    "move_source": None if good is None else old_owner[good],
                    "move_destination": destination,
                    "masks": masks,
                    "graph": [list(row) for row in graph],
                    "matching": list(matchings[0]),
                }
    return None


def audit_profile(path: Path) -> dict:
    document = json.loads(path.read_text())
    values = core.validate_values(document["values"], expected_n=4, lower=1)
    states = enumerate_states(values)
    failed = []
    failed_by_key = {}
    successful = 0
    hall_completable = {}
    for state in states:
        hosts = []
        for host in range(4):
            masks = list(state["masks"])
            masks[host] |= 1 << state["floater"]
            graph, matchings = perfect_matchings(values, tuple(masks))
            if matchings:
                hosts.append(
                    {
                        "host": host,
                        "graph": [list(row) for row in graph],
                        "matching": list(matchings[0]),
                    }
                )
        if hosts:
            successful += 1
            hall_completable[(state["floater"], state["base_index"])] = True
            continue
        hall_completable[(state["floater"], state["base_index"])] = False
        host_obstructions = []
        for host in range(4):
            masks = list(state["masks"])
            masks[host] |= 1 << state["floater"]
            graph, matchings = perfect_matchings(values, tuple(masks))
            assert not matchings
            host_obstructions.append(
                {
                    "host": host,
                    "graph": [list(row) for row in graph],
                    "hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in hall_witnesses(graph)
                    ],
                }
            )
        failure = {
                "floater": state["floater"],
                "base_index": state["base_index"],
                "masks": list(state["masks"]),
                "utilities": list(state["utilities"]),
                "directly_insertable_hosts": list(state["insertable_hosts"]),
                "host_obstructions": host_obstructions,
            }
        failed.append(failure)
        failed_by_key[(state["floater"], state["base_index"])] = failure
    nash_products = [
        state["utilities"][0]
        * state["utilities"][1]
        * state["utilities"][2]
        * state["utilities"][3]
        for state in states
    ]
    maximum_nash = max(nash_products)
    maximum_nash_states = [
        state for state, product in zip(states, nash_products) if product == maximum_nash
    ]
    maximum_nash_hall_completable = [
        state
        for state in maximum_nash_states
        if hall_completable[(state["floater"], state["base_index"])]
    ]
    maximum_nash_one_move_witnesses = [
        one_old_good_move_completion(values, state) for state in maximum_nash_states
    ]
    utilitarian_scores = [sum(state["normalized"]) for state in states]
    maximum_utilitarian = max(utilitarian_scores)
    maximum_utilitarian_states = [
        state
        for state, score in zip(states, utilitarian_scores)
        if score == maximum_utilitarian
    ]
    maximum_utilitarian_one_move_witnesses = [
        one_old_good_move_completion(values, state)
        for state in maximum_utilitarian_states
    ]
    utility_vectors = sorted({state["utilities"] for state in states}, reverse=True)
    pareto_frontier = [
        utilities
        for utilities in utility_vectors
        if not any(
            all(other[agent] >= utilities[agent] for agent in range(4))
            and other != utilities
            for other in utility_vectors
        )
    ]
    frontier_set = set(pareto_frontier)
    frontier_states = [state for state in states if state["utilities"] in frontier_set]
    frontier_one_move = [
        one_old_good_move_completion(values, state) for state in frontier_states
    ]
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "n": 4,
        "m": len(values[0]),
        "eligible_state_count": len(states),
        "hall_completable_state_count": successful,
        "hall_blocked_state_count": len(failed),
        "universal_lemma_holds_on_profile": not failed,
        "first_counterexample": failed[0] if failed else None,
        "maximum_nash_selector": {
            "maximum_product": maximum_nash,
            "winner_count": len(maximum_nash_states),
            "hall_completable_winner_count": len(maximum_nash_hall_completable),
            "has_hall_completable_winner": bool(maximum_nash_hall_completable),
            "has_one_old_good_move_completion": any(
                witness is not None for witness in maximum_nash_one_move_witnesses
            ),
            "one_old_good_move_witness": next(
                (
                    witness
                    for witness in maximum_nash_one_move_witnesses
                    if witness is not None
                ),
                None,
            ),
            "representative_winner": {
                "floater": maximum_nash_states[0]["floater"],
                "base_index": maximum_nash_states[0]["base_index"],
                "masks": list(maximum_nash_states[0]["masks"]),
                "utilities": list(maximum_nash_states[0]["utilities"]),
                "hall_completable": hall_completable[
                    (
                        maximum_nash_states[0]["floater"],
                        maximum_nash_states[0]["base_index"],
                    )
                ],
                "hall_obstruction": failed_by_key.get(
                    (
                        maximum_nash_states[0]["floater"],
                        maximum_nash_states[0]["base_index"],
                    )
                ),
            },
        },
        "maximum_normalized_utilitarian_selector": {
            "maximum_score": {
                "numerator": maximum_utilitarian.numerator,
                "denominator": maximum_utilitarian.denominator,
            },
            "winner_count": len(maximum_utilitarian_states),
            "one_old_good_move_completable_winner_count": sum(
                witness is not None
                for witness in maximum_utilitarian_one_move_witnesses
            ),
            "has_one_old_good_move_completion": any(
                witness is not None
                for witness in maximum_utilitarian_one_move_witnesses
            ),
            "all_winners_one_old_good_move_completable": all(
                witness is not None
                for witness in maximum_utilitarian_one_move_witnesses
            ),
            "representative_winner": {
                "floater": maximum_utilitarian_states[0]["floater"],
                "base_index": maximum_utilitarian_states[0]["base_index"],
                "masks": list(maximum_utilitarian_states[0]["masks"]),
                "utilities": list(maximum_utilitarian_states[0]["utilities"]),
                "one_old_good_move_completion": (
                    maximum_utilitarian_one_move_witnesses[0]
                ),
            },
        },
        "pareto_selector": {
            "frontier_utility_vector_count": len(pareto_frontier),
            "frontier_state_count": len(frontier_states),
            "one_old_good_move_completable_state_count": sum(
                witness is not None for witness in frontier_one_move
            ),
            "has_one_old_good_move_completable_state": any(
                witness is not None for witness in frontier_one_move
            ),
            "all_frontier_states_one_old_good_move_completable": all(
                witness is not None for witness in frontier_one_move
            ),
            "first_blocked_frontier_state": next(
                (
                    {
                        "floater": state["floater"],
                        "base_index": state["base_index"],
                        "masks": list(state["masks"]),
                        "utilities": list(state["utilities"]),
                    }
                    for state, witness in zip(frontier_states, frontier_one_move)
                    if witness is None
                ),
                None,
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profiles", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema": SCHEMA,
        "claim": (
            "Every eligible four-agent one-floater EFX state has some host "
            "whose enlarged four-bundle partition supports an EFX matching."
        ),
        "profiles": [audit_profile(path) for path in args.profiles],
    }
    result["universal_lemma_survives"] = all(
        record["universal_lemma_holds_on_profile"] for record in result["profiles"]
    )
    if args.output:
        atomic_json(args.output, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
