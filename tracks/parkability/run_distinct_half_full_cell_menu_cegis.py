#!/usr/bin/env python3
"""Search for a small cap-free favorite-pair menu under no full Hall cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-menu-cegis-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_values(raw):
    values = tuple(tuple(int(value) for value in row) for row in raw)
    if len(values) != N or any(len(row) != M for row in values):
        raise ValueError("profile has wrong dimensions")
    audit_branch(values)
    if full_hall_cells(values):
        raise ValueError("seed profile has a full Hall cell")
    return values


def load_profiles(path: Path):
    payload = json.loads(path.read_text())
    raw_profiles = []
    if payload.get("values") is not None:
        raw_profiles.append(payload["values"])
    if payload.get("real_canonical_values") is not None:
        raw_profiles.append(payload["real_canonical_values"])
    raw_profiles.extend(
        record["values"]
        for record in payload.get("trace", [])
        if record.get("values") is not None
    )
    raw_profiles.extend(
        record["values"]
        for record in payload.get("removal_boundaries", [])
        if record.get("values") is not None
    )
    if not raw_profiles:
        raise ValueError(f"seed has no profiles: {path}")
    return tuple(decode_values(raw) for raw in raw_profiles)


def minimum_menu(repair_sets, universe):
    model = cp_model.CpModel()
    selected = [model.NewBoolVar(f"partition_{position}") for position in range(len(universe))]
    for repairs in repair_sets:
        model.Add(
            sum(
                selected[position]
                for position, partition in enumerate(universe)
                if partition in repairs
            )
            >= 1
        )
    model.Minimize(
        1_000_000 * sum(selected)
        + sum((position + 1) * literal for position, literal in enumerate(selected))
    )
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 20260731
    status = solver.Solve(model)
    if status != cp_model.OPTIMAL:
        raise RuntimeError("minimum hitting-menu solve did not finish optimally")
    return tuple(
        partition
        for position, partition in enumerate(universe)
        if solver.Value(selected[position])
    )


def build_master(menu):
    master = ParkabilityLRAMaster(N, M)
    add_branch(master, None, threshold_encoding="sorting")
    for agent in range(N - 1):
        master.solver.add(
            master.values[agent][FAVORITE]
            >= master.values[agent + 1][FAVORITE]
        )
    for good in range(5, M - 1):
        master.solver.add(master.values[0][good] >= master.values[0][good + 1])
    full_cell_encoding = add_no_full_hall_cell(master)
    for partition in menu:
        master.add_partition_obstruction(partition)
    return master, full_cell_encoding


def encode_partitions(partitions):
    return [
        [list(bundle) for bundle in partition]
        for partition in partitions
    ]


def run(output, smt2, seed_paths, time_limit, max_iterations):
    universe = tuple(favorite_pair_balanced_universe())
    profiles = []
    seen = set()
    for path in seed_paths:
        for values in load_profiles(path):
            if values not in seen:
                seen.add(values)
                profiles.append(values)
    initial_profile_count = len(profiles)

    trace = []
    status = "ITERATION_LIMIT"
    final_master = None
    full_cell_encoding = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        repair_sets = tuple(
            set(supported_partitions(values, list(universe)))
            for values in profiles
        )
        if any(not repairs for repairs in repair_sets):
            raise AssertionError("seed profile refutes the full-cell dichotomy")
        menu = minimum_menu(repair_sets, universe)
        master, full_cell_encoding = build_master(menu)
        solved = master.solve(time_limit_s=time_limit)
        final_master = master
        record = {
            "iteration": iteration,
            "profile_count": len(profiles),
            "menu_size": len(menu),
            "menu": encode_partitions(menu),
            "solver_status": solved.raw_status,
            "reason_unknown": solved.reason_unknown,
            "values": None,
            "favorite_pair_repair_count": None,
        }
        if solved.status == "UNSAT":
            status = "UNSAT_MENU_CANDIDATE"
            trace.append(record)
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            trace.append(record)
            break
        values = solved.values
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("menu escape has a full Hall cell")
        if supported_partitions(values, list(menu)):
            raise AssertionError("menu escape repairs a selected partition")
        repairs = supported_partitions(values, list(universe))
        if not repairs:
            status = "FULL_CELL_SELECTION_COUNTEREXAMPLE"
            record["values"] = [list(row) for row in values]
            record["favorite_pair_repair_count"] = 0
            trace.append(record)
            break
        record["values"] = [list(row) for row in values]
        record["favorite_pair_repair_count"] = len(repairs)
        trace.append(record)
        if values in seen:
            raise AssertionError("menu CEGIS repeated a profile")
        seen.add(values)
        profiles.append(values)

    if final_master is None:
        raise AssertionError("no menu iteration ran")
    formula = final_master.to_smt2()
    smt2.parent.mkdir(parents=True, exist_ok=True)
    smt2.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "seed_sources": [
            {"path": str(path), "sha256": sha256(path)}
            for path in seed_paths
        ],
        "initial_profile_count": initial_profile_count,
        "final_profile_count": len(profiles),
        "favorite_pair_partition_count": len(universe),
        "full_hall_cell_forbidden": True,
        "full_cell_encoding": full_cell_encoding,
        "time_limit_seconds_per_iteration": time_limit,
        "max_iterations": max_iterations,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "smt2_path": str(smt2),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "An UNSAT menu would be a cap-free finite-menu strengthening of "
            "the full-cell dichotomy, subject to independent replay. SAT "
            "iterations are exact menu counterexamples but retain other "
            "favorite-pair EFX repairs."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--max-iterations", type=int, default=10)
    args = parser.parse_args()
    if args.time_limit <= 0 or args.max_iterations < 1:
        parser.error("invalid menu CEGIS parameters")
    result = run(
        args.output,
        args.smt2,
        tuple(args.seed),
        args.time_limit,
        args.max_iterations,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
