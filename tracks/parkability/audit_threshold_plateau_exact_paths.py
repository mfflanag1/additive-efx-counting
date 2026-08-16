#!/usr/bin/env python3
"""Audit threshold-plateau completion paths with exact Hall margins."""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_threshold_plateau_completion import load_values, owners
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from analyze_threshold_plateau_completion import load_values, owners
    from fast_count import FastParkability


SCHEMA = "threshold-plateau-exact-hall-path-audit-v1"


def mask_value(values, observer: int, mask: int) -> int:
    return sum(
        values[observer][good]
        for good in range(len(values[observer]))
        if mask & (1 << good)
    )


def mask_threshold(values, observer: int, mask: int) -> int:
    entries = [
        values[observer][good]
        for good in range(len(values[observer]))
        if mask & (1 << good)
    ]
    if not entries:
        return 0
    return sum(entries) - min(entries)


def complete_masks(state: dict, host: int) -> tuple[int, ...]:
    masks = list(state["masks"])
    masks[host] |= 1 << state["floater"]
    return tuple(masks)


def feasibility_graph(values, masks: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    n = len(values)
    totals = [
        [mask_value(values, observer, mask) for mask in masks]
        for observer in range(n)
    ]
    thresholds = [
        [mask_threshold(values, observer, mask) for mask in masks]
        for observer in range(n)
    ]
    return tuple(
        tuple(
            bundle
            for bundle in range(n)
            if all(
                totals[observer][bundle] >= thresholds[observer][target]
                for target in range(n)
                if target != bundle
            )
        )
        for observer in range(n)
    )


def margin_graph(
    values,
    masks: tuple[int, ...],
    cutoff: Fraction,
    *,
    strict: bool,
) -> tuple[tuple[int, ...], ...]:
    n = len(values)
    row_totals = tuple(sum(row) for row in values)
    totals = [
        [mask_value(values, observer, mask) for mask in masks]
        for observer in range(n)
    ]
    thresholds = [
        [mask_threshold(values, observer, mask) for mask in masks]
        for observer in range(n)
    ]
    return tuple(
        tuple(
            bundle
            for bundle in range(n)
            if (
                Fraction(
                    totals[observer][bundle]
                    - max(
                        thresholds[observer][target]
                        for target in range(n)
                        if target != bundle
                    ),
                    row_totals[observer],
                )
                > cutoff
                if strict
                else Fraction(
                    totals[observer][bundle]
                    - max(
                        thresholds[observer][target]
                        for target in range(n)
                        if target != bundle
                    ),
                    row_totals[observer],
                )
                >= cutoff
            )
        )
        for observer in range(n)
    )


def hall_witnesses(graph: tuple[tuple[int, ...], ...]) -> tuple[dict, ...]:
    witnesses = []
    n = len(graph)
    for size in range(1, n + 1):
        for agents in itertools.combinations(range(n), size):
            neighborhood = sorted(
                {bundle for agent in agents for bundle in graph[agent]}
            )
            if len(neighborhood) < size:
                witnesses.append(
                    {
                        "agents": list(agents),
                        "neighbors": neighborhood,
                        "deficiency": size - len(neighborhood),
                    }
                )
    return tuple(witnesses)


def exact_best_hall_margin(values, state: dict):
    n = len(values)
    row_totals = tuple(sum(row) for row in values)
    best = None
    best_host = None
    best_permutation = None
    best_bottlenecks = None
    for host in range(n):
        masks = complete_masks(state, host)
        totals = [
            [mask_value(values, observer, mask) for mask in masks]
            for observer in range(n)
        ]
        thresholds = [
            [mask_threshold(values, observer, mask) for mask in masks]
            for observer in range(n)
        ]
        for permutation in itertools.permutations(range(n)):
            observer_records = []
            for observer in range(n):
                assigned = permutation[observer]
                required = max(
                    thresholds[observer][target]
                    for target in range(n)
                    if target != assigned
                )
                slack = Fraction(
                    totals[observer][assigned] - required,
                    row_totals[observer],
                )
                observer_records.append(
                    {
                        "observer": observer,
                        "assigned_bundle": assigned,
                        "worst_targets": [
                            target
                            for target in range(n)
                            if target != assigned
                            and thresholds[observer][target] == required
                        ],
                        "slack": slack,
                    }
                )
            margin = min(record["slack"] for record in observer_records)
            if best is None or margin > best:
                best = margin
                best_host = host
                best_permutation = permutation
                best_bottlenecks = [
                    record for record in observer_records if record["slack"] == margin
                ]
    assert (
        best is not None
        and best_host is not None
        and best_permutation is not None
        and best_bottlenecks is not None
    )
    return best, best_host, best_permutation, best_bottlenecks


def state_record(evaluator: FastParkability, winner: dict, m: int) -> dict:
    masks = tuple(
        int(mask)
        for mask in evaluator.base_masks[winner["floater"]][winner["base_index"]]
    )
    return {
        "floater": winner["floater"],
        "masks": masks,
        "owners": owners(masks, winner["floater"], m),
        "hall_insertable": winner["hall_insertable"],
    }


def exact_paths(
    values,
    states: list[dict],
    *,
    minimum_slots_only: bool = False,
) -> tuple[dict, dict, dict]:
    by_owners = {state["owners"]: state for state in states}
    margins = {}
    best_data = {}

    def margin(owner_vector):
        if owner_vector not in margins:
            record = by_owners[owner_vector]
            value, host, permutation, bottlenecks = exact_best_hall_margin(
                values, record
            )
            margins[owner_vector] = value
            best_data[owner_vector] = (host, permutation, bottlenecks)
        return margins[owner_vector]

    distances = {}
    successor = {}
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
            if minimum_slots_only:
                slot_step = minimum_slot_step(values, key, current)
                if not (
                    slot_step["outgoing_is_owner_minimum"]
                    and slot_step["incoming_is_new_owner_minimum"]
                ):
                    continue
            if margin(key) >= margin(current):
                continue
            distances[key] = distances[current] + 1
            successor[key] = current
            queue.append(key)
    return distances, successor, {key: (margins.get(key), best_data.get(key)) for key in by_owners}


def minimum_slot_step(values, left: tuple[int, ...], right: tuple[int, ...]) -> dict:
    old_floater = left.index(-1)
    new_floater = right.index(-1)
    owner = left[new_floater]
    if owner < 0 or right[old_floater] != owner:
        raise AssertionError("path edge is not a floater swap")
    old_bundle = [good for good, label in enumerate(left) if label == owner]
    new_bundle = [good for good, label in enumerate(right) if label == owner]
    outgoing_is_minimum = values[owner][new_floater] == min(
        values[owner][good] for good in old_bundle
    )
    incoming_is_minimum = values[owner][old_floater] == min(
        values[owner][good] for good in new_bundle
    )
    return {
        "owner": owner,
        "incoming_old_floater": old_floater,
        "outgoing_new_floater": new_floater,
        "outgoing_is_owner_minimum": outgoing_is_minimum,
        "incoming_is_new_owner_minimum": incoming_is_minimum,
    }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    profile_records = []
    relation_counts = Counter()
    total_selected = 0
    reached = 0
    total_maximum_states = 0
    total_blocked_maximum_states = 0
    reachable_blocked_maximum_states = 0
    minimum_slot_reachable_blocked_maximum_states = 0
    fixed_token_orbit_reachable_blocked_maximum_states = 0
    maximum_minimum_slot_path_length = 0
    transition_count = 0
    unique_transition_records = {}
    all_blocked_transition_count = 0
    all_blocked_minimum_slot_transition_count = 0
    all_blocked_unique_transitions = set()
    path_length_counts = Counter()

    for failure in document["direct_hall_failures"]:
        values = load_values(failure)
        n = len(values)
        m = len(values[0])
        evaluator = FastParkability(n, m)
        landscape = evaluator.partial_linear_potential_landscape(
            values,
            potential="normalized_threshold",
        )
        states = [state_record(evaluator, winner, m) for winner in landscape["maximizers"]]
        total_maximum_states += len(states)
        blocked_states = [state for state in states if not state["hall_insertable"]]
        total_blocked_maximum_states += len(blocked_states)
        by_owners = {state["owners"]: state for state in states}
        distances, successor, margin_data = exact_paths(values, states)
        minimum_slot_distances, minimum_slot_successor, _minimum_slot_data = (
            exact_paths(values, states, minimum_slots_only=True)
        )
        reachable_blocked = [
            state for state in blocked_states if state["owners"] in distances
        ]
        reachable_blocked_maximum_states += len(reachable_blocked)
        minimum_slot_reachable_blocked_maximum_states += sum(
            state["owners"] in minimum_slot_distances
            for state in blocked_states
        )
        for blocked_state in blocked_states:
            current = blocked_state["owners"]
            if current not in minimum_slot_distances:
                continue
            maximum_minimum_slot_path_length = max(
                maximum_minimum_slot_path_length,
                minimum_slot_distances[current],
            )
            released_by_owner = {}
            while current in minimum_slot_successor:
                following = minimum_slot_successor[current]
                slot_step = minimum_slot_step(values, current, following)
                released_by_owner.setdefault(slot_step["owner"], set()).add(
                    slot_step["outgoing_new_floater"]
                )
                current = following
            fixed_token_orbit_reachable_blocked_maximum_states += int(
                all(len(goods) <= 1 for goods in released_by_owner.values())
            )
        for blocked_state in reachable_blocked:
            current = blocked_state["owners"]
            while current in successor:
                following = successor[current]
                all_blocked_transition_count += 1
                all_blocked_unique_transitions.add(
                    (failure["values_sha256"], current, following)
                )
                slot_step = minimum_slot_step(values, current, following)
                all_blocked_minimum_slot_transition_count += int(
                    slot_step["outgoing_is_owner_minimum"]
                    and slot_step["incoming_is_new_owner_minimum"]
                )
                current = following
        selected_paths = []
        for blocked in failure["winners"]:
            total_selected += 1
            start = owners(tuple(blocked["masks"]), blocked["floater"], m)
            if start not in distances:
                continue
            reached += 1
            path = [start]
            while path[-1] in successor:
                path.append(successor[path[-1]])
            path_length_counts[len(path) - 1] += 1
            steps = []
            for left, right in zip(path, path[1:]):
                transition_count += 1
                left_margin, (
                    left_host,
                    left_permutation,
                    left_bottlenecks,
                ) = margin_data[left]
                right_margin, (
                    right_host,
                    right_permutation,
                    right_bottlenecks,
                ) = margin_data[right]
                if left_margin is None or right_margin is None:
                    raise AssertionError("missing exact path margin")
                step = minimum_slot_step(values, left, right)
                if right_host == step["owner"]:
                    raise AssertionError(
                        "strict improvement cannot reinsert the new floater "
                        "into its source"
                    )
                graph = feasibility_graph(values, complete_masks(by_owners[left], left_host))
                strict_margin_graph = margin_graph(
                    values,
                    complete_masks(by_owners[left], left_host),
                    left_margin,
                    strict=True,
                )
                weak_margin_graph = margin_graph(
                    values,
                    complete_masks(by_owners[left], left_host),
                    left_margin,
                    strict=False,
                )
                right_graph = feasibility_graph(
                    values,
                    complete_masks(by_owners[right], right_host),
                )
                witnesses = hall_witnesses(graph)
                critical_witnesses = hall_witnesses(strict_margin_graph)
                if not critical_witnesses:
                    raise AssertionError(
                        "strict-above-margin graph unexpectedly has a perfect matching"
                    )
                if hall_witnesses(weak_margin_graph):
                    raise AssertionError(
                        "at-margin graph unexpectedly lacks the selected matching"
                    )
                minimum_witness_size = min(len(item["agents"]) for item in witnesses)
                minimum_witnesses = tuple(
                    item
                    for item in witnesses
                    if len(item["agents"]) == minimum_witness_size
                )
                canonical = minimum_witnesses[0]
                minimum_critical_witness_size = min(
                    len(item["agents"]) for item in critical_witnesses
                )
                minimum_critical_witnesses = tuple(
                    item
                    for item in critical_witnesses
                    if len(item["agents"]) == minimum_critical_witness_size
                )
                canonical_critical = minimum_critical_witnesses[0]
                full_cut_two_source_candidates = []
                full_cut_two_source_state = (
                    minimum_critical_witness_size == n
                    and len(canonical_critical["neighbors"]) == n - 1
                )
                if full_cut_two_source_state:
                    missing_bundle = next(
                        bundle
                        for bundle in range(n)
                        if bundle not in canonical_critical["neighbors"]
                    )
                    old_floater = left.index(-1)
                    for candidate_source in sorted({left_host, missing_bundle}):
                        source_goods = [
                            good
                            for good, owner in enumerate(left)
                            if owner == candidate_source
                        ]
                        if not source_goods:
                            continue
                        owner_minimum = min(
                            values[candidate_source][good]
                            for good in source_goods
                        )
                        for candidate_good in source_goods:
                            if (
                                values[candidate_source][candidate_good]
                                != owner_minimum
                            ):
                                continue
                            candidate = list(left)
                            candidate[old_floater] = candidate_source
                            candidate[candidate_good] = -1
                            candidate_key = tuple(candidate)
                            if candidate_key not in by_owners:
                                continue
                            candidate_margin, _candidate_best = margin_data[
                                candidate_key
                            ]
                            if candidate_margin is None:
                                candidate_margin = exact_best_hall_margin(
                                    values,
                                    by_owners[candidate_key],
                                )[0]
                            full_cut_two_source_candidates.append(
                                {
                                    "source": candidate_source,
                                    "outgoing_good": candidate_good,
                                    "margin": fraction_text(candidate_margin),
                                    "strictly_improves": (
                                        candidate_margin > left_margin
                                    ),
                                }
                            )
                step.update(
                    {
                        "from_margin": fraction_text(left_margin),
                        "to_margin": fraction_text(right_margin),
                        "best_host": left_host,
                        "best_permutation": list(left_permutation),
                        "best_bottlenecks": [
                            {
                                **record,
                                "slack": fraction_text(record["slack"]),
                            }
                            for record in left_bottlenecks
                        ],
                        "best_host_graph": [list(row) for row in graph],
                        "canonical_hall_witness": canonical,
                        "strict_margin_graph": [
                            list(row) for row in strict_margin_graph
                        ],
                        "canonical_critical_hall_witness": canonical_critical,
                        "full_cut_two_source_candidates": (
                            full_cut_two_source_candidates
                        ),
                        "successor_best_host": right_host,
                        "successor_best_permutation": list(right_permutation),
                        "successor_best_bottlenecks": [
                            {
                                **record,
                                "slack": fraction_text(record["slack"]),
                            }
                            for record in right_bottlenecks
                        ],
                        "successor_best_host_graph": [
                            list(row) for row in right_graph
                        ],
                    }
                )
                relation_counts["outgoing_owner_minimum"] += int(
                    step["outgoing_is_owner_minimum"]
                )
                relation_counts["incoming_new_owner_minimum"] += int(
                    step["incoming_is_new_owner_minimum"]
                )
                relation_counts["owner_in_canonical_deficient_set"] += int(
                    step["owner"] in canonical["agents"]
                )
                relation_counts["owner_in_some_minimum_deficient_set"] += int(
                    any(step["owner"] in item["agents"] for item in minimum_witnesses)
                )
                relation_counts["owner_in_some_deficient_set"] += int(
                    any(step["owner"] in item["agents"] for item in witnesses)
                )
                relation_counts["owner_in_some_deficient_neighborhood"] += int(
                        any(step["owner"] in item["neighbors"] for item in witnesses)
                )
                relation_counts["owner_in_canonical_critical_deficient_set"] += int(
                    step["owner"] in canonical_critical["agents"]
                )
                relation_counts[
                    "owner_in_some_minimum_critical_deficient_set"
                ] += int(
                    any(
                        step["owner"] in item["agents"]
                        for item in minimum_critical_witnesses
                    )
                )
                relation_counts["owner_in_some_critical_deficient_set"] += int(
                    any(
                        step["owner"] in item["agents"]
                        for item in critical_witnesses
                    )
                )
                relation_counts[
                    "owner_in_some_critical_deficient_neighborhood"
                ] += int(
                    any(
                        step["owner"] in item["neighbors"]
                        for item in critical_witnesses
                    )
                )
                relation_counts["owner_equals_best_host"] += int(
                    step["owner"] == left_host
                )
                relation_counts["owner_is_bottleneck_observer"] += int(
                    any(
                        step["owner"] == record["observer"]
                        for record in left_bottlenecks
                    )
                )
                relation_counts["owner_is_bottleneck_assigned_bundle"] += int(
                    any(
                        step["owner"] == record["assigned_bundle"]
                        for record in left_bottlenecks
                    )
                )
                relation_counts["owner_is_bottleneck_worst_target"] += int(
                    any(
                        step["owner"] in record["worst_targets"]
                        for record in left_bottlenecks
                    )
                )
                relation_counts["same_best_permutation"] += int(
                    left_permutation == right_permutation
                )
                relation_counts["successor_host_equals_source"] += int(
                    right_host == step["owner"]
                )
                if step["owner"] == left_host:
                    move_type = "one_good_transfer"
                elif right_host == left_host:
                    move_type = "two_bundle_swap"
                else:
                    move_type = "three_bundle_augmenting_path"
                relation_counts[f"completion_move_{move_type}"] += 1
                relation_counts[f"canonical_witness_size_{minimum_witness_size}"] += 1
                relation_counts[
                    f"canonical_critical_witness_size_{minimum_critical_witness_size}"
                ] += 1
                if full_cut_two_source_state:
                    relation_counts["full_cut_two_source_state"] += 1
                    relation_counts[
                        "full_cut_two_source_strict_gradient"
                    ] += int(
                        any(
                            candidate["strictly_improves"]
                            for candidate in full_cut_two_source_candidates
                        )
                    )
                edge_key = (failure["values_sha256"], left, right)
                unique_transition_records.setdefault(
                    edge_key,
                    {
                        "source": failure["source"],
                        "values_sha256": failure["values_sha256"],
                        "from_owners": list(left),
                        "to_owners": list(right),
                        **step,
                    },
                )
                steps.append(step)
            selected_paths.append(
                {
                    "start_owners": list(start),
                    "path_length": len(path) - 1,
                    "steps": steps,
                }
            )
        profile_records.append(
            {
                "source": failure["source"],
                "values_sha256": failure["values_sha256"],
                "maximum_threshold_state_count": len(states),
                "blocked_maximum_threshold_state_count": len(blocked_states),
                "exact_strict_path_blocked_maximum_state_count": len(
                    reachable_blocked
                ),
                "maximum_all_blocked_exact_strict_path_length": max(
                    (distances[state["owners"]] for state in reachable_blocked),
                    default=None,
                ),
                "exact_strict_path_selected_state_count": len(selected_paths),
                "maximum_exact_strict_path_length": max(
                    (record["path_length"] for record in selected_paths),
                    default=None,
                ),
            }
        )

    artifact = {
        "schema": SCHEMA,
        "status": (
            "EXACT_STRICT_PATHS_VERIFIED"
            if reached == total_selected
            else "EXACT_STRICT_PATH_FAILURE"
        ),
        "meaning": (
            "Exact rational audit of strictly Hall-margin-increasing floater-swap "
            "paths inside global normalized-threshold plateaus. Finite evidence, "
            "not a universal conversion theorem."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "profile_count": len(profile_records),
        "selected_state_count": total_selected,
        "exact_strict_path_selected_state_count": reached,
        "maximum_threshold_state_count": total_maximum_states,
        "blocked_maximum_threshold_state_count": total_blocked_maximum_states,
        "exact_strict_path_blocked_maximum_state_count": (
            reachable_blocked_maximum_states
        ),
        "exact_strict_minimum_slot_path_blocked_maximum_state_count": (
            minimum_slot_reachable_blocked_maximum_states
        ),
        "fixed_token_orbit_path_blocked_maximum_state_count": (
            fixed_token_orbit_reachable_blocked_maximum_states
        ),
        "maximum_exact_strict_minimum_slot_path_length": (
            maximum_minimum_slot_path_length
        ),
        "transition_occurrence_count": transition_count,
        "unique_transition_count": len(unique_transition_records),
        "all_blocked_transition_occurrence_count": all_blocked_transition_count,
        "all_blocked_unique_transition_count": len(
            all_blocked_unique_transitions
        ),
        "all_blocked_minimum_slot_transition_occurrence_count": (
            all_blocked_minimum_slot_transition_count
        ),
        "exact_strict_path_length_counts": {
            str(length): count for length, count in sorted(path_length_counts.items())
        },
        "relation_counts": dict(sorted(relation_counts.items())),
        "profiles": profile_records,
        "unique_transitions": list(unique_transition_records.values()),
    }
    if artifact["status"] != "EXACT_STRICT_PATHS_VERIFIED":
        raise AssertionError("floating Hall-margin paths did not survive exact audit")
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.source, args.output)
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in (
                    "schema",
                    "status",
                    "profile_count",
                    "selected_state_count",
                    "exact_strict_path_selected_state_count",
                    "maximum_threshold_state_count",
                    "blocked_maximum_threshold_state_count",
                    "exact_strict_path_blocked_maximum_state_count",
                    "exact_strict_minimum_slot_path_blocked_maximum_state_count",
                    "fixed_token_orbit_path_blocked_maximum_state_count",
                    "maximum_exact_strict_minimum_slot_path_length",
                    "transition_occurrence_count",
                    "unique_transition_count",
                    "all_blocked_transition_occurrence_count",
                    "all_blocked_unique_transition_count",
                    "all_blocked_minimum_slot_transition_occurrence_count",
                    "exact_strict_path_length_counts",
                    "relation_counts",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
