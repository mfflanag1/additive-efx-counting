#!/usr/bin/env python3
"""Extract a CP-SAT assumption core for a bounded full-cell formula."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from .anneal import atomic_json
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from .decide_distinct_half_full_cell_lia import reconstruct_pool
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from decide_distinct_half_full_cell_lia import reconstruct_pool
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells


SCHEMA = "distinct-half-full-cell-cpsat-assumption-core-v1"
N = 4
M = 9
FAVORITE = 0


def run(output, proto_output, source_path, cap, time_limit, workers):
    universe = tuple(favorite_pair_balanced_universe())
    source, pool, trace_counts = reconstruct_pool(source_path, universe)
    if source["cap"] != cap:
        raise ValueError("source cap changed")
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    full_cell_encoding = add_no_full_hall_cells(model, values, cap)
    for agent in range(N - 1):
        model.Add(values[agent][FAVORITE] >= values[agent + 1][FAVORITE])
    for good in range(5, M - 1):
        model.Add(values[0][good] >= values[0][good + 1])

    guards = {}
    for position, partition in enumerate(universe):
        if partition not in pool:
            continue
        guard = model.NewBoolVar(f"pool_partition_{position}")
        add_favorite_pair_obstruction(
            model, values, partition, position, guard=guard
        )
        model.AddAssumption(guard)
        guards[guard.Index()] = partition

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started
    core = []
    if status_code == cp_model.INFEASIBLE:
        for literal in solver.SufficientAssumptionsForInfeasibility():
            if literal not in guards:
                raise AssertionError("unexpected assumption literal")
            core.append(guards[literal])

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "ASSUMPTION_CORE_EXTRACTED"
            if core
            else "CP_SAT_UNKNOWN"
            if status_code == cp_model.UNKNOWN
            else solver.StatusName(status_code)
        ),
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "source_trace_survivor_counts": trace_counts,
        "symmetry_breaking": source.get("symmetry_breaking"),
        "pool_size": len(pool),
        "core_size": len(core),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in core
        ],
        "full_cell_encoding": full_cell_encoding,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "workers": workers,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "proto_path": str(proto_output),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "warning": (
            "The returned assumption core is sufficient, not necessarily "
            "minimal, and remains a CP-SAT claim until independently replayed."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    result = run(
        args.output,
        args.proto,
        args.source,
        args.cap,
        args.time_limit,
        args.workers,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
