#!/usr/bin/env python3
"""Audit host-by-host Hall obstructions in a blocked minimum-slot orbit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import exact_eligible, minimum_slot_orbit_states
    from .audit_threshold_plateau_exact_paths import mask_threshold, mask_value
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import exact_eligible, minimum_slot_orbit_states
    from audit_threshold_plateau_exact_paths import mask_threshold, mask_value


SCHEMA = "minimum-slot-host-hall-cycle-audit-v1"
BASE_STATE = {"floater": 8, "masks": (3, 12, 48, 192)}
MINIMA = (1, 3, 5, 7)


def minimal_hall_witnesses(edges):
    deficient = []
    for size in range(1, 5):
        for agents in itertools.combinations(range(4), size):
            neighbors = {
                bundle
                for agent in agents
                for bundle in range(4)
                if edges[agent][bundle]
            }
            if len(neighbors) < len(agents):
                deficient.append((agents, tuple(sorted(neighbors))))
    return [
        witness
        for witness in deficient
        if not any(
            set(other_agents) < set(witness[0])
            for other_agents, _other_neighbors in deficient
        )
    ]


def complete_edges(values, state, host):
    masks = list(state["masks"])
    masks[host] |= 1 << state["floater"]
    return [
        [
            mask_value(values, observer, masks[assigned])
            >= max(
                mask_threshold(values, observer, masks[target])
                for target in range(4)
                if target != assigned
            )
            for assigned in range(4)
        ]
        for observer in range(4)
    ]


def is_four_cycle(host_records):
    if len(host_records) != 4:
        return False
    pairs = []
    for host, record in enumerate(host_records):
        witnesses = record["minimal_hall_witnesses"]
        if len(witnesses) != 1:
            return False
        witness = witnesses[0]
        if len(witness["agents"]) != 2 or witness["neighbors"] != [host]:
            return False
        pairs.append(tuple(witness["agents"]))
    degrees = {agent: 0 for agent in range(4)}
    adjacency = {agent: set() for agent in range(4)}
    for left, right in pairs:
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        new = adjacency[vertex] - reached
        reached |= new
        frontier.extend(new)
    return len(set(pairs)) == 4 and set(degrees.values()) == {2} and len(reached) == 4


def run(source, output):
    document = json.loads(source.read_text())
    values = document["values"]
    states = [
        state
        for state in minimum_slot_orbit_states(
            values,
            BASE_STATE,
            MINIMA,
        )
        if exact_eligible(values, state)
    ]
    state_records = []
    for state in states:
        host_records = []
        for host in range(4):
            edges = complete_edges(values, state, host)
            witnesses = minimal_hall_witnesses(edges)
            host_records.append(
                {
                    "host": host,
                    "edges": edges,
                    "minimal_hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in witnesses
                    ],
                }
            )
        state_records.append(
            {
                "assignment": list(state["assignment"]),
                "floater": state["floater"],
                "masks": list(state["masks"]),
                "host_records": host_records,
                "four_host_pair_hall_cycle": is_four_cycle(host_records),
            }
        )
    all_cycles = bool(state_records) and all(
        record["four_host_pair_hall_cycle"] for record in state_records
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_ELIGIBLE_ORBIT_STATES_HAVE_FOUR_HOST_PAIR_HALL_CYCLE"
            if all_cycles
            else "GENERAL_HALL_OBSTRUCTION"
        ),
        "meaning": (
            "Exact EFX-feasibility graphs and inclusion-minimal Hall witnesses "
            "for every host completion of every eligible token-orbit state."
        ),
        "claim_boundary": (
            "The four-cycle pattern is a fact about this valuation, not a "
            "general Hall normal-form theorem."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "eligible_orbit_state_count": len(state_records),
        "all_states_have_four_host_pair_hall_cycle": all_cycles,
        "states": state_records,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
