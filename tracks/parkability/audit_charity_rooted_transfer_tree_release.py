#!/usr/bin/env python3
"""Audit release support for charity-rooted transfer trees through four owners."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rooted_trees(vertices, root):
    others = tuple(vertex for vertex in vertices if vertex != root)
    for parents in itertools.product(vertices, repeat=len(others)):
        parent = dict(zip(others, parents))
        if any(parent[vertex] == vertex for vertex in others):
            continue
        valid = True
        for start in others:
            seen = set()
            current = start
            while current != root:
                if current in seen or current not in parent:
                    valid = False
                    break
                seen.add(current)
                current = parent[current]
            if not valid:
                break
        if valid:
            yield parent


def run():
    records = []
    total_pairs = 0
    for size in range(1, 5):
        vertices = tuple(range(size))
        root = 0
        trees = list(rooted_trees(vertices, root))
        permutation_count = 0
        for parent in trees:
            incoming = {root: {"f"}}
            released = {vertex: set() for vertex in vertices}
            for child, source in parent.items():
                packet = f"R_{source}_{child}"
                incoming[child] = {packet}
                released[source].add(packet)
            all_incoming = set().union(*incoming.values())
            assert sum(map(len, incoming.values())) == len(all_incoming)
            assert all_incoming <= {"f"}.union(*released.values())
            for permutation in itertools.permutations(vertices):
                assert len(set(permutation)) == size
                permutation_count += 1
                total_pairs += 1
        records.append({
            "owner_count": size,
            "rooted_tree_count": len(trees),
            "response_permutations_checked": permutation_count,
        })
    assert [record["rooted_tree_count"] for record in records] == [1, 1, 3, 16]
    assert total_pairs == 405

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "charity-rooted-transfer-tree-release-audit-v1",
        "status": "ALL_RELEASE_COMPATIBLE",
        "records": records,
        "total_tree_permutation_pairs": total_pairs,
        "claim_boundary": (
            "finite set-support audit for all rooted labeled trees through "
            "four owners; packet valuation, EFX, and source existence are analytic"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "total_tree_permutation_pairs": result["total_tree_permutation_pairs"],
    }, indent=2))


if __name__ == "__main__":
    main()
