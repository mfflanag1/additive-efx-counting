#!/usr/bin/env python3
"""Exhaustive audit of rank-four five-target charity-path structure."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = tuple(range(4))
CHARITY = 4
TARGETS = (*OWNERS, CHARITY)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_cycles(matching):
    cycles = []
    seen = set()
    for start in OWNERS:
        if start in seen:
            continue
        order = []
        position = {}
        vertex = start
        while vertex != CHARITY and vertex not in seen and vertex not in position:
            position[vertex] = len(order)
            order.append(vertex)
            vertex = matching[vertex]
        seen.update(order)
        if vertex in position:
            cycles.append(tuple(order[position[vertex]:]))
    return cycles


def path_from_hole(matching, hole):
    path = []
    vertex = hole
    while vertex != CHARITY:
        assert vertex not in path
        path.append(vertex)
        vertex = matching[vertex]
    return tuple(path)


def run(root: Path) -> dict:
    counts = {
        "charity_hole_with_owner_cycle": 0,
        "owner_hole_with_owner_cycle": 0,
        "owner_hole_hamiltonian_charity_path": 0,
    }
    path_matchings = []
    for selected in itertools.permutations(TARGETS, len(OWNERS)):
        matching = dict(zip(OWNERS, selected))
        hole = next(target for target in TARGETS if target not in selected)
        cycles = owner_cycles(matching)
        if hole == CHARITY:
            assert cycles
            counts["charity_hole_with_owner_cycle"] += 1
        elif cycles:
            counts["owner_hole_with_owner_cycle"] += 1
        else:
            path = path_from_hole(matching, hole)
            assert len(path) == len(OWNERS)
            assert set(path) == set(OWNERS)
            assert matching[path[-1]] == CHARITY
            counts["owner_hole_hamiltonian_charity_path"] += 1
            path_matchings.append((matching, hole, path))

    cycle_lengths = {}
    pivot_count = 0
    for matching, hole, path in path_matchings:
        for source in OWNERS:
            old_target = matching[source]
            pivoted = dict(matching)
            pivoted[source] = hole
            assert old_target not in pivoted.values()
            cycles = owner_cycles(pivoted)
            expected = tuple(path[: path.index(source) + 1])
            assert any(
                len(cycle) == len(expected) and set(cycle) == set(expected)
                for cycle in cycles
            )
            length = len(expected)
            cycle_lengths[str(length)] = cycle_lengths.get(str(length), 0) + 1
            pivot_count += 1

    script = Path(__file__).resolve()
    theorem = root / "results/PI_FREE_FIVE_TARGET_CHARITY_PATH_HOLE_EDGE_LEMMA_20260811.md"
    return {
        "schema": "pi-free-five-target-charity-path-hole-edge-audit-v1",
        "status": "ALL_EXHAUSTED",
        "rank_four_matching_count": sum(counts.values()),
        "classification_counts": counts,
        "surviving_path_count": len(path_matchings),
        "hole_edge_pivot_count": pivot_count,
        "pivot_cycle_length_counts": cycle_lengths,
        "every_cycle_free_owner_hole_matching_is_hamiltonian_to_charity": True,
        "every_edge_into_surviving_hole_closes_owner_cycle": True,
        "remaining_gate": (
            "surplus-budgeted payment of a stable-label decorated prefix cycle"
        ),
        "claim_boundary": (
            "matching decomposition and one-pivot cycle only; physical payment, "
            "repeated-support GG, and EFX remain open"
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
