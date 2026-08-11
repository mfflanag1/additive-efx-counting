#!/usr/bin/env python3
"""Exhaust the anchor-constrained q-priority matching dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


SOURCES = ("r", "q", "c", "s")
TARGETS = ("h", "t1", "t2", "t3")
ANCHOR = ("r", "h")
FORBIDDEN = ("q", "h")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matchings(edges: set[tuple[str, str]]):
    yield ()
    for size in range(1, len(TARGETS) + 1):
        for targets in itertools.combinations(TARGETS, size):
            for sources in itertools.permutations(SOURCES, size):
                matching = tuple(zip(sources, targets))
                if all(edge in edges for edge in matching):
                    yield matching


def anchor_component_balance(anchored_matching, maximum_matching):
    anchored_edges = set(anchored_matching)
    maximum_edges = set(maximum_matching)
    symmetric = anchored_edges ^ maximum_edges
    adjacency = {}
    for source, target in symmetric:
        left, right = ("source", source), ("target", target)
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    start = ("source", ANCHOR[0])
    stack = [start]
    component_nodes = set()
    while stack:
        node = stack.pop()
        if node in component_nodes:
            continue
        component_nodes.add(node)
        stack.extend(adjacency.get(node, ()))
    component_edges = {
        edge for edge in symmetric
        if ("source", edge[0]) in component_nodes
        and ("target", edge[1]) in component_nodes
    }
    degrees = [len(adjacency[node]) for node in component_nodes]
    return {
        "maximum_minus_anchor_edges": (
            len(component_edges & maximum_edges)
            - len(component_edges & anchored_edges)
        ),
        "is_path": bool(component_edges) and max(degrees, default=0) <= 2
        and sum(degree == 1 for degree in degrees) == 2,
    }


def run(root: Path) -> dict:
    optional_edges = tuple(
        edge
        for edge in itertools.product(SOURCES, TARGETS)
        if edge not in {ANCHOR, FORBIDDEN}
    )
    counts = {
        "relations": 0,
        "anchor_rank_gap": 0,
        "anchor_rank_gap_exactly_one": 0,
        "anchor_rank_gap_path_witness": 0,
        "anchor_rank_equal_q_representable": 0,
        "anchor_rank_equal_q_unmatched": 0,
        "uncovered": 0,
    }
    rank_gap_examples = []
    for mask in range(1 << len(optional_edges)):
        edges = {ANCHOR}
        edges.update(
            edge for index, edge in enumerate(optional_edges)
            if mask & (1 << index)
        )
        all_matchings = tuple(matchings(edges))
        rank = max(map(len, all_matchings))
        anchored = tuple(
            matching for matching in all_matchings if ANCHOR in matching
        )
        anchor_rank = max(map(len, anchored))
        counts["relations"] += 1
        if anchor_rank < rank:
            counts["anchor_rank_gap"] += 1
            if rank == anchor_rank + 1:
                counts["anchor_rank_gap_exactly_one"] += 1
            anchored_maximum = next(
                matching for matching in anchored
                if len(matching) == anchor_rank
            )
            path_witness = any(
                (record := anchor_component_balance(
                    anchored_maximum, maximum_matching
                ))["is_path"]
                and record["maximum_minus_anchor_edges"] == 1
                for maximum_matching in all_matchings
                if len(maximum_matching) == rank
            )
            if path_witness:
                counts["anchor_rank_gap_path_witness"] += 1
            else:
                counts["uncovered"] += 1
            if len(rank_gap_examples) < 3:
                rank_gap_examples.append({
                    "edges": [list(edge) for edge in sorted(edges)],
                    "rank": rank,
                    "anchor_rank": anchor_rank,
                })
            continue
        maximum_anchored = tuple(
            matching for matching in anchored if len(matching) == rank
        )
        if any(any(source == "q" for source, _ in matching) for matching in maximum_anchored):
            counts["anchor_rank_equal_q_representable"] += 1
            continue
        counts["anchor_rank_equal_q_unmatched"] += 1
        q_neighbors = {target for source, target in edges if source == "q"}
        if q_neighbors:
            counts["uncovered"] += 1
    assert counts["relations"] == 1 << 14
    assert counts["anchor_rank_gap_exactly_one"] == counts["anchor_rank_gap"]
    assert counts["anchor_rank_gap_path_witness"] == counts["anchor_rank_gap"]
    assert counts["uncovered"] == 0

    script = Path(__file__).resolve()
    theorem = root / "results/ANCHOR_CONSTRAINED_Q_PRIORITY_MATCHING_LEMMA_20260811.md"
    return {
        "schema": "anchor-constrained-q-priority-matching-audit-v1",
        "status": "ALL_CLASSIFIED",
        "sources": list(SOURCES),
        "targets": list(TARGETS),
        "forced_anchor": list(ANCHOR),
        "forbidden_sacrificed_q_anchor_edge": list(FORBIDDEN),
        "counts": counts,
        "rank_gap_examples": rank_gap_examples,
        "claim_boundary": (
            "exhaustive four-source response-graph theorem: an anchor-compatible "
            "maximum matching either represents q or an unmatched sacrificed q "
            "has degree zero; release-compatible closure of the anchor-rank-gap "
            "alternating path and source-inactive reset recurrence remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/anchor_constrained_q_priority_matching_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
