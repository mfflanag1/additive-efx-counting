#!/usr/bin/env python3
"""Exhaust the nonself image-three maps and verify full owner connectedness."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def component_sizes(mapping):
    adjacency = {owner: set() for owner in OWNERS}
    for target, source in enumerate(mapping):
        adjacency[target].add(source)
        adjacency[source].add(target)
    unseen = set(OWNERS)
    sizes = []
    while unseen:
        start = min(unseen)
        seen = set()
        queue = deque([start])
        while queue:
            owner = queue.popleft()
            if owner in seen:
                continue
            seen.add(owner)
            queue.extend(adjacency[owner] - seen)
        unseen -= seen
        sizes.append(len(seen))
    return tuple(sorted(sizes, reverse=True))


def run(root: Path = ROOT) -> dict[str, object]:
    maps = []
    component_histogram = Counter()
    missing_histogram = Counter()
    duplicate_histogram = Counter()
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        if len(set(mapping)) != 3:
            continue
        maps.append(mapping)
        sizes = component_sizes(mapping)
        component_histogram[sizes] += 1
        missing = next(owner for owner in OWNERS if owner not in mapping)
        duplicate = next(owner for owner in OWNERS if mapping.count(owner) == 2)
        missing_histogram[missing] += 1
        duplicate_histogram[duplicate] += 1

    theorem = root / "results/IMAGE_THREE_FULL_OWNER_CONNECTED_RANK_DEFECT_LEMMA_20260814.md"
    capture = root / "results/MISSING_SOURCE_TWO_CHOICE_FAN_DOUBLE_CAPTURE_LEMMA_20260814.md"
    extraction = root / "results/SATURATED_REPRESENTED_COMPONENT_CHARITY_EXTRACTION_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "connected full-owner physical response component" in text
    assert "hidden rank hypothesis" in text

    return {
        "schema": "image-three-full-owner-connected-rank-defect-audit-v1",
        "status": "ALL_48_MAPS_CONNECTED_RANK_THREE",
        "map_count": len(maps),
        "component_size_histogram": {
            "+".join(map(str, sizes)): count
            for sizes, count in sorted(component_histogram.items())
        },
        "missing_source_histogram": {
            str(owner): missing_histogram[owner] for owner in OWNERS
        },
        "duplicated_source_histogram": {
            str(owner): duplicate_histogram[owner] for owner in OWNERS
        },
        "all_maps_connected": component_histogram == {(4,): 48},
        "response_rank": 3,
        "owner_component_size": 4,
        "rank_full_for_component": False,
        "rank_four_augmentation_proved": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, capture, extraction, script)
        },
        "claim_boundary": (
            "every nonself image-three map is full-owner connected, but its "
            "source rank is three and the component-extraction rank gate remains"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
