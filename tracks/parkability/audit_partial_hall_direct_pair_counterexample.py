#!/usr/bin/env python3
"""Exactly audit the realizable counterexample to direct-only pair extraction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from . import core
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .audit_partial_hall_completion import (
        hall_witnesses,
        one_old_good_move_completion,
        perfect_matchings,
    )
except ImportError:
    import core
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from audit_partial_hall_completion import (
        hall_witnesses,
        one_old_good_move_completion,
        perfect_matchings,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    values = core.validate_values(document["values"], expected_n=4, lower=1)
    base_masks = tuple(document["base_masks"])
    floater = document["floater"]
    state = next(
        state
        for state in enumerate_states(values)
        if state["floater"] == floater and state["masks"] == base_masks
    )
    direct = []
    for host in range(4):
        masks = list(base_masks)
        masks[host] |= 1 << floater
        graph, matchings = perfect_matchings(values, tuple(masks))
        host_pairs = [
            list(pair)
            for pair in itertools.combinations(range(4), 2)
            if set(graph[pair[0]]) | set(graph[pair[1]]) == {host}
        ]
        direct.append(
            {
                "host": host,
                "masks": masks,
                "graph": [list(row) for row in graph],
                "perfect_matching_count": len(matchings),
                "host_pair_witnesses": host_pairs,
                "hall_witnesses": [
                    {"agents": list(agents), "neighbors": list(neighbors)}
                    for agents, neighbors in hall_witnesses(graph)
                ],
            }
        )
    transfer_completion = one_old_good_move_completion(values, state)
    artifact = {
        "schema": "partial-hall-direct-pair-counterexample-audit-v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "base_is_eligible_one_floater_efx": True,
        "direct_insertion_graphs": direct,
        "all_direct_insertions_blocked": all(
            record["perfect_matching_count"] == 0 for record in direct
        ),
        "all_direct_insertions_avoid_host_pair": all(
            not record["host_pair_witnesses"] for record in direct
        ),
        "one_old_good_move_completion": transfer_completion,
        "direct_only_conjecture_refuted": (
            all(record["perfect_matching_count"] == 0 for record in direct)
            and all(not record["host_pair_witnesses"] for record in direct)
        ),
        "radius_one_completion_exists": transfer_completion is not None,
        "claim_boundary": (
            "This refutes direct-insertion pair extraction only. It does not "
            "refute pair extraction with one old-good transfer or complete EFX."
        ),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
