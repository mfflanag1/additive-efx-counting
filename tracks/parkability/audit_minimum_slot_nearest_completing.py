#!/usr/bin/env python3
"""Audit nearest higher Hall-completable states for blocked-orbit landmarks."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_nearest_exchange_components import transfer_components
    from .run_minimum_slot_orbit_cegar import (
        global_landscape,
        owner_assignment,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_nearest_exchange_components import transfer_components
    from run_minimum_slot_orbit_cegar import global_landscape, owner_assignment


SCHEMA = "minimum-slot-nearest-completing-landmark-audit-v1"
BASE_STATE = {"floater": 8, "masks": (3, 12, 48, 192)}


def run(sources, output):
    base_assignment = owner_assignment(BASE_STATE)
    records = []
    for source in sources:
        document = json.loads(source.read_text())
        values = document["values"]
        orbit = document["orbit_audit"]
        if orbit["status"] != "ORBIT_ALL_ELIGIBLE_STATES_BLOCKED":
            raise ValueError(f"source orbit is not blocked: {source}")
        landscape, fixed, higher = global_landscape(
            values,
            witness_mode="hall_insertable",
        )
        if fixed is not None:
            raise ValueError(f"source base is already globally maximal: {source}")
        state = {
            "floater": higher["floater"],
            "masks": tuple(higher["masks"]),
        }
        components = transfer_components(
            base_assignment,
            owner_assignment(state),
        )
        records.append(
            {
                "source": str(source),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "eligible_orbit_state_count": orbit[
                    "eligible_orbit_state_count"
                ],
                "global_maximizer_count": landscape["maximizer_count"],
                "higher_state": {
                    **higher,
                    "masks": list(higher["masks"]),
                },
                "transfer_component_count": len(components),
                "transfer_components": components,
            }
        )
    all_completing = all(
        record["higher_state"]["hall_insertable"] for record in records
    )
    all_connected = all(
        record["transfer_component_count"] == 1 for record in records
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_LANDMARKS_HAVE_CONNECTED_COMPLETING_IMPROVER"
            if all_completing and all_connected
            else "LANDMARK_PROPERTY_FAILED"
        ),
        "meaning": (
            "Exact replay of the nearest higher Hall-completable allocation "
            "for selected blocked-orbit landmark valuations."
        ),
        "claim_boundary": (
            "This is finite landmark evidence, not a proof that every blocked "
            "orbit has a connected completing improver."
        ),
        "landmark_count": len(records),
        "all_have_hall_completing_higher_state": all_completing,
        "all_selected_higher_states_connected": all_connected,
        "records": records,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
