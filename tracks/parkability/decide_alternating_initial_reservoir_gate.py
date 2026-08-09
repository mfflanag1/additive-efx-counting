#!/usr/bin/env python3
"""Decide whether the initial alternating q-reservoir can miss its threshold."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-initial-reservoir-threshold-gate-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decide(sizes: tuple[int, int, int, int], timeout_seconds: float) -> dict:
    cell = make_cell(sizes)
    _tr, _br, tq, bq = cell["packets"]
    x_r = cell["base_bundles"][1]
    desired = tq + (cell["floater"],)
    reservoir = x_r + bq
    solver, values, _own = structural_solver(cell)
    q = 3
    deletion_values = tuple(
        subset_sum(
            values,
            q,
            tuple(good for good in desired if good != removed),
        )
        for removed in desired
    )
    reservoir_value = subset_sum(values, q, reservoir)
    solver.add(z3.Or(*(reservoir_value < entry for entry in deletion_values)))
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "desired_bundle": [cell["goods"][good] for good in desired],
        "reservoir": [cell["goods"][good] for good in reservoir],
        "solver_status": str(status),
        "claim_boundary": {
            "sat": "the initial reservoir may miss the q deletion threshold in this exact cell",
            "unsat": "the initial reservoir reaches the q deletion threshold only in this exact cell",
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.sat:
        integers = integerize(solver.model(), values)
        q_row = integers[q]
        q_reservoir = sum(q_row[good] for good in reservoir)
        q_threshold = max(
            sum(q_row[good] for good in desired if good != removed)
            for removed in desired
        )
        if not q_reservoir < q_threshold:
            raise AssertionError("SAT model does not miss the reservoir threshold")
        result.update(
            {
                "status": "INITIAL_RESERVOIR_THRESHOLD_REFUTED",
                "q_reservoir_value": q_reservoir,
                "q_desired_threshold": q_threshold,
                "values": [list(row) for row in integers],
            }
        )
    elif status == z3.unsat:
        result["status"] = "UNSAT_INITIAL_RESERVOIR_THRESHOLD"
    else:
        result["status"] = "UNKNOWN"
        result["reason_unknown"] = solver.reason_unknown()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = decide(sizes, args.timeout_seconds)
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
        "z3_version": z3.get_version_string(),
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
