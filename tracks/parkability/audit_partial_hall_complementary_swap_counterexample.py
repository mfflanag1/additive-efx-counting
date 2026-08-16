#!/usr/bin/env python3
"""Audit an exact counterexample to the eight-rival complementary-swap gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states
    from .audit_partial_hall_augmenting_exchange_topologies import (
        component_state_properties,
        owner_vector,
        transfers,
    )
    from .decide_partial_hall_complementary_swap_gate import RIVALS8
    from .search_partial_hall_two_positive_reroute import BASE_MASKS, BASE_FLOATER, hall_obstructed
except ImportError:
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states
    from audit_partial_hall_augmenting_exchange_topologies import (
        component_state_properties,
        owner_vector,
        transfers,
    )
    from decide_partial_hall_complementary_swap_gate import RIVALS8
    from search_partial_hall_two_positive_reroute import BASE_MASKS, BASE_FLOATER, hall_obstructed


def potential(values, masks) -> Fraction:
    return sum(
        (
            Fraction(
                sum(values[agent][good] for good in range(9) if masks[agent] & (1 << good)),
                sum(values[agent]),
            )
            for agent in range(4)
        ),
        Fraction(),
    )


def fraction_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    values = tuple(tuple(map(int, row)) for row in document["values"])
    base_owner = owner_vector(BASE_MASKS, BASE_FLOATER)
    base_efx, base_parked = component_state_properties(values, base_owner)
    hall_failure = hall_obstructed(values)
    base_score = potential(values, BASE_MASKS)
    states = enumerate_states(values)
    eligible = {(state["floater"], tuple(state["masks"])): state for state in states}
    rival_records = []
    for rival in RIVALS8:
        key = rival["floater"], tuple(rival["masks"])
        score = potential(values, key[1])
        rival_records.append(
            {
                "floater": key[0],
                "masks": list(key[1]),
                "eligible": key in eligible,
                "potential_gain": fraction_record(score - base_score),
                "eligible_and_improving": key in eligible and score > base_score,
            }
        )
    sum_gain = (
        Fraction(values[0][0] + values[0][4] - values[0][6] - values[0][7], sum(values[0]))
        + Fraction(values[2][6] + values[2][7] - values[2][0] - values[2][4], sum(values[2]))
    )
    improving = []
    for state in states:
        score = sum(state["normalized"], Fraction())
        if score <= base_score:
            continue
        target_owner = owner_vector(tuple(state["masks"]), state["floater"])
        distance = len(transfers(base_owner, target_owner))
        if distance <= 5:
            improving.append((score - base_score, distance, state))
    improving.sort(key=lambda item: (-item[0], item[1], item[2]["floater"], tuple(item[2]["masks"])))
    status = (
        "VERIFIED_COUNTEREXAMPLE"
        if base_efx
        and base_parked
        and hall_failure
        and sum_gain > 0
        and not any(record["eligible_and_improving"] for record in rival_records)
        else "FAILED_AUDIT"
    )
    artifact = {
        "schema": "partial-hall-complementary-swap-counterexample-audit-v1",
        "status": status,
        "meaning": (
            "A verified counterexample refutes only the fixed eight-rival "
            "positive-sum conversion. It does not refute the radius-five "
            "improvement theorem or complete additive EFX."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "base_efx": base_efx,
        "base_floater_nonenvy": base_parked,
        "radius_one_hall_obstruction": hall_failure,
        "complementary_swap_sum_gain": fraction_record(sum_gain),
        "rivals": rival_records,
        "eligible_improving_rival_count_within_radius_five": len(improving),
        "best_improving_rival": (
            {
                "potential_gain": fraction_record(improving[0][0]),
                "owner_distance": improving[0][1],
                "floater": improving[0][2]["floater"],
                "masks": list(improving[0][2]["masks"]),
            }
            if improving else None
        ),
    }
    if status != "VERIFIED_COUNTEREXAMPLE":
        raise AssertionError("eight-rival counterexample audit failed")
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
