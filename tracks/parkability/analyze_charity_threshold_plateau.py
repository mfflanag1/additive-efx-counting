#!/usr/bin/env python3
"""Audit absorption reachability inside a fixed-charity threshold plateau."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import (
        absorption_margin,
        load_profiles,
        theta_maximizers,
    )
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import (
        absorption_margin,
        load_profiles,
        theta_maximizers,
    )


SCHEMA = "charity-threshold-plateau-audit-v1"


def owner_minima(mask, owner, values):
    minimum = min(
        values[owner][good]
        for good in range(len(values[owner]))
        if mask & (1 << good)
    )
    return tuple(
        good
        for good in range(len(values[owner]))
        if mask & (1 << good) and values[owner][good] == minimum
    )


def neighbors(state, states, values):
    masks, charity = state
    n = len(masks)
    for incoming in range(len(values[0])):
        if not charity & (1 << incoming):
            continue
        for owner in range(n):
            for outgoing in owner_minima(masks[owner], owner, values):
                candidate_masks = list(masks)
                candidate_masks[owner] = (
                    candidate_masks[owner] & ~(1 << outgoing)
                ) | (1 << incoming)
                candidate_charity = (charity & ~(1 << incoming)) | (1 << outgoing)
                candidate = (tuple(candidate_masks), candidate_charity)
                if candidate in states:
                    yield candidate


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
    reverse = {state: [] for state in states}
    edge_count = 0
    strict_edge_count = 0
    for state in states:
        for target in set(neighbors(state, states, values)):
            reverse[target].append(state)
            edge_count += 1
            strict_edge_count += margins[target] > margins[state]
    distances = {state: 0 for state in absorbing}
    queue = deque(absorbing)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source in distances:
                continue
            distances[source] = distances[target] + 1
            queue.append(source)
    blocked = states - absorbing
    unreachable = blocked - distances.keys()
    return {
        "status": (
            "ALL_BLOCKED_MAXIMA_REACH_ABSORPTION"
            if not unreachable
            else "UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
        ),
        "eligible_state_count": landscape["eligible_state_count"],
        "theta_maximizer_count": len(states),
        "absorbing_maximizer_count": len(absorbing),
        "blocked_maximizer_count": len(blocked),
        "reachable_blocked_maximizer_count": len(blocked) - len(unreachable),
        "maximum_path_length": max(
            (distances[state] for state in blocked if state in distances),
            default=None,
        ),
        "minimum_swap_edge_count": edge_count,
        "strict_margin_edge_count": strict_edge_count,
        "unreachable_states": [
            {"masks": list(masks), "charity_mask": charity, "margin": str(margins[(masks, charity)])}
            for masks, charity in sorted(unreachable)
        ],
    }


def run(source, output, charity_size):
    if output.exists():
        raise ValueError("output must be new")
    records = []
    for label, values in load_profiles(source):
        records.append(
            {
                "source": label,
                "values": [list(row) for row in values],
                **analyze(values, charity_size),
            }
        )
    failures = [
        record
        for record in records
        if record["status"] == "UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
    ]
    result = {
        "schema": SCHEMA,
        "status": (
            "UNREACHABLE_BLOCKED_MAXIMUM_FOUND"
            if failures
            else "PLATEAU_REACHABILITY_SURVIVES"
        ),
        "meaning": (
            "Exact reachability through eligible owner-minimum/charity swaps "
            "inside each global normalized-threshold plateau."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "charity_size": charity_size,
        "profile_count": len(records),
        "records": records,
        "claim_boundary": (
            "Finite plateau reachability is not a universal absorption theorem."
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
