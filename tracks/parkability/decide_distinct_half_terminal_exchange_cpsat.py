#!/usr/bin/env python3
"""Bounded CP-SAT decision for a fixed terminal EFX matching."""

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
        parse_low_pair,
        target_partitions,
    )
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
        parse_low_pair,
        target_partitions,
    )
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-terminal-exchange-cpsat-v1"


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


def add_terminal_slack_branch(model, values, partition, matching, branch):
    if branch == "any":
        return
    equalities = []
    for observer, own_bundle in enumerate(matching):
        own = sum(values[observer][good] for good in partition[own_bundle])
        for target_bundle, target in enumerate(partition):
            if target_bundle == own_bundle:
                continue
            for removed in target:
                remainder = sum(
                    values[observer][good]
                    for good in target
                    if good != removed
                )
                if branch == "strict":
                    model.Add(own > remainder)
                elif branch == "boundary":
                    equality = model.NewBoolVar(
                        f"terminal_boundary_{observer}_{own_bundle}_"
                        f"{target_bundle}_{removed}"
                    )
                    model.Add(own == remainder).OnlyEnforceIf(equality)
                    equalities.append(equality)
                else:
                    raise ValueError("unknown terminal slack branch")
    if branch == "boundary":
        model.AddBoolOr(equalities)


def matching_is_efx(values, partition, matching):
    return all(
        own_bundle == target_bundle
        or sum(values[observer][good] for good in partition[own_bundle])
        >= sum(values[observer][good] for good in target if good != removed)
        for observer, own_bundle in enumerate(matching)
        for target_bundle, target in enumerate(partition)
        for removed in target
    )


def matching_slacks(values, partition, matching):
    return tuple(
        sum(values[observer][good] for good in partition[own_bundle])
        - sum(values[observer][good] for good in target if good != removed)
        for observer, own_bundle in enumerate(matching)
        for target_bundle, target in enumerate(partition)
        if target_bundle != own_bundle
        for removed in target
    )


def run(
    case,
    target,
    matching_orbit,
    cap,
    time_limit,
    workers,
    random_seed,
    result_path,
    proto_path,
    require_no_full_cell=True,
    terminal_slack_branch="any",
    target_pool_path=None,
    forbidden_full_cell_pairs=None,
):
    partition = TERMINAL_PARTITIONS[case]
    matching = TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit]
    target_universe = target_partitions(target, partition)
    if target_pool_path is None:
        targets = target_universe
    else:
        payload = json.loads(target_pool_path.read_text())
        if payload.get("case", case) != case or payload.get("target", target) != target:
            raise ValueError("target pool metadata does not match the requested case")
        if payload.get("terminal_matching_orbit", matching_orbit) != matching_orbit:
            raise ValueError("target pool metadata has a different matching orbit")
        targets = tuple(
            tuple(tuple(bundle) for bundle in item)
            for item in payload["core_partitions"]
        )
        if not targets or not set(targets).issubset(target_universe):
            raise ValueError("target pool is not a nonempty target-family subset")
    universe = favorite_pair_universe("all")
    positions = {candidate: position for position, candidate in enumerate(universe)}

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
    add_matching_efx(model, values, partition, matching)
    add_terminal_slack_branch(
        model, values, partition, matching, terminal_slack_branch
    )
    for candidate in targets:
        add_favorite_pair_obstruction(
            model, values, candidate, positions[candidate]
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started
    decoded = None
    model_full_cells = set()
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        decoded = tuple(
            tuple(solver.Value(values[agent][good]) for good in range(M))
            for agent in range(N)
        )
        audit_branch(decoded)
        model_full_cells = {tuple(cell) for cell in full_hall_cells(decoded)}
        if require_no_full_cell and model_full_cells:
            raise AssertionError("decoded model has a forbidden full Hall cell")
        if forbidden_full_cell_pairs is not None and model_full_cells.intersection(
            forbidden_full_cell_pairs
        ):
            raise AssertionError("decoded model has a selected forbidden Hall cell")
        if not matching_is_efx(decoded, partition, matching):
            raise AssertionError("decoded terminal matching is not EFX")
        terminal_slacks = matching_slacks(decoded, partition, matching)
        if (
            terminal_slack_branch == "strict"
            and min(terminal_slacks) <= 0
        ) or (
            terminal_slack_branch == "boundary"
            and 0 not in terminal_slacks
        ):
            raise AssertionError("decoded terminal slack branch changed")
        if any(
            matching_rank(feasible_graph(decoded, candidate)) == N
            for candidate in targets
        ):
            raise AssertionError("decoded model retains a forbidden target")

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    encoded_targets = json.dumps(
        [[list(bundle) for bundle in item] for item in targets],
        separators=(",", ":"),
    ).encode()
    repairs = (
        tuple(supported_partitions(decoded, list(universe)))
        if decoded is not None
        else ()
    )
    histogram = Counter(
        favorite_pair_orbit_signature(candidate) for candidate in repairs
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "TERMINAL_SELECTOR_COUNTEREXAMPLE"
            if decoded is not None
            else "FINITE_CAP_UNSAT_CANDIDATE"
            if status_code == cp_model.INFEASIBLE
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": solver.StatusName(status_code),
        "case": case,
        "target": target,
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": list(matching),
        "terminal_slack_branch": terminal_slack_branch,
        "terminal_matching_orbit_count": len(
            TERMINAL_MATCHING_REPRESENTATIVES[case]
        ),
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "terminal_partition": [list(bundle) for bundle in partition],
        "terminal_signature": list(favorite_pair_orbit_signature(partition)),
        "target_partition_count": len(targets),
        "target_pool_source": (
            str(target_pool_path) if target_pool_path is not None else None
        ),
        "target_pool_source_sha256": (
            hashlib.sha256(target_pool_path.read_bytes()).hexdigest()
            if target_pool_path is not None
            else None
        ),
        "target_partitions_sha256": hashlib.sha256(encoded_targets).hexdigest(),
        "full_hall_cell_forbidden": require_no_full_cell,
        "full_hall_cell_forbidden_pairs": (
            [list(pair) for pair in forbidden_full_cell_pairs]
            if forbidden_full_cell_pairs is not None
            else None
        ),
        "full_hall_cells": (
            [list(pair) for pair in sorted(model_full_cells)]
            if decoded is not None
            else None
        ),
        "full_cell_encoding": full_cell_encoding,
        "symmetry_breaking": [],
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "values": [list(row) for row in decoded] if decoded is not None else None,
        "favorite_pair_efx_partition_count": len(repairs) if decoded else None,
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
        "proto_path": str(proto_path),
        "proto_sha256": hashlib.sha256(proto_path.read_bytes()).hexdigest(),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "warning": (
            "SAT refutes only the selected terminal-to-target implication. "
            "INFEASIBLE is finite-cap only and requires independent replay."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument(
        "--target",
        choices=(
            "radius2",
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
            "same_favorite",
            "eight_orbit",
        ),
        required=True,
    )
    parser.add_argument("--matching-orbit", type=int, required=True)
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=180)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--allow-full-hall-cell", action="store_true")
    parser.add_argument(
        "--only-forbid-full-cell", type=parse_low_pair, action="append"
    )
    parser.add_argument("--target-pool", type=Path)
    parser.add_argument(
        "--terminal-slack-branch",
        choices=("any", "strict", "boundary"),
        default="any",
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.workers < 1
        or not 0
        <= args.matching_orbit
        < len(TERMINAL_MATCHING_REPRESENTATIVES[args.case])
        or (args.allow_full_hall_cell and args.only_forbid_full_cell)
    ):
        parser.error("invalid bounded decision parameters")
    result = run(
        args.case,
        args.target,
        args.matching_orbit,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.result,
        args.proto,
        not args.allow_full_hall_cell and args.only_forbid_full_cell is None,
        args.terminal_slack_branch,
        args.target_pool,
        tuple(args.only_forbid_full_cell) if args.only_forbid_full_cell else None,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
