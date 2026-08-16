#!/usr/bin/env python3
"""Freeze an exact refutation of the Pareto completion selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

try:
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .scan_partial_nash_potential import matrices
    from .scan_partial_pareto_completion import exact_audit
except ImportError:
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from scan_partial_nash_potential import matrices
    from scan_partial_pareto_completion import exact_audit


SCHEMA = "partial-pareto-completion-refutation-audit-v1"
EXPECTED_BLOCKED_VECTOR = [10432, 32782, 30737, 20512]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_vector(state: dict, m: int) -> tuple[int | None, ...]:
    owner: list[int | None] = [None] * m
    for agent, mask in enumerate(state["masks"]):
        for good in range(m):
            if mask & (1 << good):
                owner[good] = agent
    return tuple(owner)


def public_state(state: dict, m: int) -> dict:
    return {
        "floater": state["floater"],
        "base_owner": list(owner_vector(state, m)),
        "utilities": list(state["utilities"]),
        "utility_product": math.prod(state["utilities"]),
        "insertable_hosts": list(state["insertable_hosts"]),
    }


def audit(source: Path) -> dict:
    profiles = list(matrices(source))
    if len(profiles) != 1 or profiles[0][0] != "values":
        raise ValueError("source must contain exactly one values matrix")
    values = profiles[0][1]
    exact = exact_audit(values)
    blocked = exact["blocked_vectors"]
    if len(blocked) != 1 or blocked[0]["utilities"] != EXPECTED_BLOCKED_VECTOR:
        raise AssertionError("the frozen blocked Pareto vector changed")
    if blocked[0]["realization_count"] != 1:
        raise AssertionError("the blocked Pareto vector is not uniquely realized")
    if blocked[0]["insertable_realization_count"]:
        raise AssertionError("the frozen Pareto vector became insertable")
    maximum = exact["maximum_product_vectors"]
    if not maximum or not any(
        record["insertable_realization_count"] > 0 for record in maximum
    ):
        raise AssertionError("the maximum-product comparison is not insertable")

    states = enumerate_states(values)
    m = len(values[0])
    by_identity = {
        (state["floater"], owner_vector(state, m)): state for state in states
    }

    def neighbors_of(identity):
        floater, owner = identity
        neighbors = []
        for ejected, host in enumerate(owner):
            if host is None:
                continue
            exchanged_owner = list(owner)
            exchanged_owner[floater] = host
            exchanged_owner[ejected] = None
            neighbor_identity = (ejected, tuple(exchanged_owner))
            if neighbor_identity in by_identity:
                neighbors.append(neighbor_identity)
        return neighbors

    blocked_identity = (
        blocked[0]["representative"]["floater"],
        tuple(blocked[0]["representative"]["base_owner"]),
    )
    blocked_state = by_identity[blocked_identity]
    blocked_owner = blocked_identity[1]
    exchange_neighbors = [
        by_identity[identity] for identity in neighbors_of(blocked_identity)
    ]
    if len(exchange_neighbors) != 1:
        raise AssertionError("the frozen local exchange degree changed")
    if not exchange_neighbors[0]["insertable_hosts"]:
        raise AssertionError("the unique local neighbor is not insertable")
    if math.prod(exchange_neighbors[0]["utilities"]) >= math.prod(
        blocked_state["utilities"]
    ):
        raise AssertionError("the unique local neighbor no longer loses product")
    component = {blocked_identity}
    stack = [blocked_identity]
    while stack:
        for identity in neighbors_of(stack.pop()):
            if identity not in component:
                component.add(identity)
                stack.append(identity)
    if len(component) != 2:
        raise AssertionError("the frozen local exchange component changed")

    higher_product_insertable = [
        state
        for state in states
        if state["insertable_hosts"]
        and math.prod(state["utilities"]) > math.prod(blocked_state["utilities"])
    ]
    assignment_distances = [
        sum(
            left != right
            for left, right in zip(
                blocked_owner,
                owner_vector(state, m),
            )
        )
        for state in higher_product_insertable
    ]
    if not assignment_distances or min(assignment_distances) != 4:
        raise AssertionError("the global-rescue assignment distance changed")
    return {
        "schema": SCHEMA,
        "status": "EXACT_PARETO_SELECTOR_REFUTATION",
        "meaning": (
            "The displayed utility vector is Pareto maximal among every "
            "eligible one-floater EFX state of the fixed additive profile, "
            "but its unique realization admits no direct insertion of the "
            "floater. The profile's maximum-product frontier vector is "
            "insertable."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "values": [list(row) for row in values],
        "eligible_base_count": exact["eligible_base_count"],
        "distinct_utility_vector_count": exact[
            "distinct_utility_vector_count"
        ],
        "pareto_frontier_utility_vector_count": exact[
            "pareto_frontier_utility_vector_count"
        ],
        "blocked_pareto_vector": blocked[0],
        "local_exchange": {
            "eligible_neighbor_count": len(exchange_neighbors),
            "neighbors": [
                public_state(state, m) for state in exchange_neighbors
            ],
            "component_state_count": len(component),
            "interpretation": (
                "The unique eligible floater exchange is insertable but "
                "strictly lowers the utility product; reversing that exchange "
                "is the only eligible continuation."
            ),
        },
        "global_rescue": {
            "higher_product_insertable_state_count": len(
                higher_product_insertable
            ),
            "minimum_good_assignment_hamming_distance": min(
                assignment_distances
            ),
        },
        "maximum_product": exact["maximum_product"],
        "maximum_product_vectors": maximum,
        "claim_boundary": (
            "This refutes the Pareto-maximal completion selector. It does "
            "not refute maximum-Nash completion or complete additive EFX."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("results/adaptive_seed_trace92_i5.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
