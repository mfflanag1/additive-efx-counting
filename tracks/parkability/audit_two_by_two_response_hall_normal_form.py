#!/usr/bin/env python3
"""Exhaustively audit the two-by-two response-Hall normal form."""

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
        (source_0, 0) in edges and (source_1, 1) in edges
        for source_0, source_1 in ((0, 1), (1, 0))
    )


def classify(edges: set[tuple[int, int]]) -> str:
    neighborhoods = [
        {source for source in range(2) if (source, target) in edges}
        for target in range(2)
    ]
    if has_covering_matching(edges):
        return "COVERING_MATCHING"
    if any(not neighborhood for neighborhood in neighborhoods):
        return "EMPTY_TARGET"
    assert neighborhoods[0] == neighborhoods[1]
    assert len(neighborhoods[0]) == 1
    return "COMMON_SINGLETON"


def run(root: Path) -> dict:
    universe = tuple(itertools.product(range(2), repeat=2))
    records = []
    counts = {
        "COVERING_MATCHING": 0,
        "EMPTY_TARGET": 0,
        "COMMON_SINGLETON": 0,
    }
    for mask in range(1 << len(universe)):
        edges = {
            edge for index, edge in enumerate(universe) if mask & (1 << index)
        }
        classification = classify(edges)
        counts[classification] += 1
        records.append({
            "mask": mask,
            "edges": [list(edge) for edge in sorted(edges)],
            "classification": classification,
        })

    assert counts == {
        "COVERING_MATCHING": 7,
        "EMPTY_TARGET": 7,
        "COMMON_SINGLETON": 2,
    }

    paired_full_sdr = 0
    for left in records:
        for right in records:
            if (
                left["classification"] == "COVERING_MATCHING"
                and right["classification"] == "COVERING_MATCHING"
            ):
                paired_full_sdr += 1
    assert paired_full_sdr == 49

    script = Path(__file__).resolve()
    theorem = root / "results/TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md"
    return {
        "schema": "two-by-two-response-hall-normal-form-audit-v1",
        "status": "ALL_EXHAUSTED",
        "relation_count": len(records),
        "classification_counts": counts,
        "paired_full_sdr_count": paired_full_sdr,
        "claim_boundary": (
            "exact graph classification only; elimination of the empty-target "
            "and common-singleton star forms is not proved"
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
    output = args.output or root / "results/two_by_two_response_hall_normal_form_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
