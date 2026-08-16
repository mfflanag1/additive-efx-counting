#!/usr/bin/env python3
"""Search stored Hall obstructions for a two-positive reroute refutation."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states
    from .audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        component_state_properties,
        owner_vector,
        owners_key,
        transfer_components,
        transfers,
    )
    from .audit_partial_hall_completion import perfect_matchings
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    import core
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states
    from audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        component_state_properties,
        owner_vector,
        owners_key,
        transfer_components,
        transfers,
    )
    from audit_partial_hall_completion import perfect_matchings
    from decide_partial_hall_radius_one import candidate_partitions


BASE = ((6, 7), (1, 2, 3), (0, 4), (5,))
BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8


def recognized_values(document):
    if isinstance(document, dict):
        for key, raw in document.items():
            if key in {"values", "post_wall_values", "wall_values"}:
                try:
                    yield core.validate_values(
                        raw, expected_n=4, expected_m=9, lower=1
                    )
                except (AssertionError, TypeError, ValueError):
                    pass
            yield from recognized_values(raw)
    elif isinstance(document, list):
        for item in document:
            yield from recognized_values(item)


def hall_obstructed(values) -> bool:
    for move in candidate_partitions(BASE, BASE_FLOATER):
        masks = tuple(
            sum(1 << good for good in bundle) for bundle in move["partition"]
        )
        _, matchings = perfect_matchings(values, masks)
        if matchings:
            return False
    return True


def fraction_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def primitive_profile(values):
    return tuple(
        tuple(entry // reduce(gcd, row) for entry in row) for row in values
    )


def analyze(values):
    base_owner = owner_vector(BASE_MASKS, BASE_FLOATER)
    base_efx, base_parked = component_state_properties(values, base_owner)
    if not base_efx or not base_parked or not hall_obstructed(values):
        return None
    row_totals = tuple(map(sum, values))
    base_utilities = tuple(
        sum(values[agent][good] for good in BASE[agent]) for agent in range(4)
    )
    base_score = sum(
        (Fraction(base_utilities[agent], row_totals[agent]) for agent in range(4)),
        Fraction(),
    )
    states = enumerate_states(values)
    eligible = {(state["floater"], tuple(state["masks"])): state for state in states}
    connected_improvers = []
    for candidate in states:
        candidate_score = sum(candidate["normalized"], Fraction())
        if candidate_score <= base_score:
            continue
        candidate_owner = owner_vector(candidate["masks"], candidate["floater"])
        if component_count(transfers(base_owner, candidate_owner)) == 1:
            connected_improvers.append((candidate, candidate_owner, candidate_score))
    qualifying = 0
    reroute_successes = 0
    counterexamples = []
    for state in states:
        state_score = sum(state["normalized"], Fraction())
        if state_score <= base_score:
            continue
        target_owner = owner_vector(state["masks"], state["floater"])
        edges = transfers(base_owner, target_owner)
        if len(edges) > 5:
            continue
        components = transfer_components(edges)
        if len(components) != 2:
            continue
        component_records = []
        qualifies = True
        for goods in components:
            intermediate = list(base_owner)
            for good in goods:
                intermediate[good] = target_owner[good]
            component_efx, component_parked = component_state_properties(
                values, tuple(intermediate)
            )
            component_utilities = tuple(
                sum(
                    values[agent][good]
                    for good, owner in enumerate(intermediate)
                    if owner == agent
                )
                for agent in range(4)
            )
            gain = sum(
                (
                    Fraction(component_utilities[agent], row_totals[agent])
                    for agent in range(4)
                ),
                Fraction(),
            ) - base_score
            component_records.append(
                {
                    "goods": list(goods),
                    "partial_efx": component_efx,
                    "floater_nonenvy": component_parked,
                    "potential_gain": fraction_record(gain),
                }
            )
            qualifies &= gain > 0 and component_parked and not component_efx
        if not qualifies:
            continue
        qualifying += 1
        successful = []
        for good in range(9):
            for destination in range(-1, 4):
                if destination == target_owner[good]:
                    continue
                reroute_owner = list(target_owner)
                reroute_owner[good] = destination
                key = owners_key(tuple(reroute_owner))
                if key is None:
                    continue
                reroute_edges = transfers(base_owner, tuple(reroute_owner))
                reroute_state = eligible.get(key)
                if reroute_state is None or component_count(reroute_edges) != 1:
                    continue
                gain = sum(reroute_state["normalized"], Fraction()) - base_score
                if gain > 0:
                    successful.append(
                        {
                            "good": good,
                            "destination": destination,
                            "floater": key[0],
                            "masks": list(key[1]),
                            "potential_gain": fraction_record(gain),
                        }
                    )
        if successful:
            reroute_successes += 1
            continue
        nearest_state, nearest_owner, nearest_score = min(
            connected_improvers,
            key=lambda item: sum(
                left != right for left, right in zip(target_owner, item[1])
            ),
        )
        nearest_distance = sum(
            left != right for left, right in zip(target_owner, nearest_owner)
        )
        counterexamples.append(
            {
                "floater": state["floater"],
                "masks": list(state["masks"]),
                "owner_distance": len(edges),
                "potential_gain": fraction_record(state_score - base_score),
                "components": component_records,
                "nearest_connected_bridge": {
                    "owner_distance_from_disconnected_rival": nearest_distance,
                    "floater": nearest_state["floater"],
                    "masks": list(nearest_state["masks"]),
                    "potential_gain": fraction_record(nearest_score - base_score),
                },
            }
        )
    return {
        "qualifying_two_positive_mutual_dependency_count": qualifying,
        "one_good_reroute_success_count": reroute_successes,
        "counterexamples": counterexamples,
    }


def run(directory: Path, output: Path) -> dict:
    profiles = {}
    for path in sorted(directory.glob("*.json")):
        if path.name == "partial_hall_two_positive_reroute_corpus_search.json":
            continue
        try:
            document = json.loads(path.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        for values in recognized_values(document):
            primitive = primitive_profile(values)
            digest = hashlib.sha256(
                json.dumps(primitive, separators=(",", ":")).encode()
            ).hexdigest()
            profiles.setdefault(digest, {"values": primitive, "sources": []})[
                "sources"
            ].append(str(path))
    obstruction_records = []
    for digest, profile in profiles.items():
        analysis = analyze(profile["values"])
        if analysis is None:
            continue
        obstruction_records.append(
            {
                "value_sha256": digest,
                "sources": profile["sources"],
                "values": [list(row) for row in profile["values"]],
                **analysis,
            }
        )
    counterexample_count = sum(
        len(record["counterexamples"]) for record in obstruction_records
    )
    bridge_distances = [
        counterexample["nearest_connected_bridge"][
            "owner_distance_from_disconnected_rival"
        ]
        for record in obstruction_records
        for counterexample in record["counterexamples"]
    ]
    artifact = {
        "schema": "partial-hall-two-positive-reroute-search-v1",
        "status": (
            "REFUTED" if counterexample_count else "NO_COUNTEREXAMPLE_IN_CORPUS"
        ),
        "meaning": (
            "Exact stored-corpus search for a canonical Hall obstruction with "
            "an improving distance-at-most-five rival having two positive, "
            "parked, non-EFX transfer components but no connected eligible "
            "improving one-good reroute. Absence is corpus evidence only."
        ),
        "directory": str(directory),
        "distinct_positive_4x9_profile_count": len(profiles),
        "canonical_hall_obstruction_profile_count": len(obstruction_records),
        "qualifying_rival_count": sum(
            record["qualifying_two_positive_mutual_dependency_count"]
            for record in obstruction_records
        ),
        "one_good_reroute_success_count": sum(
            record["one_good_reroute_success_count"]
            for record in obstruction_records
        ),
        "counterexample_count": counterexample_count,
        "maximum_counterexample_bridge_distance": (
            max(bridge_distances) if bridge_distances else None
        ),
        "counterexamples_requiring_more_than_two_reroutes": sum(
            distance > 2 for distance in bridge_distances
        ),
        "records": obstruction_records,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.directory, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
