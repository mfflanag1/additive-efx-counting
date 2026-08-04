#!/usr/bin/env python3
"""Extract nearest (Theta, utility)-improving escapes from champion counterexamples."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import (
        absorption_signature,
        eligible,
        tables,
        theta,
    )
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import (
        absorption_signature,
        eligible,
        tables,
        theta,
    )


SCHEMA = "unique-defect-champion-local-escape-audit-v1"


def labels(masks, charity, m):
    result = []
    for good in range(m):
        if charity & (1 << good):
            result.append(len(masks))
            continue
        result.append(next(owner for owner, mask in enumerate(masks) if mask & (1 << good)))
    return tuple(result)


def transfer_components(old_labels, new_labels):
    parent = list(range(max(old_labels + new_labels) + 1))

    def find(slot):
        while parent[slot] != slot:
            parent[slot] = parent[parent[slot]]
            slot = parent[slot]
        return slot

    def union(left, right):
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    changed = []
    for good, (old, new) in enumerate(zip(old_labels, new_labels)):
        if old != new:
            changed.append(good)
            union(old, new)
    components = {}
    for good in changed:
        root = find(old_labels[good])
        component = components.setdefault(root, {"goods": [], "slots": set()})
        component["goods"].append(good)
        component["slots"].update((old_labels[good], new_labels[good]))
    return [
        {"goods": value["goods"], "slots": sorted(value["slots"])}
        for value in components.values()
    ]


def enumerate_states(values):
    n = len(values)
    m = len(values[0])
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    for floater in range(m):
        allocated = [good for good in range(m) if good != floater]
        for owners in itertools.product(range(n), repeat=len(allocated)):
            masks = [0] * n
            for good, owner in zip(allocated, owners):
                masks[owner] |= 1 << good
            masks = tuple(masks)
            charity = 1 << floater
            if all(masks) and eligible(masks, charity, totals, thresholds):
                utilities = tuple(totals[owner][masks[owner]] for owner in range(n))
                yield {
                    "masks": masks,
                    "charity": charity,
                    "theta": theta(masks, totals, thresholds, row_totals),
                    "utilities": utilities,
                }


def audit_record(path):
    document = json.loads(path.read_text())
    values = tuple(tuple(row) for row in document["values"])
    n = len(values)
    m = len(values[0])
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    base_masks = tuple(document["masks"])
    base_charity = 1 << document["floater"]
    base_theta = theta(base_masks, totals, thresholds, row_totals)
    base_utilities = tuple(
        totals[owner][base_masks[owner]] for owner in range(n)
    )
    base_key = (base_theta, base_utilities)
    base_labels = labels(base_masks, base_charity, m)
    improving = []
    for state in enumerate_states(values):
        if (state["theta"], state["utilities"]) <= base_key:
            continue
        state_labels = labels(state["masks"], state["charity"], m)
        distance = sum(
            old != new for old, new in zip(base_labels, state_labels)
        )
        improving.append((distance, state, state_labels))
    if not improving:
        raise AssertionError("counterexample state has no extremal improvement")
    minimum_distance = min(item[0] for item in improving)
    nearest = [item for item in improving if item[0] == minimum_distance]
    distance, state, state_labels = max(
        nearest,
        key=lambda item: (item[1]["theta"], item[1]["utilities"]),
    )
    signature, witness = absorption_signature(
        state["masks"],
        state["charity"],
        totals,
        thresholds,
        row_totals,
    )
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "base_theta": str(base_theta),
        "base_utilities": list(base_utilities),
        "improving_state_count": len(improving),
        "minimum_label_distance": minimum_distance,
        "nearest_improving_state_count": len(nearest),
        "selected_escape": {
            "masks": list(state["masks"]),
            "charity_mask": state["charity"],
            "theta_change": str(state["theta"] - base_theta),
            "utility_changes": [
                after - before
                for before, after in zip(base_utilities, state["utilities"])
            ],
            "transfer_components": transfer_components(base_labels, state_labels),
            "absorption_signature": [str(value) for value in signature],
            "absorption_witness": witness,
        },
    }


def run(paths, output):
    if output.exists():
        raise ValueError("output must be new")
    result = {
        "schema": SCHEMA,
        "status": "EXACT_ESCAPES_EXTRACTED",
        "records": [audit_record(path) for path in paths],
        "claim_boundary": (
            "These are exact escape witnesses for the listed finite profiles. They "
            "do not prove the global extremal alternative or EFX existence."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.paths, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
