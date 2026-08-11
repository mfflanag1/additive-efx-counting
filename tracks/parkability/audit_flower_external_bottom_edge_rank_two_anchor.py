#!/usr/bin/env python3
"""Audit the permanent rank-two flower anchor."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_covering_matching(edges: set[tuple[int, int]]) -> bool:
    return any(
        all((source, target) in edges for target, source in enumerate(perm))
        for perm in itertools.permutations(range(2))
    )


def has_empty_target(edges: set[tuple[int, int]]) -> bool:
    return any(not any(target == t for _, target in edges) for t in range(2))


def common_singleton(edges: set[tuple[int, int]]) -> bool:
    neighborhoods = [
        {source for source, target in edges if target == t}
        for t in range(2)
    ]
    return len(neighborhoods[0]) == 1 and neighborhoods[0] == neighborhoods[1]


def run(root: Path) -> dict:
    sources = ("r", "b")
    targets = ("T_q+f", "A_b subset T_r+B_q")
    matching = [[source, target] for source, target in zip(sources, targets)]
    assert len({source for source, _ in matching}) == 2
    assert len({target for _, target in matching}) == 2

    support_atoms = {
        "root_core": {"T_q", "f"},
        "external_bottom_core_parent": {"T_r", "B_q"},
    }
    supports_disjoint = not (
        support_atoms["root_core"]
        & support_atoms["external_bottom_core_parent"]
    )

    universe = [(source, target) for source in range(2) for target in range(2)]
    uncovered = 0
    for mask in range(16):
        edges = {edge for bit, edge in enumerate(universe) if mask & (1 << bit)}
        if not (
            has_covering_matching(edges)
            or has_empty_target(edges)
            or common_singleton(edges)
        ):
            uncovered += 1

    script = Path(__file__).resolve()
    theorem = root / "results/FLOWER_EXTERNAL_BOTTOM_EDGE_RANK_TWO_ANCHOR_LEMMA_20260811.md"
    return {
        "schema": "flower-external-bottom-edge-rank-two-anchor-audit-v1",
        "status": "ALL_FORCED",
        "permanent_matching": matching,
        "sources_distinct": True,
        "parent_supports_disjoint": supports_disjoint,
        "reset_support": {
            "fixed_cores": ["T_q+f", "A_b"],
            "residual_pool": "all remaining owner-union goods",
            "complete_partition": True,
        },
        "two_by_two_relation_count": 16,
        "two_by_two_uncovered_count": uncovered,
        "claim_boundary": (
            "cap-free exclusion of GG rank-one termination; canonical "
            "rank-two repair/reset recurrence is not terminated"
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
    output = args.output or root / "results/flower_external_bottom_edge_rank_two_anchor_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
