#!/usr/bin/env python3
"""Classify the frozen lex-hard flower topology gate structurally."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
    from .run_flexible_later_owner_topology_cegar import classify_candidates
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import old_bundles
    from run_flexible_later_owner_topology_cegar import classify_candidates


PRIORITY = ("r", "q", "c", "s")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges(signature):
    result = []
    for entry in signature.split(";"):
        direction, count = entry.split(":")
        source, target = direction.split("->")
        result.extend((source, target) for _ in range(int(count)))
    return tuple(result)


def shape(signature):
    entries = edges(signature)
    multiplicity = Counter(tuple(sorted(edge)) for edge in entries)
    degree = Counter()
    for (left, right), count in multiplicity.items():
        degree[left] += count
        degree[right] += count
    vertex_count = len(degree)
    degrees = tuple(sorted(degree.values(), reverse=True))
    multiples = tuple(sorted(multiplicity.values(), reverse=True))
    if len(entries) == 1:
        return "edge1"
    if len(entries) == 2:
        return "parallel2" if vertex_count == 2 else "path2"
    if vertex_count == 2:
        return "parallel3"
    if vertex_count == 3:
        if multiples == (2, 1):
            return "parallel2+pendant"
        return "triangle" if degrees == (2, 2, 2) else "star3"
    return "star3" if degrees == (3, 1, 1, 1) else "path3"


def run(seed_path):
    seed = json.loads(seed_path.read_text())
    groups = classify_candidates(old_bundles(), "lex")
    records = []
    summary = defaultdict(lambda: {"class_count": 0, "allocation_count": 0})
    compatible_classes = 0
    compatible_allocations = 0
    for signature in seed["selected_topology_classes"]:
        entry_edges = edges(signature)
        incoming = {target for _, target in entry_edges}
        outgoing = {source for source, _ in entry_edges}
        earliest_incoming = next(
            (agent for agent in PRIORITY if agent in incoming), None
        )
        later_compatible = (
            "q" in incoming
            and not ("r" in outgoing and "r" not in incoming)
        )
        allocation_count = len(groups[signature])
        record = {
            "signature": signature,
            "shape": shape(signature),
            "scope": "charity" if "_" in incoming | outgoing else "owners",
            "earliest_incoming_owner": earliest_incoming,
            "later_transfer_structurally_compatible": later_compatible,
            "allocation_count": allocation_count,
        }
        records.append(record)
        key = (
            record["shape"],
            record["scope"],
            earliest_incoming or "none",
            "later-compatible" if later_compatible else "earlier-only",
        )
        summary[key]["class_count"] += 1
        summary[key]["allocation_count"] += allocation_count
        if later_compatible:
            compatible_classes += 1
            compatible_allocations += allocation_count
    assert len(records) == 37
    assert sum(record["allocation_count"] for record in records) == 2514
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-topology-shape-census-v1",
        "status": "CLASSIFIED",
        "topology_class_count": len(records),
        "candidate_allocation_count": sum(
            record["allocation_count"] for record in records
        ),
        "later_compatible_topology_class_count": compatible_classes,
        "later_compatible_allocation_count": compatible_allocations,
        "earlier_only_topology_class_count": len(records) - compatible_classes,
        "earlier_only_allocation_count": 2514 - compatible_allocations,
        "summary": [
            {
                "shape": key[0],
                "scope": key[1],
                "earliest_incoming_owner": key[2],
                "branch": key[3],
                **counts,
            }
            for key, counts in sorted(summary.items())
        ],
        "records": sorted(records, key=lambda record: record["signature"]),
        "claim_boundary": (
            "exact structural classification of the frozen bounded 37-class "
            "lex gate; later-compatible is necessary rather than sufficient "
            "for preserving r and improving q"
        ),
        "provenance": {
            "seed": str(seed_path.relative_to(root)),
            "seed_sha256": sha256(seed_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "later_compatible_topology_classes": result[
            "later_compatible_topology_class_count"
        ],
        "earlier_only_topology_classes": result[
            "earlier_only_topology_class_count"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
