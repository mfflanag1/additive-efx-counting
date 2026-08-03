#!/usr/bin/env python3
"""Cross-check the symbolic Hall blocker against explicit perfect matchings."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import (
        bundles_from_masks,
        minimum_slot_orbit_states,
    )
    from .run_minimum_slot_orbit_cegar import (
        efx_edge,
        hall_matching_failure,
        numeric_complete_edges,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import bundles_from_masks, minimum_slot_orbit_states
    from run_minimum_slot_orbit_cegar import (
        efx_edge,
        hall_matching_failure,
        numeric_complete_edges,
    )


SCHEMA = "minimum-slot-hall-encoding-audit-v2"
BASE_STATE = {"floater": 8, "masks": (3, 12, 48, 192)}
MINIMA = (1, 3, 5, 7)


def explicit_matching_exists(edges):
    return any(
        all(edges[observer][assigned] for observer, assigned in enumerate(permutation))
        for permutation in itertools.permutations(range(4))
    )


def symbolic_matching_failure(values, complete, prefix):
    symbolic_values = [
        [z3.RealVal(entry) for entry in row]
        for row in values
    ]
    solver = z3.Solver()
    solver.add(hall_matching_failure(symbolic_values, complete, prefix))
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError(f"Hall encoding returned unknown: {solver.reason_unknown()}")
    return result == z3.sat


def symbolic_enumerated_matching_failure(values, complete):
    symbolic_values = [
        [z3.RealVal(entry) for entry in row]
        for row in values
    ]
    formula = z3.And(
        *(
            z3.Or(
                *(
                    z3.Not(
                        efx_edge(
                            symbolic_values,
                            complete,
                            observer,
                            permutation[observer],
                        )
                    )
                    for observer in range(4)
                )
            )
            for permutation in itertools.permutations(range(4))
        )
    )
    solver = z3.Solver()
    solver.add(formula)
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError(
            f"enumerated matching encoding returned unknown: {solver.reason_unknown()}"
        )
    return result == z3.sat


def audit_profile(name, values, source=None):
    mismatches = []
    host_checks = 0
    explicit_failures = 0
    hall_symbolic_failures = 0
    enumerated_symbolic_failures = 0
    for state_index, state in enumerate(
        minimum_slot_orbit_states(values, BASE_STATE, MINIMA)
    ):
        bundles = bundles_from_masks(state["masks"], 9)
        for host in range(4):
            complete = list(bundles)
            complete[host] = tuple(sorted((*complete[host], state["floater"])))
            edges = numeric_complete_edges(values, complete)
            explicit_failure = not explicit_matching_exists(edges)
            hall_symbolic_failure = symbolic_matching_failure(
                values,
                complete,
                f"audit_{name}_{state_index}_{host}",
            )
            enumerated_symbolic_failure = symbolic_enumerated_matching_failure(
                values,
                complete,
            )
            host_checks += 1
            explicit_failures += int(explicit_failure)
            hall_symbolic_failures += int(hall_symbolic_failure)
            enumerated_symbolic_failures += int(enumerated_symbolic_failure)
            if not (
                explicit_failure
                == hall_symbolic_failure
                == enumerated_symbolic_failure
            ):
                mismatches.append(
                    {
                        "assignment": list(state["assignment"]),
                        "host": host,
                        "edges": [list(row) for row in edges],
                        "explicit_failure": explicit_failure,
                        "hall_symbolic_failure": hall_symbolic_failure,
                        "enumerated_symbolic_failure": enumerated_symbolic_failure,
                    }
                )
    record = {
        "name": name,
        "orbit_state_count": 120,
        "host_check_count": host_checks,
        "explicit_failure_count": explicit_failures,
        "hall_symbolic_failure_count": hall_symbolic_failures,
        "enumerated_symbolic_failure_count": enumerated_symbolic_failures,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }
    if source is not None:
        record["source"] = str(source)
        record["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    return record


def run(source, output):
    source_document = json.loads(source.read_text())
    source_values = source_document.get("values", source_document)
    profiles = [
        audit_profile("all_ones", [[1] * 9 for _ in range(4)]),
        audit_profile("blocked_boundary", source_values, source),
    ]
    mismatch_count = sum(profile["mismatch_count"] for profile in profiles)
    result = {
        "schema": SCHEMA,
        "status": "EXACT_MATCH" if mismatch_count == 0 else "MISMATCH",
        "meaning": (
            "The compact symbolic Hall-failure formula and the auxiliary-free "
            "24-matching blocker both agree with explicit perfect-matching "
            "enumeration for every host completion of all 120 token-orbit states "
            "in both audit profiles."
        ),
        "claim_boundary": (
            "This validates the encoding on two exact profiles; it is not an "
            "EFX-existence theorem or a formal proof of the encoding for all inputs."
        ),
        "profile_count": len(profiles),
        "host_check_count": sum(profile["host_check_count"] for profile in profiles),
        "mismatch_count": mismatch_count,
        "profiles": profiles,
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
