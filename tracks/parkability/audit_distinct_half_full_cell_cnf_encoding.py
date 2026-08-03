#!/usr/bin/env python3
"""Audit both polarities of the cap-5 threshold-CNF encoding."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_full_cell_cegar import full_hall_cells
    from .run_generic_partition_cegar import supported_partitions
    from .terminal_cnf import solve_formula
    from .terminal_distinct_half_full_cell_cnf import build
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_full_cell_cegar import full_hall_cells
    from run_generic_partition_cegar import supported_partitions
    from terminal_cnf import solve_formula
    from terminal_distinct_half_full_cell_cnf import build


SCHEMA = "distinct-half-full-cell-cnf-encoding-audit-v1"
FULL_CELL_VALUES = (
    (4, 3, 3, 3, 3, 3, 3, 1, 1),
    (4, 3, 3, 3, 3, 3, 3, 1, 1),
    (4, 3, 3, 3, 3, 3, 3, 1, 1),
    (4, 3, 3, 3, 3, 3, 3, 1, 1),
)


def solve(values, partitions):
    encoder, decoded_partitions, full_cell_encoding = build(
        {"core_partitions": partitions}, 5, fixed_values=values
    )
    result = solve_formula(encoder.cnf.clauses, "cadical195")
    return result["status"], {
        "variables": encoder.cnf.nv,
        "clauses": len(encoder.cnf.clauses),
        "partition_count": len(decoded_partitions),
        "full_cell_encoding": full_cell_encoding,
    }


def audit(source_path: Path):
    source = json.loads(source_path.read_text())
    no_full_values = tuple(tuple(row) for row in source["trace"][0]["values"])
    audit_branch(no_full_values)
    audit_branch(FULL_CELL_VALUES)
    no_full_cells = full_hall_cells(no_full_values)
    positive_cells = full_hall_cells(FULL_CELL_VALUES)
    if no_full_cells or positive_cells != [[7, 8]]:
        raise AssertionError("CNF control profiles changed")

    universe = tuple(favorite_pair_balanced_universe())
    repairs = set(supported_partitions(no_full_values, list(universe)))
    supporting = next(partition for partition in universe if partition in repairs)
    obstructed = next(partition for partition in universe if partition not in repairs)

    no_full_status, no_full_counts = solve(no_full_values, [])
    full_status, full_counts = solve(FULL_CELL_VALUES, [])
    supporting_status, supporting_counts = solve(
        no_full_values, [[list(bundle) for bundle in supporting]]
    )
    obstructed_status, obstructed_counts = solve(
        no_full_values, [[list(bundle) for bundle in obstructed]]
    )
    if (
        no_full_status is not True
        or full_status is not False
        or supporting_status is not False
        or obstructed_status is not True
        or len(repairs) != 361
        or no_full_counts["clauses"] != 566828
        or full_counts != no_full_counts
        or supporting_counts["clauses"] != 574836
        or obstructed_counts != supporting_counts
    ):
        raise AssertionError("threshold-CNF polarity changed")

    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FULL_CELL_CNF_ENCODING_AUDIT_PASSED",
        "no_full_cell_polarity": {
            "negative_control_cells": no_full_cells,
            "negative_control_cnf_sat": no_full_status,
            "positive_control_cells": positive_cells,
            "positive_control_cnf_sat": full_status,
            "counts": no_full_counts,
        },
        "partition_obstruction_polarity": {
            "supporting_partition": [list(bundle) for bundle in supporting],
            "supporting_partition_cnf_sat": supporting_status,
            "obstructed_partition": [list(bundle) for bundle in obstructed],
            "obstructed_partition_cnf_sat": obstructed_status,
            "trace_profile_repairs": len(repairs),
            "counts": supporting_counts,
        },
        "interpretation": (
            "With item values fixed, the independent threshold CNF is SAT "
            "exactly on the no-full-cell control and on a genuinely "
            "obstructed favorite-pair partition; reversing either semantic "
            "polarity makes it UNSAT."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
