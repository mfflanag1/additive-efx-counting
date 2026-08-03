#!/usr/bin/env python3
"""Test free base-host edge bits under simultaneous token-orbit blockage."""

from __future__ import annotations

import argparse
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
        orbit_matching_failure,
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
        orbit_matching_failure,
    )


SCHEMA = "minimum-slot-pair-cycle-edge-flexibility-audit-v1"


def verdict_name(verdict):
    if verdict == z3.sat:
        return "SAT"
    if verdict == z3.unsat:
        return "UNSAT"
    return "UNKNOWN"


def run(source, output, timeout_seconds, flip_timeout_seconds, resume=None):
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

    completes = []
    source_edges = []
    for host, observers in enumerate(PAIR_HALL_CYCLE):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], FLOATER)))
        completes.append(complete)
        host_edges = numeric_complete_edges(source_values, complete)
        source_edges.append(host_edges)
        for observer in observers:
            for assigned in range(4):
                solver.add(
                    efx_edge(values, complete, observer, assigned)
                    == (assigned == host)
                )

    for assignment in itertools.permutations(TOKENS):
        bundles = orbit_bundles(assignment)
        solver.add(
            z3.Implies(
                eligible(values, bundles, assignment[4]),
                orbit_matching_failure(values, assignment),
            )
        )

    free_edges = []
    keep_literals = []
    for host, pair in enumerate(PAIR_HALL_CYCLE):
        for observer in sorted(set(range(4)) - set(pair)):
            for assigned in range(4):
                expected = bool(source_edges[host][observer][assigned])
                edge = efx_edge(
                    values,
                    completes[host],
                    observer,
                    assigned,
                )
                keep = z3.Bool(f"keep_edge_{host}_{observer}_{assigned}")
                solver.add(z3.Implies(keep, edge == expected))
                free_edges.append((host, observer, assigned, expected, edge))
                keep_literals.append(keep)

    baseline = solver.check(*keep_literals)
    baseline_reason = solver.reason_unknown() if baseline == z3.unknown else None
    prior_records = []
    if resume is not None:
        prior_document = json.loads(resume.read_text())
        prior_records = prior_document.get("records", [])
    record_map = {
        (record["host"], record["observer"], record["assigned"]): record
        for record in prior_records
        if record.get("flip_verdict") != "UNKNOWN"
        and (record.get("flip_verdict") != "SAT" or record.get("values") is not None)
    }
    records = sorted(
        record_map.values(),
        key=lambda record: (record["host"], record["observer"], record["assigned"]),
    )

    def checkpoint(status):
        result = {
            "schema": SCHEMA,
            "status": status,
            "meaning": (
                "Exact satisfiability test of every Hamming-one neighboring host-edge "
                "cell, holding the other 31 bits at the source pattern under simultaneous "
                "blockage of all 120 token states."
            ),
            "claim_boundary": (
                "SAT flips identify an adjacent simultaneously blocked edge cell. UNSAT "
                "flips prove only local Hamming-one isolation from the source pattern; "
                "multiple edge bits may still change together."
            ),
            "source": str(source),
            "timeout_seconds_per_check": timeout_seconds,
            "flip_timeout_seconds_per_check": flip_timeout_seconds,
            "baseline_verdict": verdict_name(baseline),
            "baseline_reason_unknown": baseline_reason,
            "free_edge_count": len(records),
            "flexible_edge_count": sum(
                record["flip_verdict"] == "SAT" for record in records
            ),
            "forced_edge_count": sum(
                record["flip_verdict"] == "UNSAT" for record in records
            ),
            "unknown_edge_count": sum(
                record["flip_verdict"] == "UNKNOWN" for record in records
            ),
            "records": records,
        }
        atomic_json(output, result)
        return result

    checkpoint("EDGE_FLEXIBILITY_IN_PROGRESS")
    if baseline == z3.sat:
        solver.set(timeout=flip_timeout_seconds * 1000)
        for index, (host, observer, assigned, expected, edge) in enumerate(free_edges):
            key = (host, observer, assigned)
            if key in record_map:
                continue
            solver.push()
            solver.add(edge != expected)
            verdict = solver.check(
                *(keep for offset, keep in enumerate(keep_literals) if offset != index)
            )
            reason = solver.reason_unknown() if verdict == z3.unknown else None
            model_values = integer_values(solver.model(), values) if verdict == z3.sat else None
            solver.pop()
            record_map[key] = {
                "host": host,
                "observer": observer,
                "assigned": assigned,
                "source_edge": expected,
                "flip_verdict": verdict_name(verdict),
                "reason_unknown": reason,
                "values": model_values,
            }
            records[:] = sorted(
                record_map.values(),
                key=lambda record: (
                    record["host"],
                    record["observer"],
                    record["assigned"],
                ),
            )
            checkpoint("EDGE_FLEXIBILITY_IN_PROGRESS")

    final_status = (
        "EDGE_FLEXIBILITY_CLASSIFIED"
        if baseline == z3.sat
        and len(records) == len(free_edges)
        and all(record["flip_verdict"] != "UNKNOWN" for record in records)
        else "EDGE_FLEXIBILITY_PARTIAL"
    )
    return checkpoint(final_status)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--flip-timeout-seconds", type=int, default=10)
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.timeout_seconds,
        args.flip_timeout_seconds,
        args.resume,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
