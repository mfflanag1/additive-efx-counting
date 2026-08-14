#!/usr/bin/env python3
"""Independent graph audit of form-2 six-branch full-owner admission."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


OWNERS = ("r", "q", "s", "d")
VERTICES = {*OWNERS, "charity"}
CYCLE_TRANSFERS = {
    "r": ("q", "r"),
    "q": ("s", "q"),
    "s": ("r", "s"),
}
D_TRANSFERS = {"r": ("r", "d"), "q": ("q", "d")}


def connected(edges):
    adjacency = {vertex: set() for vertex in VERTICES}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    queue = deque(["charity"])
    while queue:
        vertex = queue.popleft()
        if vertex in seen:
            continue
        seen.add(vertex)
        queue.extend(adjacency[vertex] - seen)
    return seen == VERTICES


def branch_rows():
    rows = []
    for d_target, d_edge in D_TRANSFERS.items():
        for omitted in ("r", "q", "s"):
            edges = {
                ("charity", omitted),
                d_edge,
                *(
                    edge for source, edge in CYCLE_TRANSFERS.items()
                    if source != omitted
                ),
            }
            assert len(edges) == 4
            assert connected(edges)
            degrees = {
                vertex: sum(vertex in edge for edge in edges)
                for vertex in VERTICES
            }
            assert sum(degrees.values()) == 8
            # Connected graph with five vertices and four edges is a tree.
            rows.append({
                "d_response_target": d_target,
                "omitted_cycle_source": omitted,
                "edges": sorted(map(list, edges)),
                "degrees": degrees,
                "connected_all_five_vertices": True,
                "spanning_tree": True,
            })
    assert len(rows) == 6
    assert {
        (row["d_response_target"], row["omitted_cycle_source"])
        for row in rows
    } == set(itertools.product(("r", "q"), ("r", "q", "s")))
    return rows


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_SIX_BRANCH_FULL_OWNER_ADMISSION_REDUCTION_20260814.md"
    rows = branch_rows()
    return {
        "schema": "form2-six-branch-full-owner-admission-v1",
        "status": "SIX_FOUR_EDGE_SPANNING_TREES",
        "branch_count": len(rows),
        "branches": rows,
        "minimum_response_argument": {
            "premise": (
                "C has globally minimum cardinality among all subbundles "
                "strictly desired above an owner's probe utility"
            ),
            "contradiction_step": (
                "tail_k(C)>u_k implies some C-g is a smaller strictly "
                "desired subbundle for k"
            ),
            "conclusion": "tail_k(C)<=u_k for every observer k",
        },
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free graph and minimum-response safety audit; signed "
            "base-margin admission and saturation composition are not proved"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "branch_count": result["branch_count"]
    }, indent=2))


if __name__ == "__main__":
    main()
