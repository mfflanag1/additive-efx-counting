#!/usr/bin/env python3
"""Decide a fixed-good partial-EFX restart radius at a single wall."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import graph, matching_count
    from .core import iter_unlabeled_nonempty_partitions
    from .decide_row_merge_single_wall_radius import (
        N,
        as_fraction,
        canonical_partition,
        disjoint_subset_pairs,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        partition_distance,
        primitive_rows,
        radius_partitions,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import graph, matching_count
    from core import iter_unlabeled_nonempty_partitions
    from decide_row_merge_single_wall_radius import (
        N,
        as_fraction,
        canonical_partition,
        disjoint_subset_pairs,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        partition_distance,
        primitive_rows,
        radius_partitions,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-partial-entry-radius-lra-v1"


def delete_good(partition, deleted_good):
    reduced = tuple(
        tuple(good for good in bundle if good != deleted_good)
        for bundle in partition
    )
    return canonical_partition(reduced)


def partial_partitions(m, deleted_good):
    remaining = tuple(good for good in range(m) if good != deleted_good)
    found = set()
    for labels in itertools.product(range(N), repeat=len(remaining)):
        if len(set(labels)) != N:
            continue
        found.add(
            canonical_partition(
                tuple(
                    tuple(
                        good
                        for good, label in zip(remaining, labels)
                        if label == bundle
                    )
                    for bundle in range(N)
                )
            )
        )
    return tuple(sorted(found))


def deficient_block_partitions(original, witness_size, deleted_good):
    deficient_goods = tuple(
        good
        for bundle in original[:witness_size]
        for good in bundle
        if good != deleted_good
    )
    outside = tuple(tuple(bundle) for bundle in original[witness_size:])
    found = set()
    for labels in itertools.product(range(witness_size), repeat=len(deficient_goods)):
        if len(set(labels)) != witness_size:
            continue
        internal = tuple(
            tuple(
                good
                for good, label in zip(deficient_goods, labels)
                if label == bundle
            )
            for bundle in range(witness_size)
        )
        found.add(canonical_partition((*internal, *outside)))
    return tuple(sorted(found))


def deficient_block_candidates(original, witness_size, radius):
    deficient_goods = tuple(
        good for bundle in original[:witness_size] for good in bundle
    )
    found = []
    for deleted_good in deficient_goods:
        origin = delete_good(original, deleted_good)
        for partition in deficient_block_partitions(
            original, witness_size, deleted_good
        ):
            if partition_distance(origin, partition) <= radius:
                found.append((deleted_good, partition))
    return tuple(sorted(found))


def global_any_deletion_candidates(original, radius):
    m = sum(len(bundle) for bundle in original)
    return tuple(
        sorted(
            (deleted_good, partition)
            for deleted_good in range(m)
            for partition in radius_partitions(
                delete_good(original, deleted_good), radius
            )
            if all(partition)
        )
    )


def global_wall_isolation(wall_values, post_values, u, w):
    critical = {tuple(sorted((tuple(u), tuple(w))))}
    failures = []
    for left, right in disjoint_subset_pairs(len(wall_values[0])):
        if tuple(sorted((left, right))) in critical:
            continue
        wall_difference = sum(wall_values[0][good] for good in left) - sum(
            wall_values[0][good] for good in right
        )
        post_difference = sum(post_values[0][good] for good in left) - sum(
            post_values[0][good] for good in right
        )
        if wall_difference == 0 or wall_difference * post_difference <= 0:
            failures.append((left, right, wall_difference, post_difference))
    return failures


def audit_model(
    wall_values,
    post_values,
    original,
    u,
    w,
    deleted_goods,
    radius,
    candidates,
    witness_size,
    restart_mode,
):
    wall_graph = literal_graph(wall_values, original)
    post_graph = literal_graph(post_values, original)
    changed = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(N)
        for bundle in range(N)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if changed != ((0, 0, True, False),):
        raise AssertionError("the model changed more than the critical original edge")
    if any(not wall_graph[agent][agent] for agent in range(N)):
        raise AssertionError("the wall allocation is not EFX")
    if any(
        matching_count(graph(post_values, candidate))
        for _deleted_good, candidate in candidates
    ):
        raise AssertionError("an encoded partial entry exists inside the radius")

    support_count = 0
    allocation_count = 0
    histogram = Counter()
    nearest = None
    for deleted_good in deleted_goods:
        origin = delete_good(original, deleted_good)
        partitions = (
            partial_partitions(len(post_values[0]), deleted_good)
            if restart_mode in {"fixed-perturbed", "global-any-deletion"}
            else deficient_block_partitions(
                original, witness_size, deleted_good
            )
        )
        for partition in partitions:
            count = matching_count(graph(post_values, partition))
            if not count:
                continue
            distance = partition_distance(origin, partition)
            support_count += 1
            allocation_count += count
            histogram[distance] += 1
            record = (distance, deleted_good, partition)
            if nearest is None or record < nearest:
                nearest = record

    complete_partition_count = 0
    complete_allocation_count = 0
    for partition in iter_unlabeled_nonempty_partitions(N, len(post_values[0])):
        count = matching_count(graph(post_values, partition))
        if count:
            complete_partition_count += 1
            complete_allocation_count += count

    failures = global_wall_isolation(wall_values, post_values, u, w)
    return {
        "wall_feasibility_graph": [list(row) for row in wall_graph],
        "post_feasibility_graph": [list(row) for row in post_graph],
        "changed_original_partition_edges": [list(item) for item in changed],
        "restart_mode": restart_mode,
        "eligible_deleted_goods": list(deleted_goods),
        "candidate_partition_count": len(candidates),
        "partial_efx_supporting_partition_count": support_count,
        "partial_efx_allocation_count": allocation_count,
        "minimum_partial_efx_transfer_distance": (
            nearest[0] if nearest is not None else None
        ),
        "nearest_partial_efx_deleted_good": (
            nearest[1] if nearest is not None else None
        ),
        "nearest_partial_efx_partition": (
            [list(bundle) for bundle in nearest[2]]
            if nearest is not None
            else None
        ),
        "partial_efx_partition_transfer_distance_histogram": {
            str(distance): histogram[distance] for distance in sorted(histogram)
        },
        "complete_efx_supporting_partition_count": complete_partition_count,
        "complete_efx_allocation_count": complete_allocation_count,
        "global_wall_isolation_verified": not failures,
        "additional_wall_failure_count": len(failures),
        "additional_wall_failure_sample": [
            [list(left), list(right), before, after]
            for left, right, before, after in failures[:12]
        ],
    }


def run(
    result_path,
    smt2_path,
    sizes,
    witness_size,
    radius,
    time_limit,
    skip_global_wall_isolation,
    restart_mode,
):
    if result_path.exists() or smt2_path.exists():
        raise ValueError("result and SMT2 paths must be new")
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    perturbed_good = w[0]
    if restart_mode == "fixed-perturbed":
        deleted_goods = (perturbed_good,)
        partial_origin = delete_good(original, perturbed_good)
        candidates = tuple(
            (perturbed_good, partition)
            for partition in sorted(radius_partitions(partial_origin, radius))
        )
    elif restart_mode == "deficient-block":
        deleted_goods = tuple(
            good
            for bundle in original[:witness_size]
            for good in bundle
        )
        candidates = deficient_block_candidates(original, witness_size, radius)
    elif restart_mode == "global-any-deletion":
        deleted_goods = tuple(range(m))
        candidates = global_any_deletion_candidates(original, radius)
    else:
        raise ValueError("unknown restart mode")

    master = ParkabilityLRAMaster(N, m)
    solver = master.solver
    wall_rows = master.values
    epsilon = z3.Real("wall_epsilon")
    solver.add(epsilon > 0)
    post_row = tuple(
        value + epsilon if good == perturbed_good else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])
    solver.add(zsum(wall_rows[0], u) == zsum(wall_rows[0], w))
    solver.add(
        *(wall_rows[0][critical_good] < wall_rows[0][good] for good in w)
    )
    for target_index, target in enumerate(original):
        if target_index == 0:
            continue
        for removed in target:
            remainder = tuple(good for good in target if good != removed)
            if target_index == 1 and removed == critical_good:
                continue
            solver.add(zsum(wall_rows[0], u) > zsum(wall_rows[0], remainder))

    if not skip_global_wall_isolation:
        critical_pair = {tuple(sorted((u, w)))}
        for left, right in disjoint_subset_pairs(m):
            if tuple(sorted((left, right))) in critical_pair:
                continue
            wall_left = zsum(wall_rows[0], left)
            wall_right = zsum(wall_rows[0], right)
            post_left = zsum(post_row, left)
            post_right = zsum(post_row, right)
            solver.add(wall_left != wall_right)
            solver.add(
                z3.Or(
                    z3.And(wall_left > wall_right, post_left > post_right),
                    z3.And(wall_left < wall_right, post_left < post_right),
                )
            )

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    if skip_global_wall_isolation:
        solver.add(
            *(post_edges[0][bundle] == wall_edges[0][bundle] for bundle in range(1, N))
        )

    deficient_agents = tuple(range(witness_size))
    deficient_bundles = tuple(range(1, witness_size))
    for agent in deficient_agents:
        for bundle in range(N):
            if bundle not in deficient_bundles:
                solver.add(z3.Not(post_edges[agent][bundle]))
    for size in range(1, witness_size):
        for agents in itertools.combinations(deficient_agents, size):
            solver.add(has_matching_expression(post_edges, agents, deficient_bundles))

    for index, (_deleted_good, partition) in enumerate(candidates):
        edges = edge_matrix(solver, post_rows, partition, f"partial_candidate_{index}")
        solver.add(z3.Not(has_matching_expression(edges)))
    smt2_path.write_text(solver.to_smt2())
    formula_sha256 = hashlib.sha256(smt2_path.read_bytes()).hexdigest()

    solver.set(timeout=int(time_limit * 1000))
    started = time.time()
    status = solver.check()
    elapsed = time.time() - started
    model = solver.model() if status == z3.sat else None
    wall_values = None
    post_values = None
    scaled_epsilon = None
    audit = None
    if model is not None:
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        epsilon_fraction = as_fraction(model, epsilon)
        post_fraction = tuple(
            value + (epsilon_fraction if good == perturbed_good else 0)
            for good, value in enumerate(wall_fractions[0])
        )
        wall_values, post_row_values = primitive_rows(wall_fractions, post_fraction)
        post_values = (post_row_values, *wall_values[1:])
        scaled_epsilon = (
            post_values[0][perturbed_good] - wall_values[0][perturbed_good]
        )
        audit = audit_model(
            wall_values,
            post_values,
            original,
            u,
            w,
            deleted_goods,
            radius,
            candidates,
            witness_size,
            restart_mode,
        )

    result = {
        "schema": SCHEMA,
        "status": (
            "PARTIAL_ENTRY_RADIUS_REFUTATION_FOUND"
            if status == z3.sat
            else "UNSAT_CANDIDATE"
            if status == z3.unsat
            else "UNKNOWN"
        ),
        "claim_boundary": (
            "A SAT result refutes only the encoded partial-entry family. An "
            "UNSAT result is confined to the encoded bundle shape, Hall size, "
            "restart mode, and wall assumptions. Neither outcome completes EFX."
        ),
        "domain": "strictly positive additive real valuations",
        "n": N,
        "m": m,
        "bundle_sizes_excluding_critical_good": list(sizes),
        "minimal_hall_witness_size": witness_size,
        "restart_mode": restart_mode,
        "partial_entry_radius": radius,
        "eligible_deleted_goods": list(deleted_goods),
        "candidate_partition_count": len(candidates),
        "global_wall_isolation_encoded": not skip_global_wall_isolation,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "smt2_path": str(smt2_path),
        "smt2_sha256": formula_sha256,
        "wall_partition": [list(bundle) for bundle in original],
        "critical_wall": {
            "moving_bundle_u": list(u),
            "envied_remainder_w": list(w),
            "critical_good": critical_good,
            "perturbed_good": perturbed_good,
        },
        "wall_values": [list(row) for row in wall_values] if wall_values else None,
        "post_wall_values": [list(row) for row in post_values] if post_values else None,
        "scaled_wall_epsilon": scaled_epsilon,
        "audit": audit,
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", type=int, nargs=4, default=(2, 1, 2, 1))
    parser.add_argument("--witness-size", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--skip-global-wall-isolation", action="store_true")
    parser.add_argument(
        "--restart-mode",
        choices=(
            "fixed-perturbed",
            "deficient-block",
            "global-any-deletion",
        ),
        default="fixed-perturbed",
    )
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.result,
        args.smt2,
        tuple(args.sizes),
        args.witness_size,
        args.radius,
        args.time_limit,
        args.skip_global_wall_isolation,
        args.restart_mode,
    )


if __name__ == "__main__":
    main()
