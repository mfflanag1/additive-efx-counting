#!/usr/bin/env python3
"""Bounded decision for the rank-one triple conversion dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path

import ortools

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
    from .integer_partition_master import IntegerPartitionMaster
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
    from integer_partition_master import IntegerPartitionMaster


SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"


def add_rank_one_premise(master):
    masks = tuple(sum(1 << good for good in bundle) for bundle in RESIDUAL)
    for resident in range(1, N):
        for bundle_index in range(len(RESIDUAL)):
            violations = master._edge_violations(
                resident,
                bundle_index,
                RESIDUAL,
                masks,
            )
            if bundle_index == 0:
                master.model.AddBoolAnd(
                    [violation.Not() for violation in violations]
                )
            else:
                master.model.AddBoolOr(violations)


def run(
    upper,
    conversion_scope,
    cegar_singletons,
    add_per_iteration,
    max_iterations,
    time_limit,
    workers,
    result_path,
    proto_path,
):
    if (
        upper < 1
        or conversion_scope not in {"first", "all", "radius2"}
        or add_per_iteration < 1
        or max_iterations < 1
        or time_limit <= 0
        or workers < 1
        or result_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("valid bounds and new output paths are required")
    master = IntegerPartitionMaster(N, M, upper)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    favorite = master.values[OWNER][FAVORITE]
    for bundle in RESIDUAL:
        for removed in bundle:
            master.model.Add(
                favorite
                >= sum(
                    master.values[OWNER][good]
                    for good in bundle
                    if good != removed
                )
            )
    add_rank_one_premise(master)

    singleton_partitions = tuple(
        ((FAVORITE,),) + partition for partition in residual_partitions()
    )
    singleton_pool = []
    singleton_pool_set = set()
    if not cegar_singletons:
        for partition in singleton_partitions:
            master.add_partition_obstruction(partition)
            singleton_pool.append(partition)
            singleton_pool_set.add(tuple(sorted(partition)))
    all_conversions = conversion_partitions()
    blocked_partitions = (
        balanced_transfer_neighborhood(RESIDUAL, 2)
        if conversion_scope == "radius2"
        else conversion_partitions(conversion_scope)
    )
    for partition in blocked_partitions:
        master.add_partition_obstruction(partition)

    started = time.time()
    trace = []
    solved = None
    candidate = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(
            time_limit_s=time_limit,
            workers=workers,
            random_seed=1,
        )
        if solved.status != "SAT":
            break
        values = solved.values
        assert values is not None
        if not cegar_singletons:
            candidate = values
            break
        survivors = []
        for partition in singleton_partitions:
            key = tuple(sorted(partition))
            if key in singleton_pool_set:
                continue
            if matching_rank(feasible_graph(values, partition)) == N:
                survivors.append(partition)
        trace.append({
            "iteration": iteration,
            "singleton_pool_size_before": len(singleton_pool),
            "supported_unpooled_singleton_partition_count": len(survivors),
            "solver_status": solved.raw_status,
            "solver_wall_seconds": solved.wall_time_seconds,
            "values": [list(row) for row in values],
        })
        if not survivors:
            candidate = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            singleton_pool.append(partition)
            singleton_pool_set.add(tuple(sorted(partition)))
    if solved is None:
        raise AssertionError("CP-SAT performed no solve")
    elapsed = time.time() - started
    values = candidate
    candidate_audit = None
    if values is not None:
        singleton_support = sum(
            matching_rank(feasible_graph(values, partition)) == N
            for partition in singleton_partitions
        )
        conversion_ranks = [
            matching_rank(feasible_graph(values, partition))
            for partition in all_conversions
        ]
        if (
            any(row[FAVORITE] <= max(row[1:]) for row in values)
            or not threshold_passes(values, OWNER, RESIDUAL)
            or resident_graph(values) != ((True, False, False),) * 3
            or singleton_support
            or any(
                matching_rank(feasible_graph(values, partition)) == N
                for partition in blocked_partitions
            )
        ):
            raise AssertionError("decoded CP-SAT model left the decision cell")
        support_shapes = Counter()
        support_count = 0
        for partition in core.iter_unlabeled_nonempty_partitions(N, M):
            if matching_rank(feasible_graph(values, partition)) != N:
                continue
            support_count += 1
            support_shapes[
                "".join(map(str, sorted(map(len, partition), reverse=True)))
            ] += 1
        candidate_audit = {
            "selected_owner_threshold_pass": True,
            "resident_graph": [list(row) for row in resident_graph(values)],
            "favorite_singleton_supporting_partition_count": 0,
            "all_three_conversion_ranks": conversion_ranks,
            "blocked_partition_supporting_count": 0,
            "all_supporting_partition_count": support_count,
            "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
            "complete_efx_allocation_count": independent.count_complete_efx0(values),
        }

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
            if values is not None
            else "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "ITERATION_LIMIT"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "n": N,
        "m": M,
        "domain": f"positive integers in [1,{upper}]",
        "upper": upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_partition": [list(bundle) for bundle in RESIDUAL],
        "resident_rank_one_common_bundle": list(CONTESTED),
        "conversion_scope": conversion_scope,
        "blocked_partition_count": len(blocked_partitions),
        "favorite_singleton_partition_count": len(singleton_partitions),
        "cegar_singletons": cegar_singletons,
        "singleton_obstruction_pool_size": len(singleton_pool),
        "cegar_iterations": len(trace),
        "cegar_trace": trace,
        "values": [list(row) for row in values] if values else None,
        "candidate_audit": candidate_audit,
        "solver_wall_seconds": solved.wall_time_seconds,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "conflicts": solved.conflicts,
        "branches": solved.branches,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "SAT refutes only the selected fixed/all local-conversion "
            "dichotomy; it is not an EFX counterexample. UNSAT is bounded "
            "and requires independent replay."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=20)
    parser.add_argument(
        "--conversion-scope",
        choices=("first", "all", "radius2"),
        default="first",
    )
    parser.add_argument("--time-limit", type=float, default=60)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--cegar-singletons", action="store_true")
    parser.add_argument("--add-per-iteration", type=int, default=256)
    parser.add_argument("--max-iterations", type=int, default=3)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.upper,
        args.conversion_scope,
        args.cegar_singletons,
        args.add_per_iteration,
        args.max_iterations,
        args.time_limit,
        args.workers,
        args.result,
        args.proto,
    )


if __name__ == "__main__":
    main()
