#!/usr/bin/env python3
"""Exactly audit a SAT model for the finite cyclic pair-Hall cut pool."""

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
    from .audit_threshold_plateau_exact_paths import exact_best_hall_margin
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        global_landscape,
        numeric_complete_edges,
        orbit_bundles,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import (
        audit_orbit,
        exact_eligible,
        exact_theta,
        masks_from_bundles,
    )
    from audit_threshold_plateau_exact_paths import exact_best_hall_margin
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        global_landscape,
        numeric_complete_edges,
        orbit_bundles,
    )


SCHEMA = "minimum-slot-pair-cycle-pool-model-audit-v1"
BASE_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(pool_path, values_path, output_path):
    pool = json.loads(pool_path.read_text())
    values_document = json.loads(values_path.read_text())
    values = values_document.get("values", values_document)
    base_theta = exact_theta(values, BASE_STATE)

    positive = all(entry > 0 for row in values for entry in row)
    base_eligible = exact_eligible(values, BASE_STATE)
    unique_minima = all(
        values[owner][TOKENS[owner]] < values[owner][2 * owner]
        for owner in range(4)
    )

    edge_records = []
    pair_cycle_holds = True
    for host, observers in enumerate(PAIR_HALL_CYCLE):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], FLOATER)))
        edges = numeric_complete_edges(values, complete)
        host_holds = all(
            edges[observer][assigned] == (assigned == host)
            for observer in observers
            for assigned in range(4)
        )
        pair_cycle_holds &= host_holds
        edge_records.append(
            {
                "host": host,
                "deficient_pair": list(observers),
                "pair_condition_holds": host_holds,
                "edges": [list(row) for row in edges],
            }
        )

    global_cut_violations = []
    for index, cut in enumerate(pool["global_cuts"]):
        state = {
            "floater": int(cut["floater"]),
            "masks": tuple(int(mask) for mask in cut["masks"]),
        }
        if exact_eligible(values, state) and exact_theta(values, state) > base_theta:
            global_cut_violations.append(index)

    orbit_cut_violations = []
    for index, cut in enumerate(pool["orbit_hall_cuts"]):
        assignment = tuple(int(good) for good in cut["assignment"])
        state = {
            "floater": assignment[4],
            "masks": masks_from_bundles(orbit_bundles(assignment)),
        }
        if not exact_eligible(values, state):
            continue
        margin, host, permutation, _bottlenecks = exact_best_hall_margin(values, state)
        if margin >= 0:
            orbit_cut_violations.append(
                {
                    "index": index,
                    "assignment": list(assignment),
                    "margin": str(margin),
                    "host": host,
                    "permutation": list(permutation),
                }
            )

    cut_pool_valid = all(
        (
            positive,
            base_eligible,
            unique_minima,
            pair_cycle_holds,
            not global_cut_violations,
            not orbit_cut_violations,
        )
    )
    orbit = audit_orbit(values, BASE_STATE, TOKENS[:4], include_records=False)
    landscape, fixed, higher = global_landscape(
        values,
        witness_mode="hall_insertable",
    )
    result = {
        "schema": SCHEMA,
        "status": "FINITE_POOL_SAT_REPLAYED" if cut_pool_valid else "POOL_MODEL_INVALID",
        "meaning": (
            "Exact rational replay of the batch-Z3 model against every persisted "
            "global cut, orbit blocker, and cyclic pair-Hall edge condition."
        ),
        "claim_boundary": (
            "A valid finite-pool model only identifies missing CEGAR cuts. It "
            "refutes the full pair-Hall theorem only if the full orbit is blocked "
            "and the canonical base is a true global threshold maximum."
        ),
        "pool": str(pool_path),
        "pool_sha256": sha256(pool_path),
        "values": str(values_path),
        "values_sha256": sha256(values_path),
        "positive": positive,
        "base_eligible": base_eligible,
        "strict_owner_minima": unique_minima,
        "pair_hall_cycle_holds": pair_cycle_holds,
        "host_edge_records": edge_records,
        "global_cut_count": len(pool["global_cuts"]),
        "global_cut_violation_count": len(global_cut_violations),
        "global_cut_violations": global_cut_violations,
        "orbit_cut_count": len(pool["orbit_hall_cuts"]),
        "orbit_cut_violation_count": len(orbit_cut_violations),
        "orbit_cut_violations": orbit_cut_violations,
        "full_orbit_audit": orbit,
        "full_global_audit": {
            "eligible_state_count": landscape["eligible_base_count"],
            "maximum_threshold_state_count": landscape["maximizer_count"],
            "hall_insertable_maximum_threshold_state_count": landscape[
                "hall_insertable_maximizer_count"
            ],
            "fixed_base_is_global_threshold_maximum": fixed is not None,
            "nearest_higher_state": (
                {**higher, "masks": list(higher["masks"])}
                if higher is not None
                else None
            ),
        },
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.pool, args.values, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
