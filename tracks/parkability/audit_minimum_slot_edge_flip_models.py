#!/usr/bin/env python3
"""Globally audit SAT valuations from Hamming-one host-edge cells."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit, masks_from_bundles
    from .run_minimum_slot_orbit_cegar import BASE, FLOATER, PAIR_HALL_CYCLE, TOKENS, global_landscape
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit, masks_from_bundles
    from run_minimum_slot_orbit_cegar import BASE, FLOATER, PAIR_HALL_CYCLE, TOKENS, global_landscape


SCHEMA = "minimum-slot-edge-flip-model-global-audit-v1"
BASE_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def run(source, output):
    document = json.loads(source.read_text())
    diagonal_order = [
        (host, observer)
        for host, pair in enumerate(PAIR_HALL_CYCLE)
        for observer in sorted(set(range(4)) - set(pair))
    ]
    bit_index = {entry: index for index, entry in enumerate(diagonal_order)}
    records = []
    for edge_record in document["records"]:
        if edge_record.get("flip_verdict") != "SAT" or edge_record.get("values") is None:
            continue
        if edge_record["assigned"] != edge_record["host"]:
            raise ValueError("persisted SAT model is not a diagonal edge flip")
        values = edge_record["values"]
        orbit = audit_orbit(values, BASE_STATE, TOKENS[:4], include_records=False)
        landscape, fixed, higher = global_landscape(
            values,
            witness_mode="hall_insertable",
        )
        bit = bit_index[(edge_record["host"], edge_record["observer"])]
        records.append(
            {
                "host": edge_record["host"],
                "observer": edge_record["observer"],
                "diagonal_bit": bit,
                "diagonal_pattern": 1 << bit,
                "values": values,
                "orbit_status": orbit["status"],
                "eligible_orbit_state_count": orbit["eligible_orbit_state_count"],
                "completing_orbit_state_count": orbit["completing_orbit_state_count"],
                "fixed_base_is_global_threshold_maximum": fixed is not None,
                "eligible_global_state_count": landscape["eligible_base_count"],
                "global_maximizer_count": landscape["maximizer_count"],
                "hall_insertable_global_maximizer_count": landscape[
                    "hall_insertable_maximizer_count"
                ],
                "nearest_higher_state": (
                    {**higher, "masks": list(higher["masks"])}
                    if higher is not None
                    else None
                ),
            }
        )
    all_blocked = all(
        record["orbit_status"] == "ORBIT_ALL_ELIGIBLE_STATES_BLOCKED"
        for record in records
    )
    any_global_counterexample = any(
        record["fixed_base_is_global_threshold_maximum"] for record in records
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "GLOBAL_MAXIMUM_BLOCKED_ORBIT_FOUND"
            if all_blocked and any_global_counterexample
            else "ALL_EDGE_FLIP_MODELS_BLOCKED_BUT_NONMAXIMAL"
            if all_blocked
            else "EDGE_FLIP_MODEL_AUDIT_FAILED"
        ),
        "meaning": (
            "Exact full-orbit and 589,824-state global-threshold audit of every "
            "persisted Hamming-one SAT valuation."
        ),
        "claim_boundary": (
            "Nonmaximal blocked models provide valid new global CEGAR cuts. A "
            "global counterexample status would refute only the fixed-core token-"
            "orbit theorem, not complete four-agent EFX, until independently replayed."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "model_count": len(records),
        "all_models_orbit_blocked": all_blocked,
        "global_maximum_blocked_model_count": sum(
            record["fixed_base_is_global_threshold_maximum"] for record in records
        ),
        "records": records,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
