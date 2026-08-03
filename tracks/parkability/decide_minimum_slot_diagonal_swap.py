#!/usr/bin/env python3
"""Decide a canonical improving swap in a diagonal host-edge cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import bundles_from_masks
    from .decide_threshold_hall_local_gradient import eligible, integer_values
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        numeric_complete_edges,
        orbit_bundles,
        orbit_matching_failure,
        theta,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import bundles_from_masks
    from decide_threshold_hall_local_gradient import eligible, integer_values
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        numeric_complete_edges,
        orbit_bundles,
        orbit_matching_failure,
        theta,
    )


SCHEMA = "minimum-slot-diagonal-swap-decision-v1"


def run(
    source,
    pattern,
    floater,
    masks,
    output,
    timeout_seconds,
    solver_profile,
    include_orbit_blockers=True,
):
    source_document = json.loads(source.read_text())
    source_values = source_document.get("values", source_document)
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.SolverFor("QF_LRA") if solver_profile == "qf_lra" else z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for source_row, row in zip(source_values, values):
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
        row_total = sum(int(entry) for entry in source_row)
        for source_entry, entry in zip(source_row, row):
            solver.set_initial_value(entry, z3.Q(int(source_entry), row_total))
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
                solver.add(
                    efx_edge(values, complete, observer, assigned) == expected
                )
            diagonal_order.append([host, observer])

    if include_orbit_blockers:
        for assignment in itertools.permutations(TOKENS):
            bundles = orbit_bundles(assignment)
            solver.add(
                z3.Implies(
                    eligible(values, bundles, assignment[4]),
                    orbit_matching_failure(values, assignment),
                )
            )

    candidate = bundles_from_masks(masks, 9)
    solver.add(
        z3.Or(
            z3.Not(eligible(values, candidate, floater)),
            theta(values, candidate) <= theta(values, BASE),
        )
    )
    verdict = solver.check()
    reason_unknown = solver.reason_unknown() if verdict == z3.unknown else None
    result = {
        "schema": SCHEMA,
        "status": (
            "FORCED_ELIGIBLE_STRICT_IMPROVEMENT"
            if verdict == z3.unsat
            else "NONIMPROVING_OR_INELIGIBLE_COUNTERMODEL"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "Exact decision of whether simultaneous blockage of all 120 token "
            "states forces one named allocation to be eligible and strictly improve "
            "normalized owner-threshold potential."
        ),
        "claim_boundary": (
            "UNSAT proves the named swap lemma only inside one fixed diagonal-pattern "
            "host-edge cell. It does not prove the eight-switch family, pair-Hall "
            "cell, arbitrary-core lemma, or four-agent EFX."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "diagonal_pattern": pattern,
        "diagonal_edge_order": diagonal_order,
        "candidate": {"floater": floater, "masks": list(masks)},
        "timeout_seconds": timeout_seconds,
        "solver_profile": solver_profile,
        "all_orbit_blockers_included": include_orbit_blockers,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": reason_unknown,
        "values": integer_values(solver.model(), values) if verdict == z3.sat else None,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--pattern", type=int, required=True)
    parser.add_argument("--floater", type=int, required=True)
    parser.add_argument("--masks", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--solver-profile", choices=("default", "qf_lra"), default="default")
    parser.add_argument("--omit-orbit-blockers", action="store_true")
    args = parser.parse_args()
    masks = tuple(int(mask) for mask in args.masks.split(","))
    result = run(
        args.source,
        args.pattern,
        args.floater,
        masks,
        args.output,
        args.timeout_seconds,
        args.solver_profile,
        not args.omit_orbit_blockers,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
