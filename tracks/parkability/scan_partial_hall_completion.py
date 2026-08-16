#!/usr/bin/env python3
"""Scan stored profiles for Hall-blocked maximum-Nash partial EFX states."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_partial_hall_completion import (
        one_old_good_move_completion,
        perfect_matchings,
    )
    from .fast_count import FastParkability
    from .scan_partial_nash_potential import matrices
except ImportError:
    from anneal import atomic_json
    from audit_partial_hall_completion import (
        one_old_good_move_completion,
        perfect_matchings,
    )
    from fast_count import FastParkability
    from scan_partial_nash_potential import matrices


SCHEMA = "partial-hall-completion-corpus-scan-v1"


def direct_hall_completion(values, state):
    for host in range(len(values)):
        masks = list(state["masks"])
        masks[host] |= 1 << state["floater"]
        graph, matchings = perfect_matchings(values, tuple(masks))
        if matchings:
            return {
                "floater_host": host,
                "masks": masks,
                "graph": [list(row) for row in graph],
                "matching": list(matchings[0]),
            }
    return None


def run(directory: Path, min_goods: int, max_goods: int) -> dict:
    evaluators = {}
    seen = set()
    records = []
    radius_zero_failures = []
    radius_one_failures = []
    paths = sorted(directory.glob("*.json"))
    for position, path in enumerate(paths, 1):
        for value_key, values in matrices(path):
            n = len(values)
            m = len(values[0])
            if n != 4 or m < min_goods or m > max_goods or values in seen:
                continue
            seen.add(values)
            evaluator = evaluators.setdefault((n, m), FastParkability(n, m))
            landscape = evaluator.partial_linear_potential_landscape(
                values, potential="normalized_nash"
            )
            winners = []
            for winner in landscape["maximizers"]:
                state = {
                    **winner,
                    "masks": tuple(
                        int(mask)
                        for mask in evaluator.base_masks[winner["floater"]][
                            winner["base_index"]
                        ]
                    ),
                }
                direct = direct_hall_completion(values, state)
                radius_one = one_old_good_move_completion(values, state)
                winners.append(
                    {
                        "floater": state["floater"],
                        "base_index": state["base_index"],
                        "masks": list(state["masks"]),
                        "utilities": state["utilities"],
                        "direct_hall_completion": direct,
                        "one_old_good_move_completion": radius_one,
                    }
                )
            record = {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "value_key": value_key,
                "n": n,
                "m": m,
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                "eligible_state_count": landscape["eligible_base_count"],
                "maximum_nash_winner_count": len(winners),
                "has_direct_hall_completion": any(
                    winner["direct_hall_completion"] is not None for winner in winners
                ),
                "has_one_old_good_move_completion": any(
                    winner["one_old_good_move_completion"] is not None
                    for winner in winners
                ),
                "winners": winners,
            }
            records.append(record)
            if not record["has_direct_hall_completion"]:
                radius_zero_failures.append(record)
            if not record["has_one_old_good_move_completion"]:
                radius_one_failures.append(record)
        if position % 500 == 0:
            print(
                f"files={position}/{len(paths)} profiles={len(records)} "
                f"radius1_failures={len(radius_one_failures)}",
                flush=True,
            )
    return {
        "schema": SCHEMA,
        "status": (
            "ONE_MOVE_COUNTEREXAMPLE_FOUND"
            if radius_one_failures
            else "NO_ONE_MOVE_COUNTEREXAMPLE_IN_CORPUS"
        ),
        "meaning": (
            "Finite stored-profile scan of maximum-Nash eligible partial EFX "
            "states; absence is evidence, not a theorem."
        ),
        "directory": str(directory),
        "json_file_count": len(paths),
        "distinct_profile_count": len(records),
        "max_goods": max_goods,
        "min_goods": min_goods,
        "direct_hall_failure_count": len(radius_zero_failures),
        "one_old_good_move_failure_count": len(radius_one_failures),
        "direct_hall_failures": radius_zero_failures,
        "one_old_good_move_failures": radius_one_failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--min-goods", type=int, default=1)
    parser.add_argument("--max-goods", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.directory, args.min_goods, args.max_goods)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
