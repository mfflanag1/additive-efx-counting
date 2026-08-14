#!/usr/bin/env python3
"""Exhaustive audit of four-owner nonself minimal Hall defects."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = tuple(range(4))
EDGES = tuple((target, source) for target in OWNERS for source in OWNERS if target != source)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def neighborhood(graph, targets):
    return {source for target, source in graph if target in targets}


def deficient(graph, targets):
    return len(neighborhood(graph, targets)) < len(targets)


def minimal_defects(graph):
    defects = []
    for size in range(1, 5):
        for targets in itertools.combinations(OWNERS, size):
            target_set = frozenset(targets)
            if not deficient(graph, target_set):
                continue
            if any(deficient(graph, frozenset(proper))
                   for proper_size in range(1, size)
                   for proper in itertools.combinations(targets, proper_size)):
                continue
            defects.append(target_set)
    return defects


def has_perfect_matching(graph, targets, sources):
    targets = tuple(targets)
    sources = tuple(sources)
    if len(targets) != len(sources):
        return False
    return any(
        all((target, source) in graph for target, source in zip(targets, perm))
        for perm in itertools.permutations(sources)
    )


def run(root: Path) -> dict:
    graph_count = 0
    defect_count = 0
    nonempty_defect_count = 0
    external_count = 0
    internal_cycle_counts = {"2": 0, "3": 0}
    shape_counts = {}

    for mask in range(1 << len(EDGES)):
        graph = {edge for index, edge in enumerate(EDGES) if mask & (1 << index)}
        graph_count += 1
        for targets in minimal_defects(graph):
            defect_count += 1
            if any(not neighborhood(graph, {target}) for target in targets):
                continue
            nonempty_defect_count += 1
            sources = neighborhood(graph, targets)
            assert len(sources) == len(targets) - 1
            shape = f"{len(targets)}x{len(sources)}"
            shape_counts[shape] = shape_counts.get(shape, 0) + 1
            if not sources <= set(targets):
                external_count += 1
                continue

            missing = set(targets) - sources
            assert len(missing) == 1
            reduced_targets = set(targets) - missing
            assert reduced_targets == sources
            assert has_perfect_matching(graph, reduced_targets, sources)
            size = len(sources)
            assert size in (2, 3)
            internal_cycle_counts[str(size)] += 1

    assert graph_count == 4096
    assert nonempty_defect_count == external_count + sum(internal_cycle_counts.values())
    assert set(shape_counts) <= {"2x1", "3x2", "4x3"}

    theorem = root / "results" / "FOUR_OWNER_NONSELF_MINIMAL_HALL_DEFECT_CYCLE_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "four-owner-nonself-minimal-hall-defect-cycle-audit-v1",
        "status": "ALL_MINIMAL_DEFECTS_CLASSIFIED",
        "graphs_checked": graph_count,
        "minimal_defects_checked": defect_count,
        "nonempty_minimal_defects_checked": nonempty_defect_count,
        "external_source_defects": external_count,
        "internal_cycle_counts": internal_cycle_counts,
        "shape_counts": shape_counts,
        "internal_defect_cycle_lengths": [2, 3],
        "remaining_shapes": ["2 targets / 1 external source", "3 targets / 2 sources with an external source"],
        "claim_boundary": (
            "incidence classification and internal-cycle extraction only; "
            "external-source residual payment, fixed-U, GG, and EFX remain open"
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
    print(json.dumps({"status": result["status"], "remaining_shapes": result["remaining_shapes"]}, indent=2))


if __name__ == "__main__":
    main()
