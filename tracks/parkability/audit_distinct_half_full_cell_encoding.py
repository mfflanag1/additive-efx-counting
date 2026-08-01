#!/usr/bin/env python3
"""Audit both polarities of the no-full-Hall-cell QF_LRA encoding."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3
from ortools.sat.python import cp_model

try:
    from .anneal import atomic_json
    from .audit_distinct_half_favorite_triple_boundary import (
        VALUES as NO_FULL_CELL_VALUES,
    )
    from .audit_distinct_half_two_core_boundary import VALUES as FULL_CELL_VALUES
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        M,
        N,
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from .run_distinct_half_full_cell_cpsat_cegar import (
        add_no_full_hall_cells,
    )
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_favorite_triple_boundary import (
        VALUES as NO_FULL_CELL_VALUES,
    )
    from audit_distinct_half_two_core_boundary import VALUES as FULL_CELL_VALUES
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        M,
        N,
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from run_distinct_half_full_cell_cpsat_cegar import (
        add_no_full_hall_cells,
    )


SCHEMA = "distinct-half-full-cell-encoding-audit-v1"
EXPECTED_COUNTS = {
    "low_pair_cells": 28,
    "accept_literals": 1680,
    "pairing_failure_terms": 420,
    "hall_failure_templates_per_pairing": 21,
}
EXPECTED_CPSAT_COUNTS = {
    "low_pair_cells": 28,
    "accept_literals": 1680,
    "hall_witness_literals": 8820,
    "hall_failure_templates_per_pairing": 21,
}


def encoded_status(values):
    master = ParkabilityLRAMaster(N, M, fixed_values=values)
    counts = add_no_full_hall_cell(master)
    return str(master.solver.check()), counts


def cpsat_encoded_status(values):
    cap = max(max(row) for row in values)
    model = cp_model.CpModel()
    variables = tuple(
        tuple(
            model.NewIntVar(1, cap, f"audit_value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    for agent, row in enumerate(values):
        for good, value in enumerate(row):
            model.Add(variables[agent][good] == value)
    counts = add_no_full_hall_cells(model, variables, cap)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)
    return solver.StatusName(status), counts


def audit():
    positive_cells = full_hall_cells(FULL_CELL_VALUES)
    negative_cells = full_hall_cells(NO_FULL_CELL_VALUES)
    positive_status, positive_counts = encoded_status(FULL_CELL_VALUES)
    negative_status, negative_counts = encoded_status(NO_FULL_CELL_VALUES)
    cp_positive_status, cp_positive_counts = cpsat_encoded_status(
        FULL_CELL_VALUES
    )
    cp_negative_status, cp_negative_counts = cpsat_encoded_status(
        NO_FULL_CELL_VALUES
    )
    if (
        positive_cells != [[1, 2]]
        or negative_cells
        or positive_status != str(z3.unsat)
        or negative_status != str(z3.sat)
        or positive_counts != EXPECTED_COUNTS
        or negative_counts != EXPECTED_COUNTS
        or cp_positive_status != "INFEASIBLE"
        or cp_negative_status not in {"FEASIBLE", "OPTIMAL"}
        or cp_positive_counts != EXPECTED_CPSAT_COUNTS
        or cp_negative_counts != EXPECTED_CPSAT_COUNTS
    ):
        raise AssertionError("full-cell direct/encoding equivalence changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FULL_CELL_ENCODING_AUDIT_PASSED",
        "encoding_counts": EXPECTED_COUNTS,
        "cpsat_encoding_counts": EXPECTED_CPSAT_COUNTS,
        "positive_control": {
            "full_hall_cells": positive_cells,
            "no_full_cell_formula_status": positive_status,
            "cpsat_no_full_cell_formula_status": cp_positive_status,
        },
        "negative_control": {
            "full_hall_cells": negative_cells,
            "no_full_cell_formula_status": negative_status,
            "cpsat_no_full_cell_formula_status": cp_negative_status,
        },
        "interpretation": (
            "The no-full-cell formula is UNSAT on a profile with one exact "
            "full Hall cell and SAT on a profile with none, freezing both "
            "polarities of the intermediate gate."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
