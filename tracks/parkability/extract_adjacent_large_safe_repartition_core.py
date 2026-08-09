#!/usr/bin/env python3
"""Extract a binary solver core for the safe-repartition gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_adjacent_large_safe_repartition_gate import (
        add_compatible_absence,
        rq_repartitions,
        safe_rq_repartition_expression,
    )
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        atomic_json,
        make_cell,
        structural_solver,
    )
except ImportError:
    from decide_adjacent_large_safe_repartition_gate import (
        add_compatible_absence,
        rq_repartitions,
        safe_rq_repartition_expression,
    )
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        atomic_json,
        make_cell,
        structural_solver,
    )


SCHEMA = "adjacent-large-safe-repartition-core-v2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_specs(cell):
    records = []
    for index, (r_bundle, q_bundle) in enumerate(rq_repartitions(cell)):
        records.append(
            {
                "key": f"repartition_{index}",
                "kind": "safe_rq_repartition",
                "r_bundle": r_bundle,
                "q_bundle": q_bundle,
            }
        )
    return records


def exclusion_clause(record, values, own):
    return z3.Not(
        safe_rq_repartition_expression(
            values, own, record["r_bundle"], record["q_bundle"]
        )
    )


def base_solver(cell):
    solver, values, own = structural_solver(cell)
    add_compatible_absence(solver, values, own, cell)
    return solver, values, own


def check_subset(cell, keys, timeout_seconds):
    solver, values, own = base_solver(cell)
    by_key = {record["key"]: record for record in candidate_specs(cell)}
    solver.add(*(exclusion_clause(by_key[key], values, own) for key in keys))
    solver.set(timeout=timeout_seconds * 1000)
    return str(solver.check())


def named(cell, record):
    result = {"key": record["key"], "kind": record["kind"]}
    for field in ("r_bundle", "q_bundle"):
        if field in record:
            result[field] = [cell["goods"][good] for good in record[field]]
    return result


def run(timeout_seconds, minimize=True):
    cell = make_cell((2, 2, 2, 2))
    solver, values, own = base_solver(cell)
    records = candidate_specs(cell)
    by_key = {record["key"]: record for record in records}
    for record in records:
        solver.assert_and_track(
            exclusion_clause(record, values, own), z3.Bool(record["key"])
        )
    solver.set(timeout=timeout_seconds * 1000)
    checked = solver.check()
    if checked != z3.unsat:
        raise RuntimeError(("full gate did not prove UNSAT", checked, solver.reason_unknown()))
    core = [str(label) for label in solver.unsat_core()]
    initial_core_size = len(core)

    if minimize:
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            status = check_subset(cell, trial, timeout_seconds)
            if status == "unsat":
                core = trial
            elif status == "sat":
                index += 1
            else:
                raise RuntimeError(("deletion check unknown", core[index]))

    deletions = []
    if minimize:
        for removed in core:
            status = check_subset(
                cell, [key for key in core if key != removed], timeout_seconds
            )
            deletions.append({"removed": removed, "status": status})
            if status != "sat":
                raise AssertionError(("core not deletion-minimal", removed, status))
    script = Path(__file__).resolve()
    gate = script.with_name("decide_adjacent_large_safe_repartition_gate.py")
    return {
        "schema": SCHEMA,
        "status": (
            "UNSAT_DELETION_MINIMAL_CORE" if minimize else "UNSAT_SOLVER_CORE"
        ),
        "packet_sizes": [2, 2, 2, 2],
        "full_candidate_count": len(records),
        "initial_core_size": initial_core_size,
        "core_size": len(core),
        "core": [named(cell, by_key[key]) for key in core],
        "deletion_checks": deletions,
        "claim_boundary": (
            "Exact binary-cell core only; motifs are proof-discovery evidence, "
            "not a cap-free theorem."
        ),
        "solver": {"name": "z3", "version": z3.get_version_string()},
        "provenance": {
            "extractor_script": str(script.relative_to(script.parents[2])),
            "extractor_script_sha256": sha256(script),
            "gate_script": str(gate.relative_to(gate.parents[2])),
            "gate_script_sha256": sha256(gate),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--skip-minimize", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.timeout_seconds, minimize=not args.skip_minimize)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
