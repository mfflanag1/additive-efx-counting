#!/usr/bin/env python3
"""Bounded CP-SAT witness search for the mixed threshold/Hall gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
    from .decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        OWNER,
        SHAPES,
        deficient_bundle_sets,
        residual_partitions,
        threshold_passes,
    )
    from .integer_partition_master import IntegerPartitionMaster
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        OWNER,
        SHAPES,
        deficient_bundle_sets,
        residual_partitions,
        threshold_passes,
    )
    from integer_partition_master import IntegerPartitionMaster


SCHEMA = "common-favorite-threshold-pass-hall-cpsat-v1"


def local_favorite_pair_conversions(selected):
    conversions = set()
    for donor_index, donor in enumerate(selected):
        if len(donor) != 3:
            continue
        for good in donor:
            residual = [
                tuple(item for item in donor if item != good)
                if index == donor_index
                else bundle
                for index, bundle in enumerate(selected)
            ]
            conversions.add(tuple(sorted(((FAVORITE, good), *residual))))
    return tuple(sorted(conversions))


def transfer_distance(left, right):
    overlap = max(
        sum(
            len(set(left[index]) & set(right[matching[index]]))
            for index in range(N)
        )
        for matching in itertools.permutations(range(N))
    )
    return M - overlap


def balanced_transfer_neighborhood(selected, radius):
    if radius < 1:
        return ()
    source = ((FAVORITE,),) + selected
    return tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
        and transfer_distance(source, partition) <= radius
    )


def run(
    shape,
    upper,
    encoding,
    block_local_conversions,
    block_local_transfer_radius,
    cegar_singletons,
    add_per_iteration,
    max_iterations,
    time_limit,
    workers,
    result_path,
    proto_path,
):
    if (
        shape not in SHAPES
        or upper < 1
        or time_limit <= 0
        or workers < 1
        or add_per_iteration < 1
        or max_iterations < 1
    ):
        raise ValueError("invalid shape, bound, timeout, or worker count")
    if encoding not in {"matching_clauses", "hall_selectors"}:
        raise ValueError("invalid obstruction encoding")
    if block_local_transfer_radius not in {0, 1, 2, 3}:
        raise ValueError("local transfer radius must be between zero and three")
    if block_local_conversions and block_local_transfer_radius:
        raise ValueError("select one local conversion obstruction")
    if result_path.exists() or proto_path.exists():
        raise ValueError("new output paths are required")

    selected = SHAPES[shape]
    residual = tuple(residual_partitions())
    if len(residual) != 966:
        raise AssertionError("residual partition census changed")

    master = IntegerPartitionMaster(N, M, upper)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    favorite_value = master.values[OWNER][FAVORITE]
    for bundle in selected:
        for removed in bundle:
            master.model.Add(
                favorite_value
                >= sum(
                    master.values[OWNER][good]
                    for good in bundle
                    if good != removed
                )
            )
    singleton_pool = []
    singleton_pool_set = set()
    if not cegar_singletons:
        for partition in residual:
            full_partition = ((FAVORITE,),) + partition
            master.add_partition_obstruction(
                full_partition,
                encoding=encoding,
            )
            singleton_pool.append(full_partition)
            singleton_pool_set.add(tuple(sorted(full_partition)))
    conversions = local_favorite_pair_conversions(selected)
    neighborhood = balanced_transfer_neighborhood(
        selected,
        block_local_transfer_radius,
    )
    blocked_local = conversions if block_local_conversions else neighborhood
    if blocked_local:
        for partition in blocked_local:
            master.add_partition_obstruction(partition, encoding=encoding)

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
        if solved.status != "SAT" or not cegar_singletons:
            candidate = solved.values
            break
        values = solved.values
        assert values is not None
        survivors = []
        for partition in residual:
            full_partition = ((FAVORITE,),) + partition
            canonical = tuple(sorted(full_partition))
            if canonical in singleton_pool_set:
                continue
            if matching_rank(feasible_graph(values, full_partition)) == N:
                survivors.append(full_partition)
        trace.append({
            "iteration": iteration,
            "singleton_pool_size_before": len(singleton_pool),
            "supported_unpooled_singleton_partition_count": len(survivors),
            "values": [list(row) for row in values],
            "solver_status": solved.raw_status,
            "solver_wall_seconds": solved.wall_time_seconds,
        })
        if not survivors:
            candidate = values
            break
        for full_partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(
                full_partition,
                encoding=encoding,
            )
            singleton_pool.append(full_partition)
            singleton_pool_set.add(tuple(sorted(full_partition)))
    assert solved is not None
    elapsed = time.time() - started
    status = (
        "THRESHOLD_PASS_WITHOUT_SINGLETON_EFX"
        if solved.status == "SAT" and candidate is not None
        else "BOUNDED_SHORTCUT_UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "ITERATION_LIMIT"
        if solved.status == "SAT"
        else "MASTER_UNKNOWN"
    )

    audit = None
    if candidate is not None:
        if any(
            candidate[agent][FAVORITE]
            <= max(candidate[agent][1:])
            for agent in range(N)
        ):
            raise AssertionError("candidate lost its strict common favorite")
        if not threshold_passes(candidate, OWNER, selected):
            raise AssertionError("candidate lost the selected threshold pass")

        singleton_support = []
        all_support = []
        support_shapes = Counter()
        for partition in core.iter_unlabeled_nonempty_partitions(N, M):
            if matching_rank(feasible_graph(candidate, partition)) != N:
                continue
            all_support.append(partition)
            support_shapes[tuple(sorted(map(len, partition), reverse=True))] += 1
            if (FAVORITE,) in partition:
                singleton_support.append(partition)
        if singleton_support:
            raise AssertionError("candidate has favorite-singleton EFX")

        selected_graph = feasible_graph(
            candidate,
            ((FAVORITE,),) + selected,
        )
        resident_graph = tuple(tuple(row[1:]) for row in selected_graph[1:])
        audit = {
            "selected_owner_threshold_pass": True,
            "selected_partition_resident_hall_rank": matching_rank(
                resident_graph
            ),
            "selected_partition_resident_graph": [
                list(row) for row in resident_graph
            ],
            "selected_partition_deficient_bundle_sets": deficient_bundle_sets(
                resident_graph
            ),
            "favorite_singleton_supporting_partition_count": 0,
            "all_supporting_partition_count": len(all_support),
            "complete_efx_allocation_count": independent.count_complete_efx0(
                candidate
            ),
            "local_favorite_pair_conversion_count": len(conversions),
            "local_favorite_pair_support_count": sum(
                matching_rank(feasible_graph(candidate, partition)) == N
                for partition in conversions
            ),
            "local_transfer_neighborhood_count": len(neighborhood),
            "local_transfer_neighborhood_support_count": sum(
                matching_rank(feasible_graph(candidate, partition)) == N
                for partition in neighborhood
            ),
            "supporting_partition_count_by_shape": {
                "".join(map(str, key)): value
                for key, value in sorted(support_shapes.items())
            },
        }

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": status,
        "n": N,
        "m": M,
        "domain": f"positive integers in [1,{upper}]",
        "upper": upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_shape": shape,
        "selected_residual_partition": [list(bundle) for bundle in selected],
        "favorite_singleton_partition_count": len(residual),
        "cegar_singletons": cegar_singletons,
        "singleton_obstruction_pool_size": len(singleton_pool),
        "cegar_iterations": len(trace),
        "cegar_trace": trace,
        "obstruction_encoding": encoding,
        "block_local_favorite_pair_conversions": block_local_conversions,
        "local_favorite_pair_conversion_count": len(conversions),
        "block_local_transfer_radius": block_local_transfer_radius,
        "blocked_local_partition_count": len(blocked_local),
        "solver_status": solved.raw_status,
        "solver_wall_seconds": solved.wall_time_seconds,
        "elapsed_seconds": elapsed,
        "conflicts": solved.conflicts,
        "branches": solved.branches,
        "values": [list(row) for row in candidate] if candidate else None,
        "candidate_audit": audit,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "A SAT witness refutes only the shortcut that an owner-threshold "
            "pass forces favorite-singleton EFX. Complete EFX may still be "
            "supported by a balanced or other nonsingleton partition."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=tuple(SHAPES), required=True)
    parser.add_argument("--upper", type=int, default=20)
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--cegar-singletons", action="store_true")
    parser.add_argument("--add-per-iteration", type=int, default=128)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument(
        "--block-local-favorite-pair-conversions",
        action="store_true",
    )
    parser.add_argument(
        "--block-local-transfer-radius",
        type=int,
        choices=(1, 2, 3),
        default=0,
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.shape,
        args.upper,
        args.encoding,
        args.block_local_favorite_pair_conversions,
        args.block_local_transfer_radius,
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
