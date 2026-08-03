#!/usr/bin/env python3
"""Census seed-derived adaptive-priority cells in the annealing traces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .run_lexmax_partial_cegar import add_candidate
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from run_lexmax_partial_cegar import add_candidate


SCHEMA = "adaptive-priority-trace-cell-census-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value_key(raw_values: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return core.validate_values(raw_values, expected_n=4, expected_m=9, lower=1)


def candidate_key(cells: list) -> tuple:
    return tuple(dict.fromkeys(candidate for _, candidate in cells))


def candidate_records(candidates: tuple) -> list[dict]:
    return [
        {
            "floater": floater,
            "base_owner": list(base_owner),
        }
        for floater, base_owner in candidates
    ]


def run(
    *,
    trace_paths: list[Path],
    seed_result_pairs: list[tuple[Path, Path]],
    output_path: Path,
    time_limit_s: float,
) -> dict:
    if (
        output_path.exists()
        or not trace_paths
        or not seed_result_pairs
        or time_limit_s <= 0
    ):
        raise ValueError("new output, traces, seed/results, and time are required")

    expected_endpoints = {}
    for seed_path, result_path in seed_result_pairs:
        seed = json.loads(seed_path.read_text())
        values = value_key(seed["values"])
        cells = derive_unique_seed_cells(values)
        result = json.loads(result_path.read_text())
        if (
            result.get("schema") != "adaptive-priority-lra-cegar-v1"
            or result.get("status") != "UNSAT_FIXED_CANDIDATE_CELL"
            or result.get("values") is not None
            or result.get("candidates") != candidate_records(candidate_key(cells))
        ):
            raise ValueError(f"invalid closed-cell endpoint {result_path}")
        expected_endpoints[candidate_key(cells)] = {
            "seed_path": str(seed_path.resolve()),
            "seed_sha256": sha256(seed_path),
            "result_path": str(result_path.resolve()),
            "result_sha256": sha256(result_path),
            "result_pool_size": result["pool_size"],
            "result_iterations": result["iterations"],
        }

    cells_by_key = {}
    trace_record_count = 0
    for trace_path in trace_paths:
        for line in trace_path.read_text().splitlines():
            record = json.loads(line)
            values = value_key(record["values"])
            cells = derive_unique_seed_cells(values)
            key = candidate_key(cells)
            trace_record_count += 1
            if key not in cells_by_key:
                cells_by_key[key] = {
                    "first_trace_path": str(trace_path.resolve()),
                    "first_trace_iteration": record["iteration"],
                    "occurrences": 0,
                }
            cells_by_key[key]["occurrences"] += 1

    records = []
    feasible_keys = set()
    for candidates, provenance in cells_by_key.items():
        master = ParkabilityLRAMaster(4, 9)
        for candidate in candidates:
            add_candidate(master, *candidate)
        premise = master.solve(time_limit_s=time_limit_s)
        if premise.status not in {"SAT", "UNSAT"}:
            raise RuntimeError("candidate-premise census returned UNKNOWN")
        feasible = premise.status == "SAT"
        if feasible:
            feasible_keys.add(candidates)
        records.append(
            {
                **provenance,
                "candidate_count": len(candidates),
                "candidates": candidate_records(candidates),
                "blocked_candidate_premise_status": premise.status,
                "closed_endpoint": expected_endpoints.get(candidates),
            }
        )

    if feasible_keys != set(expected_endpoints):
        raise AssertionError(
            "feasible trace cells and supplied exact endpoints do not match"
        )
    records.sort(
        key=lambda record: (
            record["first_trace_path"],
            record["first_trace_iteration"],
        )
    )
    result = {
        "schema": SCHEMA,
        "status": "ALL_FEASIBLE_TRACE_CELLS_CLOSED",
        "meaning": (
            "all jointly blocked candidate cells encountered in these finite "
            "annealing traces are exact fixed-cell UNSAT endpoints; this is "
            "not an exhaustive proof of adaptive-priority completion"
        ),
        "n": 4,
        "m": 9,
        "trace_record_count": trace_record_count,
        "unique_candidate_cell_count": len(records),
        "jointly_blocked_feasible_cell_count": len(feasible_keys),
        "jointly_blocked_infeasible_cell_count": (
            len(records) - len(feasible_keys)
        ),
        "closed_feasible_cell_count": len(expected_endpoints),
        "trace_inputs": [
            {
                "path": str(path.resolve()),
                "sha256": sha256(path),
            }
            for path in trace_paths
        ],
        "cells": records,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument(
        "--seed-result",
        nargs=2,
        type=Path,
        action="append",
        metavar=("SEED", "RESULT"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=30)
    args = parser.parse_args()
    result = run(
        trace_paths=args.trace,
        seed_result_pairs=[
            (pair[0], pair[1])
            for pair in args.seed_result
        ],
        output_path=args.output,
        time_limit_s=args.time_limit,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
