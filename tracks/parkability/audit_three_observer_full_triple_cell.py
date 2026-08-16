#!/usr/bin/env python3
"""Audit the full favorite-triple cell shared by two hard boundaries."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .run_distinct_half_conversion_dichotomy_cegar import FAVORITE
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from run_distinct_half_conversion_dichotomy_cegar import FAVORITE


SCHEMA = "three-observer-full-triple-cell-audit-v1"
N = 4
M = 9


def load_values(path):
    payload = json.loads(path.read_text())
    return tuple(tuple(map(int, row)) for row in payload["values"])


def pairings(goods):
    if not goods:
        yield ()
        return
    first = goods[0]
    for position in range(1, len(goods)):
        second = goods[position]
        remaining = goods[1:position] + goods[position + 1 :]
        for suffix in pairings(remaining):
            yield ((first, second),) + suffix


def partition_for(parked, matching):
    return tuple(
        sorted(
            ((FAVORITE,) + parked,) + tuple(tuple(sorted(pair)) for pair in matching)
        )
    )


def audit_profile(path):
    values = load_values(path)
    representatives = audit_branch(values)
    cells = []
    for parked in itertools.combinations(range(1, M), 2):
        remaining = tuple(good for good in range(1, M) if good not in parked)
        universal_acceptors = tuple(
            observer
            for observer, row in enumerate(values)
            if all(
                row[left] + row[right]
                >= row[FAVORITE] + max(row[good] for good in parked)
                for left, right in itertools.combinations(remaining, 2)
            )
        )
        efx_pairings = sum(
            matching_rank(feasible_graph(values, partition_for(parked, matching)))
            == N
            for matching in pairings(remaining)
        )
        if universal_acceptors or efx_pairings:
            cells.append({
                "parked_goods": list(parked),
                "universally_accepting_agents": list(universal_acceptors),
                "efx_pairing_count": efx_pairings,
            })

    common_bottom_pairs = tuple(
        parked
        for parked in itertools.combinations(range(1, M), 2)
        if all(
            set(parked)
            == set(sorted(range(1, M), key=lambda good: row[good])[:2])
            for row in values
        )
    )
    full_cells = tuple(
        cell for cell in cells if cell["efx_pairing_count"] == 15
    )
    three_observer_cells = tuple(
        cell for cell in cells if len(cell["universally_accepting_agents"]) >= 3
    )
    if (
        representatives != (3, 4, 5, 6)
        or common_bottom_pairs != ((1, 2),)
        or len(full_cells) != 1
        or full_cells[0]["parked_goods"] != [1, 2]
        or len(three_observer_cells) != 1
        or three_observer_cells[0]["parked_goods"] != [1, 2]
        or three_observer_cells[0]["universally_accepting_agents"] != [0, 2, 3]
    ):
        raise AssertionError(f"full-cell boundary changed for {path}")
    return {
        "source": str(path.resolve()),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "half_favorite_representatives": list(representatives),
        "common_bottom_pair": [1, 2],
        "full_cell": full_cells[0],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": SCHEMA,
        "status": "THREE_OBSERVER_FULL_TRIPLE_CELL_AUDIT_PASSED",
        "profiles": [audit_profile(path) for path in args.source],
        "interpretation": (
            "Both zero-favorite-pair boundaries contain the same full "
            "15-pairing favorite-triple cell, witnessed by three agents "
            "accepting every residual pair."
        ),
        "limitation": (
            "This finite two-profile census motivates a conditional lemma; "
            "it does not prove that the full cell is forced."
        ),
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
