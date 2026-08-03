#!/usr/bin/env python3
"""Decide cyclic cross-row clause selections against a full QF_LRA master."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
    from .analyze_pair_hall_cross_row_clause_cases import CLAUSES
    from .run_minimum_slot_orbit_cegar import (
        pair_hall_cross_row_core_clause_terms,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_pair_hall_cross_row_clause_cases import CLAUSES
    from run_minimum_slot_orbit_cegar import (
        pair_hall_cross_row_core_clause_terms,
    )


SCHEMA = "pair-hall-cross-row-clause-case-decision-v1"
WORKER_SOLVER = None
WORKER_VALUES = None


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational_text(value):
    if z3.is_rational_value(value):
        return str(Fraction(value.numerator_as_long(), value.denominator_as_long()))
    return str(value)


def initialize_worker(source_text: str, timeout_seconds: int):
    global WORKER_SOLVER, WORKER_VALUES
    WORKER_SOLVER = z3.SolverFor("QF_LRA")
    WORKER_SOLVER.set(timeout=timeout_seconds * 1000)
    WORKER_SOLVER.from_file(source_text)
    WORKER_VALUES = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]


def decide_mask(mask: int):
    solver = WORKER_SOLVER
    values = WORKER_VALUES
    solver.push()
    selections = []
    for position, (family, shift) in enumerate(CLAUSES):
        side = (mask >> position) & 1
        term = pair_hall_cross_row_core_clause_terms(
            values,
            family,
            shift,
        )[side]
        solver.add(term)
        selections.append(side)
    started = time.monotonic()
    verdict = solver.check()
    elapsed = time.monotonic() - started
    model_values = None
    if verdict == z3.sat:
        model = solver.model()
        model_values = [
            [
                rational_text(model.eval(entry, model_completion=True))
                for entry in row
            ]
            for row in values
        ]
    result = {
        "mask": mask,
        "selections": selections,
        "verdict": str(verdict),
        "reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "elapsed_seconds": elapsed,
        "values": model_values,
    }
    solver.pop()
    return result


def run(source: Path, output: Path, timeout_seconds: int, workers: int):
    if not source.is_file() or output.exists() or timeout_seconds <= 0 or workers <= 0:
        raise ValueError("existing source, new output, and positive bounds required")
    started = time.monotonic()
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=initialize_worker,
        initargs=(str(source), timeout_seconds),
    ) as executor:
        cases = list(executor.map(decide_mask, range(1 << len(CLAUSES))))
    histogram = {
        verdict: sum(case["verdict"] == verdict for case in cases)
        for verdict in sorted({case["verdict"] for case in cases})
    }
    status = (
        "SOURCE_SAT"
        if histogram.get("sat", 0)
        else "SOURCE_UNSAT"
        if histogram == {"unsat": 1 << len(CLAUSES)}
        else "INCOMPLETE"
    )
    artifact = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "One selected side from each proved cyclic cross-row clause forms "
            "an overlapping exact cover of the source. SAT of a case is SAT of "
            "the finite source; UNSAT of all 256 cases is UNSAT of the source."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": "qf_lra",
        "timeout_seconds_per_case": timeout_seconds,
        "workers": workers,
        "elapsed_seconds": time.monotonic() - started,
        "case_count": len(cases),
        "verdict_histogram": histogram,
        "cases": cases,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=10)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    artifact = run(args.source, args.output, args.timeout_seconds, args.workers)
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in (
                    "status",
                    "elapsed_seconds",
                    "case_count",
                    "verdict_histogram",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
