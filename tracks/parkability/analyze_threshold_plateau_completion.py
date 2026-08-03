#!/usr/bin/env python3
"""Analyze completion transitions inside a maximum-threshold plateau."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .fast_count import FastParkability
    from .scan_partial_nash_potential import matrices
except ImportError:
    from anneal import atomic_json
    from fast_count import FastParkability
    from scan_partial_nash_potential import matrices


def values_sha256(values) -> str:
    return hashlib.sha256(
        json.dumps(values, separators=(",", ":")).encode()
    ).hexdigest()


def owners(masks, floater: int, m: int) -> tuple[int, ...]:
    result = [-1] * m
    for agent, mask in enumerate(masks):
        for good in range(m):
            if mask & (1 << good):
                if result[good] != -1:
                    raise AssertionError("overlapping masks")
                result[good] = agent
    if result[floater] != -1 or result.count(-1) != 1:
        raise AssertionError("invalid one-floater owner vector")
    return tuple(result)


def transition_kind(left, right) -> str:
    changed = tuple(
        good for good, (a, b) in enumerate(zip(left, right)) if a != b
    )
    if len(changed) == 1:
        return "same-floater-one-good-transfer"
    if len(changed) == 2:
        old_floater = left.index(-1)
        new_floater = right.index(-1)
        if (
            old_floater != new_floater
            and set(changed) == {old_floater, new_floater}
        ):
            return "one-good-floater-swap"
    return f"owner-distance-{len(changed)}"


def bundle_from_owners(owner_vector, agent: int) -> tuple[int, ...]:
    return tuple(
        good for good, owner in enumerate(owner_vector) if owner == agent
    )


def threshold(values, agent: int, bundle: tuple[int, ...]) -> int:
    if not bundle:
        return 0
    entries = tuple(values[agent][good] for good in bundle)
    return sum(entries) - min(entries)


def minimum_slot_cycle(values, left, right) -> tuple[bool, bool]:
    changed_goods = tuple(
        good for good, (old, new) in enumerate(zip(left, right)) if old != new
    )
    vertices = {left[good] for good in changed_goods} | {
        right[good] for good in changed_goods
    }
    is_cycle = all(
        sum(left[good] == vertex for good in changed_goods)
        == sum(right[good] == vertex for good in changed_goods)
        == 1
        for vertex in vertices
    )
    ownerwise_preserving = True
    minimum_slots = is_cycle
    for agent in range(len(values)):
        old_bundle = bundle_from_owners(left, agent)
        new_bundle = bundle_from_owners(right, agent)
        if old_bundle == new_bundle:
            continue
        ownerwise_preserving &= (
            threshold(values, agent, old_bundle)
            == threshold(values, agent, new_bundle)
        )
        outgoing = tuple(good for good in old_bundle if good not in new_bundle)
        incoming = tuple(good for good in new_bundle if good not in old_bundle)
        minimum_slots &= (
            len(outgoing) == len(incoming) == 1
            and values[agent][outgoing[0]]
            == min(values[agent][good] for good in old_bundle)
            and values[agent][incoming[0]]
            == min(values[agent][good] for good in new_bundle)
        )
    return minimum_slots, ownerwise_preserving


def floater_swap_distances(states, *, strictly_improving_margin=False):
    by_owners = {state["owners"]: state for state in states}
    distances = {}
    queue = deque()
    for state in states:
        if state["hall_insertable"]:
            distances[state["owners"]] = 0
            queue.append(state["owners"])
    while queue:
        current = queue.popleft()
        floater = current.index(-1)
        for good, owner in enumerate(current):
            if owner == -1:
                continue
            neighbor = list(current)
            neighbor[floater] = owner
            neighbor[good] = -1
            key = tuple(neighbor)
            if key not in by_owners or key in distances:
                continue
            if (
                strictly_improving_margin
                and by_owners[key]["hall_margin"]
                >= by_owners[current]["hall_margin"]
            ):
                continue
            distances[key] = distances[current] + 1
            queue.append(key)
    return distances


def load_values(record: dict):
    path = Path(record["source"])
    matches = [
        values
        for _key, values in matrices(path)
        if values_sha256(values) == record["values_sha256"]
    ]
    if len(matches) != 1:
        raise AssertionError((path, record["values_sha256"], len(matches)))
    return matches[0]


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    records = []
    for failure in document["direct_hall_failures"]:
        values = load_values(failure)
        n = len(values)
        m = len(values[0])
        evaluator = FastParkability(n, m)
        landscape = evaluator.partial_linear_potential_landscape(
            values,
            potential="normalized_threshold",
        )
        maximizers = []
        for winner in landscape["maximizers"]:
            masks = tuple(
                int(mask)
                for mask in evaluator.base_masks[winner["floater"]][
                    winner["base_index"]
                ]
            )
            maximizers.append(
                {
                    "floater": winner["floater"],
                    "masks": masks,
                    "utilities": tuple(winner["utilities"]),
                    "hall_insertable": winner["hall_insertable"],
                    "hall_margin": winner["best_hall_normalized_margin"],
                    "owners": owners(masks, winner["floater"], m),
                }
            )
        completing = [state for state in maximizers if state["hall_insertable"]]
        if not completing:
            raise AssertionError("existential maximum-threshold selector failed")
        swap_distances = floater_swap_distances(maximizers)
        improving_swap_distances = floater_swap_distances(
            maximizers, strictly_improving_margin=True
        )
        selected = []
        for blocked in failure["winners"]:
            blocked_owners = owners(
                tuple(blocked["masks"]), blocked["floater"], m
            )
            nearest = min(
                completing,
                key=lambda state: sum(
                    left != right
                    for left, right in zip(blocked_owners, state["owners"])
                ),
            )
            distance = sum(
                left != right
                for left, right in zip(blocked_owners, nearest["owners"])
            )
            is_minimum_slot_cycle, ownerwise_threshold_preserving = (
                minimum_slot_cycle(values, blocked_owners, nearest["owners"])
            )
            selected.append(
                {
                    "blocked_floater": blocked["floater"],
                    "blocked_masks": blocked["masks"],
                    "nearest_distance": distance,
                    "transition_kind": transition_kind(
                        blocked_owners, nearest["owners"]
                    ),
                    "minimum_slot_cycle": is_minimum_slot_cycle,
                    "ownerwise_threshold_preserving": (
                        ownerwise_threshold_preserving
                    ),
                    "floater_swap_path_length": swap_distances.get(
                        blocked_owners
                    ),
                    "strict_hall_margin_swap_path_length": (
                        improving_swap_distances.get(blocked_owners)
                    ),
                    "completing_floater": nearest["floater"],
                    "completing_masks": list(nearest["masks"]),
                }
            )
        records.append(
            {
                "source": failure["source"],
                "values_sha256": failure["values_sha256"],
                "maximum_threshold_state_count": len(maximizers),
                "hall_completing_maximum_threshold_state_count": len(completing),
                "blocked_minimum_tiebreak_state_count": len(selected),
                "maximum_nearest_distance": max(
                    record["nearest_distance"] for record in selected
                ),
                "selected_transitions": selected,
            }
        )
    distances = [
        transition["nearest_distance"]
        for record in records
        for transition in record["selected_transitions"]
    ]
    kinds = {}
    for record in records:
        for transition in record["selected_transitions"]:
            kind = transition["transition_kind"]
            kinds[kind] = kinds.get(kind, 0) + 1
    minimum_slot_cycle_count = sum(
        transition["minimum_slot_cycle"]
        for record in records
        for transition in record["selected_transitions"]
    )
    ownerwise_threshold_preserving_count = sum(
        transition["ownerwise_threshold_preserving"]
        for record in records
        for transition in record["selected_transitions"]
    )
    swap_path_lengths = [
        transition["floater_swap_path_length"]
        for record in records
        for transition in record["selected_transitions"]
        if transition["floater_swap_path_length"] is not None
    ]
    improving_swap_path_lengths = [
        transition["strict_hall_margin_swap_path_length"]
        for record in records
        for transition in record["selected_transitions"]
        if transition["strict_hall_margin_swap_path_length"] is not None
    ]
    artifact = {
        "schema": "threshold-plateau-completion-analysis-v1",
        "status": "EXISTENTIAL_SELECTOR_SURVIVES_SOURCE_FAILURES",
        "meaning": (
            "Exact owner-distance analysis from every blocked minimum-utility "
            "tie-break winner to a Hall-completing state on the same global "
            "maximum-threshold plateau. This is finite evidence, not a theorem."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "profile_count": len(records),
        "blocked_selected_state_count": len(distances),
        "maximum_nearest_distance": max(distances),
        "transition_kind_counts": kinds,
        "minimum_slot_cycle_count": minimum_slot_cycle_count,
        "ownerwise_threshold_preserving_count": (
            ownerwise_threshold_preserving_count
        ),
        "floater_swap_reachable_count": len(swap_path_lengths),
        "maximum_floater_swap_path_length": (
            max(swap_path_lengths) if swap_path_lengths else None
        ),
        "strict_hall_margin_swap_reachable_count": len(
            improving_swap_path_lengths
        ),
        "maximum_strict_hall_margin_swap_path_length": (
            max(improving_swap_path_lengths)
            if improving_swap_path_lengths
            else None
        ),
        "records": records,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
