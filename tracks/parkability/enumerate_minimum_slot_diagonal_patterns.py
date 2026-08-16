#!/usr/bin/env python3
"""Enumerate feasible diagonal host-edge patterns in one off-host edge cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
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
    )
except ImportError:
    from anneal import atomic_json
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
    )


SCHEMA = "minimum-slot-diagonal-pattern-enumeration-v1"


def verdict_name(verdict):
    if verdict == z3.sat:
        return "SAT"
    if verdict == z3.unsat:
        return "UNSAT"
    return "UNKNOWN"


def run(source, output, timeout_seconds, max_patterns, completion_cut_mode, resume=None):
    source_document = json.loads(source.read_text())
    source_values = source_document.get("values", source_document)
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.Solver()
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

    diagonal_edges = []
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
            for assigned in range(4):
                edge = efx_edge(values, complete, observer, assigned)
                if assigned == host:
                    diagonal_order.append([host, observer])
                    diagonal_edges.append(edge)
                else:
                    solver.add(edge == bool(source_edges[observer][assigned]))

    for assignment in itertools.permutations(TOKENS):
        bundles = orbit_bundles(assignment)
        solver.add(
            z3.Implies(
                eligible(values, bundles, assignment[4]),
                orbit_completion_failure(values, assignment, completion_cut_mode),
            )
        )

    records = []
    if resume is not None:
        resume_document = json.loads(resume.read_text())
        records = list(resume_document.get("records", ()))
    seen = set()
    for record in records:
        pattern = int(record["diagonal_pattern"])
        if pattern in seen:
            raise ValueError("resume contains a duplicate diagonal pattern")
        seen.add(pattern)
        solver.add(
            z3.Or(
                *(
                    edge != bool(pattern & (1 << bit))
                    for bit, edge in enumerate(diagonal_edges)
                )
            )
        )

    status = "PATTERN_LIMIT"
    reason_unknown = None
    final_verdict = None
    while len(records) < max_patterns:
        verdict = solver.check()
        final_verdict = verdict_name(verdict)
        if verdict == z3.unsat:
            status = "ALL_FEASIBLE_PATTERNS_ENUMERATED"
            break
        if verdict == z3.unknown:
            status = "UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model = solver.model()
        pattern = sum(
            (1 << bit) * int(z3.is_true(model.eval(edge, model_completion=True)))
            for bit, edge in enumerate(diagonal_edges)
        )
        if pattern in seen:
            raise AssertionError("solver returned a blocked diagonal pattern")
        seen.add(pattern)
        records.append(
            {
                "diagonal_pattern": pattern,
                "diagonal_bits": [
                    int(bool(pattern & (1 << bit)))
                    for bit in range(len(diagonal_edges))
                ],
                "values": integer_values(model, values),
            }
        )
        solver.add(
            z3.Or(
                *(
                    edge != bool(pattern & (1 << bit))
                    for bit, edge in enumerate(diagonal_edges)
                )
            )
        )
        atomic_json(
            output,
            {
                "schema": SCHEMA,
                "status": "IN_PROGRESS",
                "source": str(source),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "completion_cut_mode": completion_cut_mode,
                "timeout_seconds_per_check": timeout_seconds,
                "diagonal_edge_order": diagonal_order,
                "record_count": len(records),
                "records": records,
            },
        )

    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact enumeration of diagonal host-edge truth patterns compatible with "
            "the fixed cyclic pair-Hall witnesses, the source's 24 off-host edges, "
            "and simultaneous blockage of all 120 fixed-core token states."
        ),
        "claim_boundary": (
            "The enumeration fixes the 24 off-host edge bits to one source profile. "
            "It does not classify the full pair-Hall cell or impose global threshold "
            "maximality. UNKNOWN and PATTERN_LIMIT are not completeness verdicts."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "completion_cut_mode": completion_cut_mode,
        "timeout_seconds_per_check": timeout_seconds,
        "max_patterns": max_patterns,
        "final_solver_verdict": final_verdict,
        "solver_reason_unknown": reason_unknown,
        "diagonal_edge_order": diagonal_order,
        "record_count": len(records),
        "records": records,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-patterns", type=int, default=256)
    parser.add_argument(
        "--completion-cut-mode",
        choices=("orbit_hall", "orbit_matching"),
        default="orbit_matching",
    )
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.timeout_seconds,
        args.max_patterns,
        args.completion_cut_mode,
        args.resume,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "schema",
                    "status",
                    "record_count",
                    "final_solver_verdict",
                    "solver_reason_unknown",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
