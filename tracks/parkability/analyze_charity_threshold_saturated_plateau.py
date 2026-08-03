#!/usr/bin/env python3
"""Audit threshold plateaus under charity and owner-Pareto exchanges."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_charity_threshold_plateau import neighbors as charity_neighbors
    from .scan_charity_threshold_absorption import (
        absorption_margin,
        load_profiles,
        theta_maximizers,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_charity_threshold_plateau import neighbors as charity_neighbors
    from scan_charity_threshold_absorption import (
        absorption_margin,
        load_profiles,
        theta_maximizers,
    )


SCHEMA = "charity-threshold-saturated-plateau-audit-v1"


def goods(mask, m):
    return tuple(good for good in range(m) if mask & (1 << good))


def owner_swap_neighbors(state, states, values):
    masks, charity = state
    m = len(values[0])
    for left in range(len(masks)):
        for right in range(left + 1, len(masks)):
            for left_good in goods(masks[left], m):
                for right_good in goods(masks[right], m):
                    if values[left][right_good] < values[left][left_good]:
                        continue
                    if values[right][left_good] < values[right][right_good]:
                        continue
                    candidate_masks = list(masks)
                    candidate_masks[left] ^= (1 << left_good) | (1 << right_good)
                    candidate_masks[right] ^= (1 << left_good) | (1 << right_good)
                    candidate = (tuple(candidate_masks), charity)
                    if candidate in states:
                        yield candidate


def reverse_reachability(states, absorbing, edge_function):
    reverse = {state: [] for state in states}
    edge_count = 0
    for state in states:
        for target in set(edge_function(state)):
            reverse[target].append(state)
            edge_count += 1
    distances = {state: 0 for state in absorbing}
    queue = deque(absorbing)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source in distances:
                continue
            distances[source] = distances[target] + 1
            queue.append(source)
    return distances, edge_count


def analyze(values, charity_size):
    landscape = theta_maximizers(values, charity_size)
    maximizers = landscape["maximizers"]
    if not maximizers:
        return {"status": "NO_EFX_WITH_CHARITY_STATE"}
    states = set(maximizers)
    margins = {
        state: absorption_margin(
            *state,
            landscape["totals"],
            landscape["thresholds"],
            landscape["row_totals"],
        )[0]
        for state in states
    }
    absorbing = {state for state, margin in margins.items() if margin >= 0}

    def charity_edges(state):
        return charity_neighbors(state, states, values)

    def owner_edges(state):
        return owner_swap_neighbors(state, states, values)

    def combined_edges(state):
        yield from charity_edges(state)
        yield from owner_edges(state)

    charity_distances, charity_edge_count = reverse_reachability(
        states, absorbing, charity_edges
    )
    combined_distances, combined_edge_count = reverse_reachability(
        states, absorbing, combined_edges
    )
    _, owner_edge_count = reverse_reachability(states, absorbing, owner_edges)
    blocked = states - absorbing
    charity_unreachable = blocked - charity_distances.keys()
    combined_unreachable = blocked - combined_distances.keys()
    rescued = charity_unreachable - combined_unreachable
    return {
        "status": (
            "SATURATED_PLATEAU_REACHES_ABSORPTION"
            if not combined_unreachable
            else "SATURATED_UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
        ),
        "eligible_state_count": landscape["eligible_state_count"],
        "theta_maximizer_count": len(states),
        "absorbing_maximizer_count": len(absorbing),
        "blocked_maximizer_count": len(blocked),
        "charity_minimum_swap_edge_count": charity_edge_count,
        "owner_pareto_swap_edge_count": owner_edge_count,
        "combined_edge_count": combined_edge_count,
        "charity_only_unreachable_count": len(charity_unreachable),
        "rescued_by_owner_swap_count": len(rescued),
        "combined_unreachable_count": len(combined_unreachable),
        "maximum_combined_path_length": max(
            (combined_distances[state] for state in blocked if state in combined_distances),
            default=None,
        ),
        "combined_unreachable_states": [
            {
                "masks": list(masks),
                "charity_mask": charity,
                "margin": str(margins[(masks, charity)]),
            }
            for masks, charity in sorted(combined_unreachable)
        ],
    }


def run(source, output, charity_size):
    if output.exists():
        raise ValueError("output must be new")
    records = []
    for label, values in load_profiles(source):
        record = {
            "source": label,
            "values": [list(row) for row in values],
            **analyze(values, charity_size),
        }
        records.append(record)
        print(f"{label}: {record['status']}", flush=True)
    failures = [
        record
        for record in records
        if record["status"] == "SATURATED_UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
    ]
    result = {
        "schema": SCHEMA,
        "status": (
            "SATURATED_UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
            if failures
            else "SATURATED_PLATEAU_REACHABILITY_SURVIVES"
        ),
        "meaning": (
            "Exact reachability among global normalized-threshold maximizers "
            "using eligible charity/minimum swaps and mutually owner-improving "
            "two-good swaps."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "charity_size": charity_size,
        "profile_count": len(records),
        "records": records,
        "claim_boundary": (
            "Finite plateau reachability does not prove the universal "
            "absorption-gradient lemma. Owner cycles of length above two are "
            "not included."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--charity-size", type=int, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output, args.charity_size)
    print(json.dumps({key: result[key] for key in ("status", "profile_count")}, indent=2))


if __name__ == "__main__":
    main()
