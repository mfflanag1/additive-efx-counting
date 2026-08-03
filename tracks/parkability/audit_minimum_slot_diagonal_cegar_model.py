#!/usr/bin/env python3
"""Exactly audit a diagonal-cell CEGAR countermodel and its global escape."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import (
        audit_orbit,
        exact_eligible,
        exact_theta,
        masks_from_bundles,
    )
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        TOKENS,
        global_landscape,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import (
        audit_orbit,
        exact_eligible,
        exact_theta,
        masks_from_bundles,
    )
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        TOKENS,
        global_landscape,
    )


SCHEMA = "minimum-slot-diagonal-cegar-model-audit-v1"
BASE_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def run(source: Path, output: Path):
    document = json.loads(source.read_text())
    if document.get("status") != "BLOCKED_NONIMPROVING_SWAP_COUNTERMODEL":
        raise ValueError("source is not a completed CEGAR countermodel")
    values = document["values"]
    base_theta = exact_theta(values, BASE_STATE)
    candidate_records = []
    for candidate in document["candidate_states"]:
        state = {
            "floater": int(candidate["floater"]),
            "masks": tuple(int(mask) for mask in candidate["masks"]),
        }
        eligible = exact_eligible(values, state)
        candidate_theta = exact_theta(values, state)
        candidate_records.append(
            {
                "floater": state["floater"],
                "masks": list(state["masks"]),
                "eligible": eligible,
                "theta": str(candidate_theta),
                "strictly_improves": eligible and candidate_theta > base_theta,
            }
        )
    orbit = audit_orbit(values, BASE_STATE, TOKENS[:4], include_records=False)
    landscape, fixed, higher = global_landscape(
        values,
        witness_mode="hall_insertable",
    )
    no_candidate_improves = not any(
        record["strictly_improves"] for record in candidate_records
    )
    orbit_blocked = orbit["completing_orbit_state_count"] == 0
    result = {
        "schema": SCHEMA,
        "status": (
            "EXACT_BLOCKED_MENU_COUNTERMODEL_NONMAXIMAL"
            if orbit_blocked and no_candidate_improves and fixed is None
            else "EXACT_BLOCKED_MENU_COUNTERMODEL_GLOBAL_MAXIMUM"
            if orbit_blocked and no_candidate_improves
            else "AUDIT_FAILED"
        ),
        "meaning": (
            "Exact rational replay of the selected exchange menu, all 120 fixed-core "
            "token states, and the complete 589,824-state threshold landscape."
        ),
        "claim_boundary": (
            "A nonmaximal result refutes only this finite exchange menu in this fixed "
            "diagonal edge cell. It does not refute the global-improvement alternative, "
            "the fixed-core theorem, or four-agent EFX."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "diagonal_pattern": document["diagonal_pattern"],
        "candidate_mode": document["candidate_mode"],
        "candidate_count": len(candidate_records),
        "candidate_strict_improvement_count": sum(
            record["strictly_improves"] for record in candidate_records
        ),
        "base_theta": str(base_theta),
        "orbit_status": orbit["status"],
        "eligible_orbit_state_count": orbit["eligible_orbit_state_count"],
        "completing_orbit_state_count": orbit["completing_orbit_state_count"],
        "fixed_base_is_global_threshold_maximum": fixed is not None,
        "eligible_global_state_count": landscape["eligible_base_count"],
        "global_maximizer_count": landscape["maximizer_count"],
        "hall_insertable_global_maximizer_count": landscape[
            "hall_insertable_maximizer_count"
        ],
        "nearest_higher_hall_insertable_state": (
            {**higher, "masks": list(higher["masks"])}
            if higher is not None
            else None
        ),
        "candidate_records": candidate_records,
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
