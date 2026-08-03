#!/usr/bin/env python3
"""Exact local-exchange audit around the canonical four-pair base."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit, exact_eligible, exact_theta
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        TOKENS,
        global_landscape,
        local_pair_exchange_states,
        masks_from_bundles,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit, exact_eligible, exact_theta
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        TOKENS,
        global_landscape,
        local_pair_exchange_states,
        masks_from_bundles,
    )


SCHEMA = "minimum-slot-local-exchange-radius-audit-v1"
FIXED_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def state_record(state, gain):
    return {
        "floater": state["floater"],
        "masks": list(state["masks"]),
        "owner_distance": state["owner_distance"],
        "threshold_gain": str(gain),
    }


def run(values_path, output_path):
    document = json.loads(values_path.read_text())
    values = document.get("values", document)
    fixed_theta = exact_theta(values, FIXED_STATE)
    local_states = local_pair_exchange_states(3)
    distance_two_state_count = sum(
        state["owner_distance"] == 2 for state in local_states
    )
    records = []
    for state in local_states:
        if not exact_eligible(values, state):
            continue
        gain = exact_theta(values, state) - fixed_theta
        records.append(state_record(state, gain))

    improving = [
        record
        for record in records
        if Fraction(record["threshold_gain"]) > 0
    ]
    nearest_distance = min(
        (record["owner_distance"] for record in improving),
        default=None,
    )
    nearest = sorted(
        (
            record
            for record in improving
            if record["owner_distance"] == nearest_distance
        ),
        key=lambda record: (
            Fraction(record["threshold_gain"]),
            record["floater"],
            record["masks"],
        ),
    )

    landscape, fixed, global_nearest = global_landscape(values)
    orbit = audit_orbit(values, FIXED_STATE, TOKENS[:4], include_records=False)
    result = {
        "schema": SCHEMA,
        "status": (
            "THREE_CYCLE_NECESSARY"
            if nearest_distance == 3
            else "DISTANCE_TWO_IMPROVEMENT"
            if nearest_distance == 2
            else "NO_RADIUS_THREE_IMPROVEMENT"
        ),
        "meaning": (
            "Exact audit of all balanced pair states at owner-assignment "
            "distance two or three from the canonical base."
        ),
        "claim_boundary": (
            "THREE_CYCLE_NECESSARY proves that no eligible positive-threshold "
            "two-slot exchange exists for this valuation, while at least one "
            "positive three-slot cycle exists. It is not an EFX counterexample."
        ),
        "values_path": str(values_path),
        "values_sha256": hashlib.sha256(values_path.read_bytes()).hexdigest(),
        "fixed_state": {
            "floater": FIXED_STATE["floater"],
            "masks": list(FIXED_STATE["masks"]),
        },
        "fixed_theta": str(fixed_theta),
        "orbit_status": orbit["status"],
        "eligible_orbit_state_count": orbit["eligible_orbit_state_count"],
        "completing_orbit_state_count": orbit["completing_orbit_state_count"],
        "local_state_count": len(local_states),
        "distance_two_state_count": distance_two_state_count,
        "distance_three_state_count": len(local_states)
        - distance_two_state_count,
        "eligible_local_state_count": len(records),
        "improving_local_state_count": len(improving),
        "improving_distance_counts": {
            str(distance): sum(
                record["owner_distance"] == distance for record in improving
            )
            for distance in (2, 3)
        },
        "nearest_improving_distance": nearest_distance,
        "nearest_improving_states": nearest,
        "fixed_base_is_global_threshold_maximum": fixed is not None,
        "global_maximizer_count": landscape["maximizer_count"],
        "global_nearest_higher_state": global_nearest,
        "eligible_local_states": records,
    }
    if global_nearest is not None and nearest:
        expected = (
            global_nearest["floater"],
            list(global_nearest["masks"]),
            global_nearest["owner_distance"],
        )
        observed = (
            nearest[0]["floater"],
            nearest[0]["masks"],
            nearest[0]["owner_distance"],
        )
        if expected != observed:
            raise AssertionError((expected, observed))
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.values, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
