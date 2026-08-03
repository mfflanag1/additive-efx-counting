#!/usr/bin/env python3
"""CEGAR for a forced improving swap in one diagonal host-edge cell."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit, bundles_from_masks, masks_from_bundles
    from .decide_threshold_hall_local_gradient import eligible, integer_values
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        numeric_complete_edges,
        orbit_bundles,
        orbit_completion_failure,
        local_pair_exchange_states,
        theta,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit, bundles_from_masks, masks_from_bundles
    from decide_threshold_hall_local_gradient import eligible, integer_values
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        numeric_complete_edges,
        orbit_bundles,
        orbit_completion_failure,
        local_pair_exchange_states,
        theta,
    )


SCHEMA = "minimum-slot-diagonal-swap-cegar-v1"
BASE_STATE = {"floater": FLOATER, "masks": masks_from_bundles(BASE)}


def run(
    source,
    initial_values_source,
    pattern,
    floater,
    masks,
    output,
    timeout_seconds,
    max_iterations,
    batch_size,
    candidate_mode,
    completion_cut_mode,
):
    source_document = json.loads(source.read_text())
    source_values = source_document.get("values", source_document)
    initial_document = json.loads(initial_values_source.read_text())
    initial_values = initial_document.get("values", initial_document)
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for initial_row, row in zip(initial_values, values):
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
        row_total = sum(int(entry) for entry in initial_row)
        for initial_entry, entry in zip(initial_row, row):
            solver.set_initial_value(entry, z3.Q(int(initial_entry), row_total))
    solver.add(eligible(values, BASE, FLOATER))
    for owner, (core, token) in enumerate(zip((0, 2, 4, 6), TOKENS[:4])):
        solver.add(values[owner][token] < values[owner][core])

    diagonal_order = []
    for host, pair in enumerate(PAIR_HALL_CYCLE):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], FLOATER)))
        source_edges = numeric_complete_edges(source_values, complete)
        for observer in pair:
            for assigned in range(4):
                solver.add(
                    efx_edge(values, complete, observer, assigned)
                    == (assigned == host)
                )
        for observer in sorted(set(range(4)) - set(pair)):
            bit = len(diagonal_order)
            for assigned in range(4):
                expected = (
                    bool(pattern & (1 << bit))
                    if assigned == host
                    else source_edges[observer][assigned]
                )
                solver.add(efx_edge(values, complete, observer, assigned) == expected)
            diagonal_order.append([host, observer])

    if candidate_mode == "named":
        candidate_states = [{"floater": floater, "masks": tuple(masks)}]
    else:
        max_distance = 2 if candidate_mode == "distance2" else 3
        candidate_states = [
            {"floater": state["floater"], "masks": tuple(state["masks"])}
            for state in local_pair_exchange_states(max_distance)
        ]
    for state in candidate_states:
        candidate = bundles_from_masks(state["masks"], 9)
        solver.add(
            z3.Or(
                z3.Not(eligible(values, candidate, state["floater"])),
                theta(values, candidate) <= theta(values, BASE),
            )
        )

    orbit_cuts = []
    orbit_cut_keys = set()
    for record in initial_document.get("orbit_cuts", ()):
        assignment = tuple(int(good) for good in record["assignment"])
        if assignment in orbit_cut_keys:
            continue
        orbit_cut_keys.add(assignment)
        orbit_cuts.append({"assignment": list(assignment)})
        bundles = orbit_bundles(assignment)
        solver.add(
            z3.Implies(
                eligible(values, bundles, assignment[4]),
                orbit_completion_failure(values, assignment, completion_cut_mode),
            )
        )
    last_values = None
    last_orbit = None
    status = "ITERATION_LIMIT"
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        verdict = solver.check()
        if verdict == z3.unsat:
            status = "FORCED_ELIGIBLE_STRICT_IMPROVEMENT"
            break
        if verdict == z3.unknown:
            status = "UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        last_values = integer_values(solver.model(), values)
        last_orbit = audit_orbit(
            last_values,
            BASE_STATE,
            TOKENS[:4],
            include_records=True,
        )
        completing = [
            record for record in last_orbit["records"] if record["completing"]
        ]
        if not completing:
            status = "BLOCKED_NONIMPROVING_SWAP_COUNTERMODEL"
            break
        added = 0
        for record in completing:
            assignment = tuple(int(good) for good in record["assignment"])
            if assignment in orbit_cut_keys:
                continue
            orbit_cut_keys.add(assignment)
            orbit_cuts.append({"assignment": list(assignment)})
            bundles = orbit_bundles(assignment)
            solver.add(
                z3.Implies(
                    eligible(values, bundles, assignment[4]),
                    orbit_completion_failure(values, assignment, completion_cut_mode),
                )
            )
            added += 1
            if added >= batch_size:
                break
        if not added:
            raise AssertionError("repeated completing orbit state")
        atomic_json(
            output,
            {
                "schema": SCHEMA,
                "status": "IN_PROGRESS",
                "iteration": iteration,
                "diagonal_pattern": pattern,
                "candidate_mode": candidate_mode,
                "completion_cut_mode": completion_cut_mode,
                "candidate_states": [
                    {"floater": state["floater"], "masks": list(state["masks"])}
                    for state in candidate_states
                ],
                "orbit_cut_count": len(orbit_cuts),
                "orbit_cuts": orbit_cuts,
                "values": last_values,
                "orbit_audit": last_orbit,
            },
        )

    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact CEGAR for whether failure of the selected improving-state menu can coexist "
            "with simultaneous blockage of the complete 120-state token orbit."
        ),
        "claim_boundary": (
            "FORCED status proves the selected menu lemma only in one fixed diagonal "
            "edge cell. COUNTERMODEL refutes only that menu lemma, not the "
            "global-improvement alternative or four-agent EFX."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "initial_values_source": str(initial_values_source),
        "diagonal_pattern": pattern,
        "diagonal_edge_order": diagonal_order,
        "candidate_mode": candidate_mode,
        "completion_cut_mode": completion_cut_mode,
        "candidate_states": [
            {"floater": state["floater"], "masks": list(state["masks"])}
            for state in candidate_states
        ],
        "iterations": iteration,
        "max_iterations": max_iterations,
        "timeout_seconds_per_check": timeout_seconds,
        "batch_size": batch_size,
        "orbit_cut_count": len(orbit_cuts),
        "orbit_cuts": orbit_cuts,
        "solver_reason_unknown": reason_unknown,
        "values": last_values,
        "orbit_audit": last_orbit,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--initial-values", type=Path, required=True)
    parser.add_argument("--pattern", type=int, required=True)
    parser.add_argument("--floater", type=int, required=True)
    parser.add_argument("--masks")
    parser.add_argument(
        "--candidate-mode",
        choices=("named", "distance2", "radius3"),
        default="named",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument(
        "--completion-cut-mode",
        choices=("orbit_matching", "orbit_hall"),
        default="orbit_matching",
    )
    args = parser.parse_args()
    if args.candidate_mode == "named" and args.masks is None:
        parser.error("--masks is required for named candidate mode")
    masks = (
        tuple(int(mask) for mask in args.masks.split(","))
        if args.masks is not None
        else ()
    )
    result = run(
        args.source,
        args.initial_values,
        args.pattern,
        args.floater,
        masks,
        args.output,
        args.timeout_seconds,
        args.max_iterations,
        args.batch_size,
        args.candidate_mode,
        args.completion_cut_mode,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "schema",
                    "status",
                    "iterations",
                    "orbit_cut_count",
                    "solver_reason_unknown",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
