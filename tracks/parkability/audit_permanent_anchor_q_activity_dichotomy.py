#!/usr/bin/env python3
"""Exhaust the permanent-anchor q-activity dichotomy."""

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


def all_matchings(edges: set[tuple[str, str]]):
    yield ()
    for size in range(1, len(TARGETS) + 1):
        for targets in itertools.combinations(TARGETS, size):
            for sources in itertools.permutations(SOURCES, size):
                matching = tuple(zip(sources, targets))
                if all(edge in edges for edge in matching):
                    yield matching


def run(root: Path) -> dict:
    optional_edges = tuple(
        edge
        for edge in itertools.product(SOURCES, TARGETS)
        if edge not in {ANCHOR, FORBIDDEN}
    )
    counts = {
        "relations": 0,
        "q_active": 0,
        "q_degree_zero": 0,
        "active_q_anchor_maximum_representable": 0,
        "anchor_rank_gap": 0,
        "anchor_rank_gap_q_active": 0,
        "uncovered": 0,
    }
    rank_gap_examples = []
    for mask in range(1 << len(optional_edges)):
        edges = {ANCHOR}
        edges.update(
            edge
            for index, edge in enumerate(optional_edges)
            if mask & (1 << index)
        )
        matchings = tuple(all_matchings(edges))
        rank = max(map(len, matchings))
        anchored = tuple(m for m in matchings if ANCHOR in m)
        anchor_rank = max(map(len, anchored))
        maximum_anchored = tuple(m for m in anchored if len(m) == anchor_rank)
        q_active = any(source == "q" for source, _ in edges)
        q_representable = any(
            any(source == "q" for source, _ in matching)
            for matching in maximum_anchored
        )

        counts["relations"] += 1
        if anchor_rank < rank:
            counts["anchor_rank_gap"] += 1
            if q_active:
                counts["anchor_rank_gap_q_active"] += 1
            if len(rank_gap_examples) < 3:
                rank_gap_examples.append({
                    "edges": [list(edge) for edge in sorted(edges)],
                    "rank": rank,
                    "anchor_rank": anchor_rank,
                    "q_active": q_active,
                    "q_anchor_maximum_representable": q_representable,
                })
        if q_active:
            counts["q_active"] += 1
            if q_representable:
                counts["active_q_anchor_maximum_representable"] += 1
            else:
                counts["uncovered"] += 1
        else:
            counts["q_degree_zero"] += 1

    assert counts["relations"] == 1 << 14
    assert counts["q_active"] == counts["active_q_anchor_maximum_representable"]
    assert counts["q_active"] + counts["q_degree_zero"] == counts["relations"]
    assert counts["uncovered"] == 0

    script = Path(__file__).resolve()
    theorem = root / "results" / "PERMANENT_ANCHOR_Q_ACTIVITY_DICHOTOMY_LEMMA_20260811.md"
    return {
        "schema": "permanent-anchor-q-activity-dichotomy-audit-v1",
        "status": "ALL_CLASSIFIED",
        "sources": list(SOURCES),
        "targets": list(TARGETS),
        "forced_anchor": list(ANCHOR),
        "forbidden_q_anchor_edge": list(FORBIDDEN),
        "counts": counts,
        "rank_gap_examples": rank_gap_examples,
        "claim_boundary": (
            "exhaustive four-source/four-target graph theorem; degree-zero "
            "source-inactive closure, residual payment, physical release support, "
            "GG closure, and general EFX remain open"
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
    output = args.output or root / "results" / "permanent_anchor_q_activity_dichotomy_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
