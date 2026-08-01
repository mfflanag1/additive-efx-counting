#!/usr/bin/env python3
"""Maximize obstructed terminal-exchange targets in a bounded domain."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from .decide_distinct_half_terminal_exchange import (
        M,
        N,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        matching_slacks,
        parse_low_pair,
        target_partitions,
    )
    from .decide_distinct_half_terminal_exchange_cpsat import matching_is_efx
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
    from .run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from decide_distinct_half_terminal_exchange import (
        M,
        N,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        matching_slacks,
        parse_low_pair,
        target_partitions,
    )
    from decide_distinct_half_terminal_exchange_cpsat import matching_is_efx
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-terminal-exchange-cpsat-optimization-v1"


def load_values(path):
    payload = json.loads(path.read_text())
    values = payload.get("values")
    if values is None:
        raise ValueError(f"hint has no values: {path}")
    if len(values) != N or any(len(row) != M for row in values):
        raise ValueError(f"hint has the wrong dimensions: {path}")
    return tuple(tuple(int(value) for value in row) for row in values)


def add_matching_efx(model, values, partition, matching):
    for observer, own_bundle in enumerate(matching):
        own = sum(values[observer][good] for good in partition[own_bundle])
        for target_bundle, target in enumerate(partition):
            if target_bundle == own_bundle:
                continue
            for removed in target:
                model.Add(
                    own
                    >= sum(
                        values[observer][good]
                        for good in target
                        if good != removed
                    )
                )


def run(
    case,
    matching_orbit,
    cap,
    time_limit,
    workers,
    random_seed,
    result_path,
    proto_path,
    hint_path=None,
    require_no_full_cell=False,
    forbidden_full_cell_pairs=None,
):
    terminal = TERMINAL_PARTITIONS[case]
    matching = TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit]
    targets = target_partitions("radius2", terminal)
    universe = favorite_pair_universe("all")
    positions = {partition: position for position, partition in enumerate(universe)}

    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    if require_no_full_cell and forbidden_full_cell_pairs is not None:
        raise ValueError("cannot forbid all and selected full Hall cells together")
    full_cell_encoding = (
        add_no_full_hall_cells(model, values, cap)
        if require_no_full_cell
        else add_no_full_hall_cells(
            model, values, cap, low_pairs=forbidden_full_cell_pairs
        )
        if forbidden_full_cell_pairs is not None
        else None
    )
    add_matching_efx(model, values, terminal, matching)

    obstruction_guards = []
    for candidate in targets:
        guard = model.NewBoolVar(f"obstruct_{positions[candidate]}")
        add_favorite_pair_obstruction(
            model,
            values,
            candidate,
            positions[candidate],
            guard=guard,
        )
        obstruction_guards.append(guard)
    model.Maximize(sum(obstruction_guards))

    hint_values = load_values(hint_path) if hint_path is not None else None
    if hint_values is not None and max(map(max, hint_values)) <= cap:
        for agent in range(N):
            for good in range(M):
                model.AddHint(values[agent][good], hint_values[agent][good])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started

    decoded = None
    repairs = ()
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        decoded = tuple(
            tuple(solver.Value(values[agent][good]) for good in range(M))
            for agent in range(N)
        )
        audit_branch(decoded)
        if not matching_is_efx(decoded, terminal, matching):
            raise AssertionError("decoded terminal matching is not EFX")
        if require_no_full_cell and full_hall_cells(decoded):
            raise AssertionError("decoded profile has a forbidden full Hall cell")
        if forbidden_full_cell_pairs is not None and set(
            map(tuple, full_hall_cells(decoded))
        ).intersection(forbidden_full_cell_pairs):
            raise AssertionError("decoded profile has a selected forbidden Hall cell")
        repairs = tuple(
            candidate
            for candidate in targets
            if matching_rank(feasible_graph(decoded, candidate)) == N
        )
    all_repairs = (
        tuple(supported_partitions(decoded, list(universe)))
        if decoded is not None
        else ()
    )
    histogram = Counter(
        favorite_pair_orbit_signature(candidate) for candidate in all_repairs
    )

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    encoded_targets = json.dumps(
        [[list(bundle) for bundle in item] for item in targets],
        separators=(",", ":"),
    ).encode()
    objective = solver.ObjectiveValue() if decoded is not None else None
    bound = solver.BestObjectiveBound() if decoded is not None else None
    result = {
        "schema": SCHEMA,
        "status": (
            "TERMINAL_SELECTOR_COUNTEREXAMPLE"
            if decoded is not None and not repairs
            else "OPTIMIZATION_CHECKPOINT"
            if decoded is not None
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": solver.StatusName(status_code),
        "case": case,
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": list(matching),
        "cap": cap,
        "n": N,
        "m": M,
        "terminal_partition": [list(bundle) for bundle in terminal],
        "target": "radius2",
        "target_partition_count": len(targets),
        "target_partitions_sha256": hashlib.sha256(encoded_targets).hexdigest(),
        "obstruction_objective": objective,
        "obstruction_objective_bound": bound,
        "target_repair_count": len(repairs) if decoded is not None else None,
        "target_repairs": (
            [[list(bundle) for bundle in item] for item in repairs]
            if decoded is not None
            else None
        ),
        "full_hall_cell_forbidden": require_no_full_cell,
        "full_hall_cell_forbidden_pairs": (
            [list(pair) for pair in forbidden_full_cell_pairs]
            if forbidden_full_cell_pairs is not None
            else None
        ),
        "full_cell_encoding": full_cell_encoding,
        "full_hall_cells": full_hall_cells(decoded) if decoded is not None else None,
        "minimum_terminal_matching_slack": (
            min(matching_slacks(decoded, terminal, matching))
            if decoded is not None
            else None
        ),
        "values": [list(row) for row in decoded] if decoded is not None else None,
        "favorite_pair_efx_partition_count": (
            len(all_repairs) if decoded is not None else None
        ),
        "favorite_pair_efx_orbit_histogram": (
            {
                repr(signature): count
                for signature, count in sorted(
                    histogram.items(), key=lambda item: repr(item[0])
                )
            }
            if decoded is not None
            else None
        ),
        "literal_complete_efx_count": (
            independent.count_complete_efx0(decoded)
            if decoded is not None
            else None
        ),
        "hint_path": str(hint_path) if hint_path is not None else None,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "proto_path": str(proto_path),
        "proto_sha256": hashlib.sha256(proto_path.read_bytes()).hexdigest(),
        "warning": (
            "Only a zero target-repair count refutes the selected terminal "
            "exchange lemma. A positive optimization checkpoint is descriptive."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument("--matching-orbit", type=int, required=True)
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--require-no-full-cell", action="store_true")
    parser.add_argument(
        "--only-forbid-full-cell", type=parse_low_pair, action="append"
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.workers < 1
        or not 0
        <= args.matching_orbit
        < len(TERMINAL_MATCHING_REPRESENTATIVES[args.case])
        or (args.require_no_full_cell and args.only_forbid_full_cell)
    ):
        parser.error("invalid optimization parameters")
    result = run(
        args.case,
        args.matching_orbit,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.result,
        args.proto,
        args.hint,
        args.require_no_full_cell,
        tuple(args.only_forbid_full_cell) if args.only_forbid_full_cell else None,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
