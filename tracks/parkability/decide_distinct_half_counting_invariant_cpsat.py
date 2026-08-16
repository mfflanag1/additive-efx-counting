#!/usr/bin/env python3
"""Bounded decision test for the 15-state pair/Hall counting invariant."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import favorite_triple_cell_counts
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from .optimize_distinct_half_eight_orbit_cpsat import canonicalize_hint
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import favorite_pair_universe
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import favorite_triple_cell_counts
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from optimize_distinct_half_eight_orbit_cpsat import canonicalize_hint
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import favorite_pair_universe
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-counting-invariant-cpsat-v1"
N = 4
M = 9
FAVORITE = 0
LOWER_BOUND = 15


def add_cell_validity_bound(model, values, cap, maximum_valid):
    accept_literal_count = 0
    witness_literal_count = 0
    failure_guard_count = 0
    minimum_failures = 15 - maximum_valid
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        accept = {}
        for agent in range(N):
            low_max = model.NewIntVar(
                1, cap, f"counting_lowmax_{lows[0]}_{lows[1]}_{agent}"
            )
            model.AddMaxEquality(
                low_max, [values[agent][low] for low in lows]
            )
            threshold = values[agent][FAVORITE] + low_max
            for edge in itertools.combinations(residual, 2):
                literal = model.NewBoolVar(
                    f"counting_accept_{lows[0]}_{lows[1]}_{agent}_"
                    f"{edge[0]}_{edge[1]}"
                )
                equivalent_ge(
                    model,
                    literal,
                    values[agent][edge[0]] + values[agent][edge[1]],
                    threshold,
                )
                accept[agent, edge] = literal
                accept_literal_count += 1

        failures = []
        for matching_position, matching in enumerate(perfect_pairings(residual)):
            conditions = []
            conditions.extend(
                tuple(accept[agent, edge].Not() for agent in range(N))
                for edge in matching
            )
            conditions.extend(
                tuple(
                    accept[agent, edge].Not()
                    for edge in edge_pair
                    for agent in range(N)
                    if agent != possible_neighbor
                )
                for edge_pair in itertools.combinations(matching, 2)
                for possible_neighbor in range(N)
            )
            conditions.extend(
                tuple(
                    accept[agent, edge].Not()
                    for edge in matching
                    for agent in range(N)
                    if agent not in possible_neighbors
                )
                for possible_neighbors in itertools.combinations(range(N), 2)
            )
            witnesses = []
            for witness_position, conjunction in enumerate(conditions):
                witness = model.NewBoolVar(
                    f"counting_hall_witness_{lows[0]}_{lows[1]}_"
                    f"{matching_position}_{witness_position}"
                )
                model.AddBoolAnd(conjunction).OnlyEnforceIf(witness)
                model.AddBoolOr(
                    literal.Not() for literal in conjunction
                ).OnlyEnforceIf(witness.Not())
                witnesses.append(witness)
                witness_literal_count += 1
            failed = model.NewBoolVar(
                f"counting_pairing_failed_{lows[0]}_{lows[1]}_"
                f"{matching_position}"
            )
            model.AddBoolOr(witnesses).OnlyEnforceIf(failed)
            model.AddBoolAnd(
                witness.Not() for witness in witnesses
            ).OnlyEnforceIf(failed.Not())
            failures.append(failed)
            failure_guard_count += 1
        model.Add(sum(failures) >= minimum_failures)
    return {
        "low_pair_cells": 28,
        "maximum_valid_pairings_per_cell": maximum_valid,
        "minimum_failed_pairings_per_cell": minimum_failures,
        "accept_literals": accept_literal_count,
        "hall_witness_literals": witness_literal_count,
        "pairing_failure_literals": failure_guard_count,
    }


def run(
    result_path,
    proto_path,
    cap,
    maximum_favorite_pair_repairs,
    time_limit,
    workers,
    random_seed,
    hint_path=None,
):
    if not 0 <= maximum_favorite_pair_repairs < LOWER_BOUND:
        raise ValueError("favorite-pair repair bound must lie in 0..14")
    maximum_cell_count = LOWER_BOUND - 1 - maximum_favorite_pair_repairs
    universe = favorite_pair_universe("all")
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    for agent in range(N - 1):
        model.Add(values[agent][FAVORITE] >= values[agent + 1][FAVORITE])
    for good in range(5, M - 1):
        model.Add(values[0][good] >= values[0][good + 1])

    obstruction_guards = []
    for position, partition in enumerate(universe):
        guard = model.NewBoolVar(f"counting_obstruct_{position}")
        add_favorite_pair_obstruction(
            model, values, partition, position, guard=guard
        )
        obstruction_guards.append(guard)
    model.Add(
        sum(obstruction_guards)
        >= len(universe) - maximum_favorite_pair_repairs
    )
    cell_encoding = add_cell_validity_bound(
        model, values, cap, maximum_cell_count
    )

    hint_values = (
        canonicalize_hint(load_values(hint_path))
        if hint_path is not None
        else None
    )
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
    replay = None
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        decoded = tuple(
            tuple(solver.Value(values[agent][good]) for good in range(M))
            for agent in range(N)
        )
        audit_branch(decoded)
        favorite_pair_count = len(
            supported_partitions(decoded, list(universe))
        )
        cell_counts = favorite_triple_cell_counts(decoded)
        maximum_replayed_cell = max(cell_counts.values(), default=0)
        score = favorite_pair_count + maximum_replayed_cell
        if (
            favorite_pair_count > maximum_favorite_pair_repairs
            or maximum_replayed_cell > maximum_cell_count
            or score >= LOWER_BOUND
        ):
            raise AssertionError("decoded model violates the counting bound")
        replay = {
            "favorite_pair_efx_partition_count": favorite_pair_count,
            "maximum_favorite_triple_cell_count": maximum_replayed_cell,
            "counting_score": score,
            "literal_complete_efx_count": independent.count_complete_efx0(
                decoded
            ),
        }

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    result = {
        "schema": SCHEMA,
        "status": (
            "COUNTING_INVARIANT_COUNTEREXAMPLE"
            if decoded is not None
            else "FINITE_CAP_UNSAT_CANDIDATE"
            if status_code == cp_model.INFEASIBLE
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "n": N,
        "m": M,
        "candidate_lower_bound": LOWER_BOUND,
        "maximum_favorite_pair_repairs": maximum_favorite_pair_repairs,
        "maximum_favorite_triple_cell_count": maximum_cell_count,
        "favorite_pair_partition_count": len(universe),
        "cell_encoding": cell_encoding,
        "values": [list(row) for row in decoded] if decoded else None,
        "semantic_replay": replay,
        "hint_path": str(hint_path) if hint_path else None,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "proto_path": str(proto_path),
        "proto_sha256": hashlib.sha256(proto_path.read_bytes()).hexdigest(),
        "warning": (
            "INFEASIBLE is a finite-cap result only; any SAT model refutes "
            "the proposed counting invariant cap-free."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=100)
    parser.add_argument("--maximum-favorite-pair-repairs", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260821)
    parser.add_argument("--hint", type=Path)
    args = parser.parse_args()
    if args.cap < 2 or args.time_limit <= 0 or args.workers < 1:
        parser.error("invalid bounded-decision parameters")
    result = run(
        args.result,
        args.proto,
        args.cap,
        args.maximum_favorite_pair_repairs,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.hint,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
