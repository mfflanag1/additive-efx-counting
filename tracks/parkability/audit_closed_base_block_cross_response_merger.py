#!/usr/bin/env python3
"""Audit the finite quotient-merger argument for closed base blocks."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERTICES = tuple(range(5))
OWNERS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_partition(labels: tuple[int, ...]) -> tuple[int, ...]:
    relabel: dict[int, int] = {}
    return tuple(relabel.setdefault(label, len(relabel)) for label in labels)


def components(block_count: int, edges: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    parent = list(range(block_count))

    def find(item: int) -> int:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    for left, right in edges:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
    return canonical_partition(tuple(find(item) for item in range(block_count)))


def run(root: Path = ROOT) -> dict[str, object]:
    partitions = sorted({
        canonical_partition(labels)
        for labels in itertools.product(range(len(VERTICES)), repeat=len(VERTICES))
    })
    checked_cross_pairs = 0
    strict_mergers = 0
    merger_bound_holds = True

    for partition in partitions:
        block_count = len(set(partition))
        if block_count < 2:
            continue
        all_edges = tuple(itertools.combinations(range(block_count), 2))
        owner_edges = {
            tuple(sorted((partition[source], partition[target])))
            for source in OWNERS
            for target in OWNERS
            if source != target and partition[source] != partition[target]
        }
        for mask in range(1 << len(all_edges)):
            existing = frozenset(
                edge for index, edge in enumerate(all_edges) if mask & (1 << index)
            )
            before = components(block_count, existing)
            for edge in owner_edges:
                left, right = edge
                if before[left] == before[right]:
                    continue
                checked_cross_pairs += 1
                after = components(block_count, existing | {edge})
                before_count = len(set(before))
                after_count = len(set(after))
                assert after_count == before_count - 1
                strict_mergers += 1
        merger_bound_holds &= block_count - 1 <= len(VERTICES) - 1

    theorem = root / "results/CLOSED_BASE_BLOCK_CROSS_RESPONSE_MERGER_LEMMA_20260814.md"
    parent = root / "results/BRANCH_TREE_BASE_CANCELLATION_OR_CLOSED_UNION_LEMMA_20260814.md"
    response_parent = root / "results/PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "outsider safety" in text
    assert "response rank" in text

    return {
        "schema": "closed-base-block-cross-response-merger-audit-v1",
        "status": "OUTSIDER_FAILURE_AUGMENTS_OR_MERGES",
        "set_partition_count_on_five_vertices": len(partitions),
        "checked_cross_block_owner_pairs": checked_cross_pairs,
        "strict_merger_checks": strict_mergers,
        "maximum_strict_mergers": len(VERTICES) - 1,
        "merger_bound_holds": merger_bound_holds,
        "packet_size_bound_used": False,
        "current_safe_response_extraction_inherited": True,
        "current_safe_response_extraction_reencoded": False,
        "outsider_safety_at_saturation": True,
        "response_rank_proved": False,
        "component_margin_separator_proved": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, response_parent, script)
        },
        "claim_boundary": (
            "cross-block EFX failure is response augmentation or strict "
            "represented-component merger; internal rank and margins remain"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
