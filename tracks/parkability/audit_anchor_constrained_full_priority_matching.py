#!/usr/bin/env python3
"""Exhaust the anchor-constrained full-priority matching theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


SOURCES = ("r", "q", "c", "s")
NONROOT = ("q", "c", "s")
TARGETS = ("h", "t1", "t2", "t3")
ANCHOR = ("r", "h")
PRIORITY = {source: index for index, source in enumerate(NONROOT)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matchings(edges):
    yield ()
    for size in range(1, len(TARGETS) + 1):
        for targets in itertools.combinations(TARGETS, size):
            for sources in itertools.permutations(SOURCES, size):
                matching = tuple(zip(sources, targets))
                if all(edge in edges for edge in matching):
                    yield matching


def coverage_key(matching):
    represented = {source for source, _ in matching}
    return tuple(int(source in represented) for source in NONROOT)


def run(root: Path) -> dict:
    optional = tuple(
        edge for edge in itertools.product(SOURCES, TARGETS) if edge != ANCHOR
    )
    counts = {
        "relations": 0,
        "selected_matchings": 0,
        "unmatched_source_occurrences": 0,
        "anchor_neighbors": 0,
        "earlier_source_blockers": 0,
        "violations": 0,
    }
    blocker_examples = []
    for mask in range(1 << len(optional)):
        edges = {ANCHOR}
        edges.update(
            edge for index, edge in enumerate(optional) if mask & (1 << index)
        )
        anchored = tuple(m for m in matchings(edges) if ANCHOR in m)
        rank = max(map(len, anchored))
        maximum = tuple(m for m in anchored if len(m) == rank)
        best_key = max(map(coverage_key, maximum))
        selected = tuple(m for m in maximum if coverage_key(m) == best_key)
        counts["relations"] += 1
        counts["selected_matchings"] += len(selected)
        for matching in selected:
            represented = {source for source, _ in matching}
            target_source = {target: source for source, target in matching}
            for source in NONROOT:
                if source in represented:
                    continue
                counts["unmatched_source_occurrences"] += 1
                for edge_source, target in edges:
                    if edge_source != source:
                        continue
                    if target == "h":
                        counts["anchor_neighbors"] += 1
                        continue
                    blocker = target_source.get(target)
                    if blocker in PRIORITY and PRIORITY[blocker] < PRIORITY[source]:
                        counts["earlier_source_blockers"] += 1
                        if len(blocker_examples) < 4:
                            blocker_examples.append({
                                "unmatched_source": source,
                                "target": target,
                                "earlier_blocker": blocker,
                                "matching": [list(edge) for edge in matching],
                            })
                        continue
                    counts["violations"] += 1
    assert counts["relations"] == 1 << 15
    assert counts["violations"] == 0

    script = Path(__file__).resolve()
    theorem = root / "results/ANCHOR_CONSTRAINED_FULL_PRIORITY_MATCHING_LEMMA_20260811.md"
    return {
        "schema": "anchor-constrained-full-priority-matching-audit-v1",
        "status": "ALL_CLASSIFIED",
        "sources": list(SOURCES),
        "targets": list(TARGETS),
        "forced_anchor": list(ANCHOR),
        "nonroot_priority": list(NONROOT),
        "counts": counts,
        "blocker_examples": blocker_examples,
        "claim_boundary": (
            "exhaustive response-graph verification of priority-triangular "
            "blockers; physical root-facing, J-exhaustion, hitting-set, and "
            "third-owner fork closure remain open"
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
