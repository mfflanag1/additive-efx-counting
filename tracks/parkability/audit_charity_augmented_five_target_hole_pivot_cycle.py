#!/usr/bin/env python3
"""Exact matching audit of five-target charity-hole pivot cycles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


SOURCES = tuple(range(4))
TARGETS = tuple(range(5))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initial_matchings():
    for matched_targets in itertools.permutations(TARGETS, len(SOURCES)):
        matching = dict(zip(SOURCES, matched_targets))
        hole = next(target for target in TARGETS if target not in matching.values())
        yield matching, hole


def pivot(matching, hole, source):
    old_target = matching[source]
    updated = dict(matching)
    updated[source] = hole
    assert len(set(updated.values())) == len(SOURCES)
    assert old_target not in updated.values()
    return updated, old_target


def explore(matching, holes, sources, states, records, depth):
    current_hole = holes[-1]
    if depth == 0:
        raise AssertionError("five targets must force a repeated hole")
    for source in SOURCES:
        updated, new_hole = pivot(matching, current_hole, source)
        next_holes = (*holes, new_hole)
        next_sources = (*sources, source)
        if new_hole in holes:
            first = holes.index(new_hole)
            cycle_holes = holes[first + 1:]
            cycle_sources = next_sources[first + 1:]
            assert len(cycle_holes) == len(cycle_sources)
            assert len(set(cycle_holes)) == len(cycle_holes)
            assert len(set(cycle_sources)) == len(cycle_sources)
            before = states[first]
            rotated = dict(before)
            for cycle_source, cycle_hole in zip(cycle_sources, cycle_holes):
                rotated[cycle_source] = cycle_hole
            assert updated == rotated
            outside = set(SOURCES) - set(cycle_sources)
            assert all(updated[source] == before[source] for source in outside)
            records.append({
                "cycle_length": len(cycle_sources),
                "first_repeat_depth": len(next_sources),
            })
            continue
        explore(updated, next_holes, next_sources, (*states, updated), records, depth - 1)


def run(root: Path) -> dict:
    records = []
    matching_count = 0
    for matching, hole in initial_matchings():
        matching_count += 1
        explore(matching, (hole,), (), (matching,), records, len(TARGETS))
    lengths = {}
    depths = {}
    for record in records:
        key = str(record["cycle_length"])
        lengths[key] = lengths.get(key, 0) + 1
        depth = str(record["first_repeat_depth"])
        depths[depth] = depths.get(depth, 0) + 1

    script = Path(__file__).resolve()
    theorem = root / "results/CHARITY_AUGMENTED_FIVE_TARGET_HOLE_PIVOT_CYCLE_LEMMA_20260811.md"
    return {
        "schema": "charity-augmented-five-target-hole-pivot-cycle-audit-v1",
        "status": "ALL_EXHAUSTED",
        "source_count": len(SOURCES),
        "target_count": len(TARGETS),
        "rank_four_matching_count": matching_count,
        "pivot_sequences_closed": len(records),
        "cycle_length_counts": lengths,
        "first_repeat_depth_counts": depths,
        "rank_preserved_every_pivot": True,
        "unique_hole_preserved_every_pivot": True,
        "cycle_sources_and_targets_distinct_before_first_repeat": True,
        "outside_matching_invariant": True,
        "remaining_gate": (
            "physical edge-label persistence and observer-safe payment across dynamic GG resets"
        ),
        "claim_boundary": (
            "exact fixed-state five-target matching recurrence; dynamic physical-label "
            "persistence, repeated-support GG, and EFX remain open"
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
