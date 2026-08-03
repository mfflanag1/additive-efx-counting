#!/usr/bin/env python3
"""Classify token states inside the cyclic pair-Hall valuation cell."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_threshold_hall_local_gradient import eligible
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        orbit_bundles,
        orbit_matching_failure,
    )
except ImportError:
    from anneal import atomic_json
    from decide_threshold_hall_local_gradient import eligible
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        TOKENS,
        efx_edge,
        orbit_bundles,
        orbit_matching_failure,
    )


SCHEMA = "minimum-slot-pair-cycle-orbit-reachability-audit-v1"


def verdict_name(verdict):
    if verdict == z3.sat:
        return "SAT"
    if verdict == z3.unsat:
        return "UNSAT"
    return "UNKNOWN"


def run(output, timeout_seconds):
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for row in values:
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(eligible(values, BASE, FLOATER))
    for owner, (core, token) in enumerate(zip((0, 2, 4, 6), TOKENS[:4])):
        solver.add(values[owner][token] < values[owner][core])
    for host, observers in enumerate(PAIR_HALL_CYCLE):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], FLOATER)))
        for observer in observers:
            for assigned in range(4):
                solver.add(
                    efx_edge(values, complete, observer, assigned)
                    == (assigned == host)
                )

    records = []
    for assignment in itertools.permutations(TOKENS):
        bundles = orbit_bundles(assignment)
        state_eligible = eligible(values, bundles, assignment[4])

        solver.push()
        solver.add(state_eligible)
        eligible_verdict = solver.check()
        eligible_reason = solver.reason_unknown() if eligible_verdict == z3.unknown else None
        solver.pop()

        solver.push()
        solver.add(state_eligible)
        solver.add(orbit_matching_failure(values, assignment))
        blocked_verdict = solver.check()
        blocked_reason = solver.reason_unknown() if blocked_verdict == z3.unknown else None
        solver.pop()

        records.append(
            {
                "assignment": list(assignment),
                "eligible": verdict_name(eligible_verdict),
                "eligible_reason_unknown": eligible_reason,
                "eligible_and_completion_blocked": verdict_name(blocked_verdict),
                "blocked_reason_unknown": blocked_reason,
            }
        )

    status = (
        "ORBIT_REACHABILITY_CLASSIFIED"
        if all(
            record["eligible"] != "UNKNOWN"
            and record["eligible_and_completion_blocked"] != "UNKNOWN"
            for record in records
        )
        else "ORBIT_REACHABILITY_PARTIAL"
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact cell-relative satisfiability classification of eligibility "
            "and simultaneous four-host completion blockage for all 120 token states."
        ),
        "claim_boundary": (
            "Each SAT result may use a different valuation. The audit classifies "
            "individual states and does not decide whether all states can be blocked "
            "simultaneously at a global threshold maximum."
        ),
        "timeout_seconds_per_check": timeout_seconds,
        "orbit_state_count": len(records),
        "eligible_possible_count": sum(record["eligible"] == "SAT" for record in records),
        "eligible_impossible_count": sum(
            record["eligible"] == "UNSAT" for record in records
        ),
        "blocked_possible_count": sum(
            record["eligible_and_completion_blocked"] == "SAT" for record in records
        ),
        "blocked_impossible_count": sum(
            record["eligible_and_completion_blocked"] == "UNSAT" for record in records
        ),
        "unknown_check_count": sum(
            record["eligible"] == "UNKNOWN"
            or record["eligible_and_completion_blocked"] == "UNKNOWN"
            for record in records
        ),
        "records": records,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()
    result = run(args.output, args.timeout_seconds)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
