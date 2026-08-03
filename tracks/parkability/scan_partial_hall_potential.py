#!/usr/bin/env python3
"""Scan stored profiles for Hall-blocked potential-maximizing partial EFX states."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_partial_hall_completion import one_old_good_move_completion
    from .fast_count import FastParkability
    from .scan_partial_hall_completion import direct_hall_completion
    from .scan_partial_nash_potential import matrices
except ImportError:
    import core
    from anneal import atomic_json
    from audit_partial_hall_completion import one_old_good_move_completion
    from fast_count import FastParkability
    from scan_partial_hall_completion import direct_hall_completion
    from scan_partial_nash_potential import matrices


SCHEMA = "partial-hall-potential-corpus-scan-v1"


def recursive_matrices(document, prefix="root"):
    if isinstance(document, dict):
        for key, raw in document.items():
            location = f"{prefix}.{key}"
            if key in {
                "values",
                "candidate_values",
                "post_wall_values",
                "wall_values",
            }:
                try:
                    yield location, core.validate_values(raw, lower=1)
                except (TypeError, ValueError):
                    pass
            yield from recursive_matrices(raw, location)
    elif isinstance(document, list):
        for index, raw in enumerate(document):
            yield from recursive_matrices(raw, f"{prefix}[{index}]")


def run(
    directory: Path,
    min_goods: int,
    max_goods: int,
    potential: str,
    recursive_values: bool = False,
    threshold_tiebreak: str = "none",
    direct_only: bool = False,
) -> dict:
    evaluators = {}
    seen = set()
    records = []
    radius_zero_failures = []
    radius_one_failures = []
    paths = sorted(directory.glob("*.json"))
    for position, path in enumerate(paths, 1):
        if recursive_values:
            try:
                candidates = recursive_matrices(json.loads(path.read_text()))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                candidates = ()
        else:
            candidates = matrices(path)
        for value_key, values in candidates:
            n = len(values)
            m = len(values[0])
            if n != 4 or m < min_goods or m > max_goods or values in seen:
                continue
            seen.add(values)
            evaluator = evaluators.setdefault((n, m), FastParkability(n, m))
            landscape = (
                evaluator.partial_pareto_threshold_landscape(values)
                if potential == "pareto_threshold"
                else evaluator.partial_linear_potential_landscape(
                    values, potential=potential
                )
            )
            selected_winners = landscape["maximizers"]
            if threshold_tiebreak in {"utilitarian", "utilitarian_min"}:
                if potential != "normalized_threshold":
                    raise ValueError(
                        "utilitarian threshold tie-break requires normalized_threshold"
                    )
                denominator = math.lcm(*(sum(row) for row in values))
                weights = tuple(denominator // sum(row) for row in values)
                secondary_scores = [
                    sum(
                        weight * utility
                        for weight, utility in zip(weights, winner["utilities"])
                    )
                    for winner in selected_winners
                ]
                best_secondary = (
                    min(secondary_scores)
                    if threshold_tiebreak == "utilitarian_min"
                    else max(secondary_scores)
                )
                selected_winners = [
                    winner
                    for winner in selected_winners
                    if sum(
                        weight * utility
                        for weight, utility in zip(weights, winner["utilities"])
                    )
                    == best_secondary
                ]
            winners = []
            for winner in selected_winners:
                state = {
                    **winner,
                    "masks": tuple(
                        int(mask)
                        for mask in evaluator.base_masks[winner["floater"]][
                            winner["base_index"]
                        ]
                    ),
                }
                winners.append(
                    {
                        "floater": state["floater"],
                        "base_index": state["base_index"],
                        "masks": list(state["masks"]),
                        "utilities": state["utilities"],
                        "identity_insertable": winner["insertable"],
                        "direct_hall_completion": (
                            {"vectorized_exact": True}
                            if direct_only and winner["hall_insertable"]
                            else (
                                None
                                if direct_only
                                else direct_hall_completion(values, state)
                            )
                        ),
                        "one_old_good_move_completion": (
                            None
                            if direct_only
                            else one_old_good_move_completion(values, state)
                        ),
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
                "winner_count": len(winners),
                "has_direct_hall_completion": any(
                    winner["direct_hall_completion"] is not None for winner in winners
                ),
                "has_identity_insertion": any(
                    winner["identity_insertable"] for winner in winners
                ),
                "all_winners_have_one_old_good_move_completion": (
                    None
                    if direct_only
                    else all(
                        winner["one_old_good_move_completion"] is not None
                        for winner in winners
                    )
                ),
                "has_one_old_good_move_completion": (
                    None
                    if direct_only
                    else any(
                        winner["one_old_good_move_completion"] is not None
                        for winner in winners
                    )
                ),
                "winners": winners,
            }
            records.append(record)
            if not record["has_direct_hall_completion"]:
                radius_zero_failures.append(record)
            if (
                not direct_only
                and not record["all_winners_have_one_old_good_move_completion"]
            ):
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
            (
                "DIRECT_COUNTEREXAMPLE_FOUND"
                if radius_zero_failures
                else "NO_DIRECT_COUNTEREXAMPLE_IN_CORPUS"
            )
            if direct_only
            else (
                "ONE_MOVE_COUNTEREXAMPLE_FOUND"
                if radius_one_failures
                else "NO_ONE_MOVE_COUNTEREXAMPLE_IN_CORPUS"
            )
        ),
        "meaning": (
            "Finite stored-profile scan of potential-maximizing eligible partial "
            "EFX states; absence is evidence, not a theorem."
        ),
        "potential": potential,
        "recursive_values": recursive_values,
        "threshold_tiebreak": threshold_tiebreak,
        "direct_only": direct_only,
        "directory": str(directory),
        "json_file_count": len(paths),
        "distinct_profile_count": len(records),
        "max_goods": max_goods,
        "min_goods": min_goods,
        "direct_hall_failure_count": len(radius_zero_failures),
        "identity_insertion_failure_count": sum(
            not record["has_identity_insertion"] for record in records
        ),
        "one_old_good_move_failure_count": len(radius_one_failures),
        "direct_hall_failures": radius_zero_failures,
        "one_old_good_move_failures": radius_one_failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--min-goods", type=int, default=1)
    parser.add_argument("--max-goods", type=int, default=10)
    parser.add_argument(
        "--potential",
        choices=(
            "normalized_utilitarian",
            "normalized_threshold",
            "pareto_threshold",
        ),
        default="normalized_utilitarian",
    )
    parser.add_argument("--recursive-values", action="store_true")
    parser.add_argument("--direct-only", action="store_true")
    parser.add_argument(
        "--threshold-tiebreak",
        choices=("none", "utilitarian", "utilitarian_min"),
        default="none",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.directory,
        args.min_goods,
        args.max_goods,
        args.potential,
        args.recursive_values,
        args.threshold_tiebreak,
        args.direct_only,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
