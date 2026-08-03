#!/usr/bin/env python3
"""Bounded CP-SAT decision for the conditional two-core/Tutte target."""

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
    from .anneal_distinct_half_rank_augmentation import Landscape
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import Landscape
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-two-core-cpsat-v1"
N = 4
M = 9
FAVORITE = 0


def low_core_candidates(scope):
    if scope == "all":
        return tuple(
            (lows, core_agents)
            for lows in itertools.combinations(range(1, M), 2)
            for core_agents in itertools.combinations(range(N), 2)
        )
    if scope == "canonical":
        return tuple(
            (
                lows,
                tuple(
                    agent for agent in range(N) if agent + 1 not in lows
                ),
            )
            for lows in itertools.combinations(range(1, N + 1), 2)
        )
    raise ValueError("two-core scope must be all or canonical")


def perfect_pairings(goods):
    if not goods:
        yield ()
        return
    first = goods[0]
    for position in range(1, len(goods)):
        second = goods[position]
        remaining = goods[1:position] + goods[position + 1 :]
        for suffix in perfect_pairings(remaining):
            yield ((first, second),) + suffix


def add_two_core_obstructions(model, values, cap, scope="all"):
    candidate_count = 0
    candidates = low_core_candidates(scope)
    for parked in dict.fromkeys(lows for lows, _ in candidates):
        remaining = tuple(good for good in range(1, M) if good not in parked)
        edges = tuple(itertools.combinations(remaining, 2))
        accept = {}
        for observer in range(N):
            parked_max = model.NewIntVar(
                1,
                cap,
                f"parkmax_{parked[0]}_{parked[1]}_{observer}",
            )
            model.AddMaxEquality(
                parked_max,
                [values[observer][good] for good in parked],
            )
            threshold = values[observer][FAVORITE] + parked_max
            for edge in edges:
                literal = model.NewBoolVar(
                    f"accept_{parked[0]}_{parked[1]}_{observer}_"
                    f"{edge[0]}_{edge[1]}"
                )
                equivalent_ge(
                    model,
                    literal,
                    values[observer][edge[0]] + values[observer][edge[1]],
                    threshold,
                )
                accept[observer, edge] = literal

        for candidate_lows, core_agents in candidates:
            if candidate_lows != parked:
                continue
            candidate_count += 1
            outsiders = tuple(
                observer for observer in range(N) if observer not in core_agents
            )
            candidate_failures = [
                accept[observer, edge].Not()
                for observer in core_agents
                for edge in edges
            ]
            for matching_position, matching in enumerate(
                perfect_pairings(remaining)
            ):
                bad_matching = model.NewBoolVar(
                    f"badpm_{parked[0]}_{parked[1]}_"
                    f"{core_agents[0]}_{core_agents[1]}_{matching_position}"
                )
                outsider_acceptances = [
                    accept[observer, tuple(sorted(edge))]
                    for edge in matching
                    for observer in outsiders
                ]
                model.AddBoolAnd(
                    literal.Not() for literal in outsider_acceptances
                ).OnlyEnforceIf(bad_matching)
                model.AddBoolOr(outsider_acceptances).OnlyEnforceIf(
                    bad_matching.Not()
                )
                candidate_failures.append(bad_matching)
            model.AddBoolOr(candidate_failures)
    if candidate_count != len(candidates):
        raise AssertionError("two-core candidate count changed")
    return candidate_count


def run(output, proto_output, cap, time_limit, workers, random_seed):
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{observer}_{good}")
            for good in range(M)
        )
        for observer in range(N)
    )
    add_branch(model, values)
    pair_universe = tuple(favorite_pair_balanced_universe())
    for position, partition in enumerate(pair_universe):
        add_favorite_pair_obstruction(model, values, partition, position)
    two_core_candidate_count = add_two_core_obstructions(model, values, cap)

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    solver.parameters.log_search_progress = True
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started

    result_values = None
    audit = None
    literal_count = None
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        result_values = tuple(
            tuple(solver.Value(values[observer][good]) for good in range(M))
            for observer in range(N)
        )
        audit_branch(result_values)
        audit = Landscape("balanced").audit(result_values)
        if (
            audit["favorite_pair_perfect_partition_count"] != 0
            or audit["two_core_tutte_low_pair_count"] != 0
        ):
            raise AssertionError("decoded model violates the encoded target")
        literal_count = independent.count_complete_efx0(result_values)

    result = {
        "schema": SCHEMA,
        "status": (
            "TWO_CORE_SELECTION_COUNTEREXAMPLE"
            if result_values is not None
            else "FINITE_CAP_UNSAT_CANDIDATE"
            if status_code == cp_model.INFEASIBLE
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "favorite_pair_partition_count": len(pair_universe),
        "two_core_candidate_count": two_core_candidate_count,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "values": [list(row) for row in result_values] if result_values else None,
        "landscape_audit": audit,
        "literal_complete_efx_count": literal_count,
        "proto_path": str(proto_output),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time_seconds": solver.WallTime(),
        "warning": (
            "A SAT model refutes only the conditional two-core selection "
            "target unless literal EFX enumeration is also zero. An "
            "INFEASIBLE verdict is finite-cap only and requires independent "
            "replay before theorem status."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    args = parser.parse_args()
    if args.cap < 2 or args.time_limit <= 0 or args.workers < 1:
        parser.error("invalid bounded decision parameters")
    result = run(
        args.output,
        args.proto,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
