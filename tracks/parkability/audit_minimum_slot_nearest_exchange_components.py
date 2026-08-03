#!/usr/bin/env python3
"""Audit transfer-component topology of nearest higher-state CEGAR cuts."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import owner_assignment
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import owner_assignment


SCHEMA = "minimum-slot-nearest-exchange-component-audit-v1"
BASE_STATE = {"floater": 8, "masks": (3, 12, 48, 192)}


def transfer_components(left, right):
    edges = [
        (source, destination, good)
        for good, (source, destination) in enumerate(zip(left, right))
        if source != destination
    ]
    remaining = {vertex for edge in edges for vertex in edge[:2]}
    components = []
    while remaining:
        root = remaining.pop()
        vertices = {root}
        frontier = [root]
        while frontier:
            vertex = frontier.pop()
            adjacent = {
                endpoint
                for source, destination, _good in edges
                if source == vertex or destination == vertex
                for endpoint in (source, destination)
            }
            new = adjacent & remaining
            remaining -= new
            vertices |= new
            frontier.extend(new)
        components.append(
            {
                "vertices": sorted(vertices),
                "edges": [
                    {"source": source, "destination": destination, "good": good}
                    for source, destination, good in edges
                    if source in vertices
                ],
            }
        )
    return components


def run(source, output):
    document = json.loads(source.read_text())
    base_assignment = owner_assignment(BASE_STATE)
    records = []
    histogram = Counter()
    for cut in document["global_cuts"]:
        state = {
            "floater": int(cut["floater"]),
            "masks": tuple(int(mask) for mask in cut["masks"]),
        }
        assignment = owner_assignment(state)
        components = transfer_components(base_assignment, assignment)
        distance = sum(
            left != right
            for left, right in zip(base_assignment, assignment)
        )
        signature = (
            distance,
            len(components),
            tuple(sorted(len(component["vertices"]) for component in components)),
        )
        histogram[signature] += 1
        records.append(
            {
                "floater": state["floater"],
                "masks": list(state["masks"]),
                "owner_distance": distance,
                "component_count": len(components),
                "components": components,
            }
        )
    all_connected = all(record["component_count"] == 1 for record in records)
    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_NEAREST_WITNESSES_CONNECTED"
            if all_connected
            else "DISCONNECTED_NEAREST_WITNESS_FOUND"
        ),
        "meaning": (
            "Exact transfer-graph topology audit of every stored nearest "
            "higher-threshold CEGAR witness."
        ),
        "claim_boundary": (
            "Connectivity is a fact about this finite witness pool, not a "
            "general connected-improvement theorem."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "witness_count": len(records),
        "all_witnesses_connected": all_connected,
        "distance_histogram": {
            str(distance): sum(
                record["owner_distance"] == distance for record in records
            )
            for distance in sorted({record["owner_distance"] for record in records})
        },
        "topology_histogram": [
            {
                "owner_distance": signature[0],
                "component_count": signature[1],
                "component_vertex_sizes": list(signature[2]),
                "count": count,
            }
            for signature, count in sorted(histogram.items())
        ],
        "records": records,
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
