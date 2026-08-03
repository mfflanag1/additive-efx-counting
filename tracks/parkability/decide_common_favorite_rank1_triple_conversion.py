#!/usr/bin/env python3
"""Decide a rank-one triple conversion-or-singleton lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        residual_partitions,
        threshold_passes,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        residual_partitions,
        threshold_passes,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "common-favorite-rank1-triple-conversion-lra-v1"
OWNER = 0
CONTESTED = (1, 2, 3)
OTHER_TRIPLE = (4, 5, 6)
PAIR = (7, 8)
RESIDUAL = (CONTESTED, OTHER_TRIPLE, PAIR)


def edge_formula(master, observer, own):
    comparisons = []
    for target in RESIDUAL:
        if target == own:
            continue
        for removed in target:
            comparisons.append(
                master._sum(observer, own)
                >= master._sum(
                    observer,
                    tuple(good for good in target if good != removed),
                )
            )
    return z3.And(*comparisons)


def conversion_partitions(scope="all"):
    partitions = tuple(
        canonical_partition([
            (FAVORITE, good),
            tuple(item for item in CONTESTED if item != good),
            OTHER_TRIPLE,
            PAIR,
        ])
        for good in CONTESTED
    )
    if scope == "first":
        return partitions[:1]
    if scope == "all":
        return partitions
    raise ValueError("unknown conversion scope")


def resident_graph(values):
    graph = feasible_graph(values, ((FAVORITE,),) + RESIDUAL)
    return tuple(tuple(graph[agent][1:]) for agent in range(1, N))


def build_master(
    obstruction_encoding,
    *,
    add_all_singletons,
    conversion_scope="all",
):
    if obstruction_encoding not in {
            "matching_clauses",
            "inline_matching_clauses",
            "hall_selectors",
    }:
        raise ValueError("unknown obstruction encoding")
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)

    for bundle in RESIDUAL:
        for removed in bundle:
            master.solver.add(
                master.values[OWNER][FAVORITE]
                >= master._sum(
                    OWNER,
                    tuple(good for good in bundle if good != removed),
                )
            )
    for resident in range(1, N):
        master.solver.add(edge_formula(master, resident, CONTESTED))
        master.solver.add(z3.Not(edge_formula(master, resident, OTHER_TRIPLE)))
        master.solver.add(z3.Not(edge_formula(master, resident, PAIR)))

    conversions = conversion_partitions(conversion_scope)
    for partition in conversions:
        master.add_partition_obstruction(
            partition,
            encoding=obstruction_encoding,
        )
    singleton_partitions = tuple(
        ((FAVORITE,),) + partition for partition in residual_partitions()
    )
    if add_all_singletons:
        for partition in singleton_partitions:
            master.add_partition_obstruction(
                partition,
                encoding=obstruction_encoding,
            )
    return master, conversions, singleton_partitions


def run(
    result_path,
    formula_path,
    time_limit,
    obstruction_encoding,
    conversion_scope,
):
    if (
        time_limit <= 0
        or result_path.exists()
        or formula_path.exists()
    ):
        raise ValueError("positive time limit and new output paths are required")
    master, conversions, singleton_partitions = build_master(
        obstruction_encoding,
        add_all_singletons=True,
        conversion_scope=conversion_scope,
    )

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    values = solved.values
    candidate_audit = None
    if values is not None:
        if (
            any(row[FAVORITE] <= max(row[1:]) for row in values)
            or not threshold_passes(values, OWNER, RESIDUAL)
            or matching_rank(resident_graph(values)) != 1
            or any(
                matching_rank(feasible_graph(values, partition)) == N
                for partition in (*conversions, *singleton_partitions)
            )
        ):
            raise AssertionError("decoded model violates the decision cell")
        candidate_audit = {
            "resident_graph": [list(row) for row in resident_graph(values)],
            "favorite_singleton_supporting_partition_count": 0,
            "local_conversion_supporting_partition_count": 0,
        }

    result = {
        "schema": SCHEMA,
        "status": (
            "RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_partition": [list(bundle) for bundle in RESIDUAL],
        "selected_owner_threshold_pass": True,
        "obstruction_encoding": obstruction_encoding,
        "conversion_scope": conversion_scope,
        "resident_rank_one_common_bundle": list(CONTESTED),
        "local_conversion_partitions": [
            [list(bundle) for bundle in partition] for partition in conversions
        ],
        "favorite_singleton_partition_count": len(singleton_partitions),
        "values": [list(row) for row in values] if values else None,
        "candidate_audit": candidate_audit,
        "solver_wall_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "formula_bytes": len(formula.encode()),
        "claim": (
            "A threshold-safe 3+3+2 partition whose residents all accept "
            "only the same triple has either a favorite-singleton EFX "
            "partition or one of the three conversions moving a contested "
            "good next to the favorite."
        ),
        "claim_boundary": (
            "UNSAT requires independent replay before theorem promotion. "
            "SAT refutes only this local dichotomy, not EFX existence. "
            "UNKNOWN decides neither direction."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=60)
    parser.add_argument(
        "--obstruction-encoding",
        choices=(
            "matching_clauses",
            "inline_matching_clauses",
            "hall_selectors",
        ),
        default="matching_clauses",
    )
    parser.add_argument(
        "--conversion-scope",
        choices=("first", "all"),
        default="all",
    )
    args = parser.parse_args()
    run(
        args.result,
        args.formula,
        args.time_limit,
        args.obstruction_encoding,
        args.conversion_scope,
    )


if __name__ == "__main__":
    main()
