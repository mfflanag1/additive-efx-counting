#!/usr/bin/env python3
"""Enumerate the Boolean cases induced by the cyclic cross-row clauses."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        CORES,
        FLOATER,
        TOKENS,
        eligible,
        owner_cores_dominate_floater,
        owner_cores_dominate_predecessor_tokens,
        pair_hall_cross_row_core_clause_terms,
    )
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import (
        BASE,
        CORES,
        FLOATER,
        TOKENS,
        eligible,
        owner_cores_dominate_floater,
        owner_cores_dominate_predecessor_tokens,
        pair_hall_cross_row_core_clause_terms,
    )


SCHEMA = "pair-hall-cross-row-clause-case-analysis-v1"
CLAUSES = tuple(
    (family, shift)
    for shift in range(4)
    for family in ("a", "b")
)


def rational_text(value):
    if z3.is_rational_value(value):
        return str(Fraction(value.numerator_as_long(), value.denominator_as_long()))
    return str(value)


def run(output: Path):
    if output.exists():
        raise ValueError("new output path required")
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.SolverFor("QF_LRA")
    for row in values:
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(eligible(values, BASE, FLOATER))
    for owner, (core, token) in enumerate(zip(CORES, TOKENS[:4])):
        solver.add(values[owner][token] < values[owner][core])
    solver.add(owner_cores_dominate_floater(values))
    solver.add(owner_cores_dominate_predecessor_tokens(values))

    cases = []
    for mask in range(1 << len(CLAUSES)):
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
            selections.append(
                {
                    "family": family,
                    "shift": shift,
                    "side": side,
                    "term": str(term),
                }
            )
        verdict = solver.check()
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
        cases.append(
            {
                "mask": mask,
                "verdict": str(verdict),
                "selections": selections,
                "values": model_values,
            }
        )
        solver.pop()

    histogram = {
        verdict: sum(case["verdict"] == verdict for case in cases)
        for verdict in sorted({case["verdict"] for case in cases})
    }
    artifact = {
        "schema": SCHEMA,
        "status": (
            "ALL_LOCAL_SELECTION_CASES_SAT"
            if histogram == {"sat": 1 << len(CLAUSES)}
            else "SOME_LOCAL_SELECTION_CASES_ELIMINATED"
        ),
        "meaning": (
            "One selected side from each of the eight cyclic cross-row clauses "
            "forms an overlapping exact cover. This scan uses only positivity, "
            "row normalization, base eligibility, unique owner minima, and the "
            "two proved owner walls; it does not use the 159/78/30 consequence "
            "pool. SAT cases therefore show only that these transparent local "
            "inequalities do not contradict that selection."
        ),
        "clause_order": [
            {"position": position, "family": family, "shift": shift}
            for position, (family, shift) in enumerate(CLAUSES)
        ],
        "case_count": len(cases),
        "verdict_histogram": histogram,
        "cases": cases,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.output)
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in ("status", "case_count", "verdict_histogram")
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
