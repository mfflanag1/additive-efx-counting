#!/usr/bin/env python3
"""Audit the dominant complementary-swap identity on stored Hall obstructions."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states
    from .audit_partial_hall_augmenting_exchange_topologies import (
        component_state_properties,
        first_efx_violation,
        owner_vector,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states
    from audit_partial_hall_augmenting_exchange_topologies import (
        component_state_properties,
        first_efx_violation,
        owner_vector,
    )


BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8
SWAPS = (
    (8, (129, 14, 80, 32)),  # exchange goods 6 and 0
    (8, (80, 14, 129, 32)),  # exchange goods 7 and 4
)
REPAIRS = (
    (8, (65, 14, 144, 32)),
    (6, (272, 14, 129, 32)),
    (1, (81, 264, 132, 32)),
    (4, (320, 14, 129, 32)),
    (7, (257, 14, 80, 32)),
)
GATE_RIVALS = SWAPS + REPAIRS
EXTENDED_GATE_RIVALS = GATE_RIVALS + ((8, (144, 14, 65, 32)),)


def potential(values, masks) -> Fraction:
    return sum(
        (
            Fraction(
                sum(
                    values[agent][good]
                    for good in range(9)
                    if masks[agent] & (1 << good)
                ),
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
    records = []
    repair_template_counts = {}
    counts = {
        "profile_count": 0,
        "positive_sum_identity_count": 0,
        "first_swap_eligible_improving_count": 0,
        "second_swap_eligible_improving_count": 0,
        "either_swap_eligible_improving_count": 0,
        "positive_sum_but_missing_eligibility_count": 0,
        "positive_sum_seven_rival_gate_covered_count": 0,
        "positive_sum_seven_rival_gate_counterexample_count": 0,
        "positive_sum_eight_rival_gate_counterexample_count": 0,
    }
    for profile in document["records"]:
        values = tuple(tuple(row) for row in profile["values"])
        base_score = potential(values, BASE_MASKS)
        states = enumerate_states(values)
        eligible = {(state["floater"], tuple(state["masks"])) for state in states}
        deltas = [potential(values, masks) - base_score for _, masks in SWAPS]
        totals = tuple(map(sum, values))
        identity_rhs = (
            Fraction(values[0][0] + values[0][4] - values[0][6] - values[0][7], totals[0])
            + Fraction(values[2][6] + values[2][7] - values[2][0] - values[2][4], totals[2])
        )
        if sum(deltas, Fraction()) != identity_rhs:
            raise AssertionError("complementary-swap identity failed")
        eligible_improving = [
            SWAPS[index] in eligible and deltas[index] > 0 for index in range(2)
        ]
        gate_covered = any(
            rival in eligible and potential(values, rival[1]) > base_score
            for rival in GATE_RIVALS
        )
        extended_gate_covered = any(
            rival in eligible and potential(values, rival[1]) > base_score
            for rival in EXTENDED_GATE_RIVALS
        )
        swap_properties = []
        for floater, masks in SWAPS:
            owners = owner_vector(masks, floater)
            partial_efx, floater_nonenvy = component_state_properties(values, owners)
            swap_properties.append(
                {
                    "partial_efx": partial_efx,
                    "floater_nonenvy": floater_nonenvy,
                    "first_efx_violation": first_efx_violation(values, owners),
                }
            )
        nearest_repairs = []
        for index, (floater, masks) in enumerate(SWAPS):
            if deltas[index] <= 0 or (floater, masks) in eligible:
                nearest_repairs.append(None)
                continue
            swap_owner = owner_vector(masks, floater)
            improving_states = [
                state
                for state in states
                if sum(state["normalized"], Fraction()) > base_score
            ]
            nearest = min(
                improving_states,
                key=lambda state: sum(
                    left != right
                    for left, right in zip(
                        swap_owner,
                        owner_vector(tuple(state["masks"]), state["floater"]),
                    )
                ),
            )
            nearest_owner = owner_vector(tuple(nearest["masks"]), nearest["floater"])
            distance = sum(
                left != right for left, right in zip(swap_owner, nearest_owner)
            )
            key = f'{nearest["floater"]}:{",".join(map(str, nearest["masks"]))}'
            repair_template_counts[key] = repair_template_counts.get(key, 0) + 1
            nearest_repairs.append(
                {
                    "owner_distance_from_swap": distance,
                    "floater": nearest["floater"],
                    "masks": list(nearest["masks"]),
                    "potential_gain": fraction_record(
                        sum(nearest["normalized"], Fraction()) - base_score
                    ),
                }
            )
        counts["profile_count"] += 1
        counts["positive_sum_identity_count"] += identity_rhs > 0
        counts["first_swap_eligible_improving_count"] += eligible_improving[0]
        counts["second_swap_eligible_improving_count"] += eligible_improving[1]
        counts["either_swap_eligible_improving_count"] += any(eligible_improving)
        counts["positive_sum_but_missing_eligibility_count"] += (
            identity_rhs > 0 and not any(eligible_improving)
        )
        counts["positive_sum_seven_rival_gate_covered_count"] += (
            identity_rhs > 0 and gate_covered
        )
        counts["positive_sum_seven_rival_gate_counterexample_count"] += (
            identity_rhs > 0 and not gate_covered
        )
        counts["positive_sum_eight_rival_gate_counterexample_count"] += (
            identity_rhs > 0 and not extended_gate_covered
        )
        records.append(
            {
                "value_sha256": profile["value_sha256"],
                "swap_eligible": [swap in eligible for swap in SWAPS],
                "swap_properties": swap_properties,
                "nearest_eligible_improving_repairs": nearest_repairs,
                "swap_potential_gains": [fraction_record(delta) for delta in deltas],
                "sum_identity_rhs": fraction_record(identity_rhs),
                "either_swap_eligible_improving": any(eligible_improving),
                "seven_rival_gate_covered": gate_covered,
                "eight_rival_gate_covered": extended_gate_covered,
            }
        )
    artifact = {
        "schema": "partial-hall-complementary-swap-audit-v1",
        "status": "VERIFIED_IDENTITY",
        "meaning": (
            "Exact rational audit of the two complementary exchanges between "
            "canonical bundles 0 and 2. The identity is analytic; coverage "
            "counts are stored-corpus facts only."
        ),
        "source": str(source),
        "swaps": [
            {"floater": floater, "masks": list(masks)} for floater, masks in SWAPS
        ],
        **counts,
        "nearest_repair_template_counts": dict(sorted(repair_template_counts.items())),
        "records": records,
    }
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
