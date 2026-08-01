#!/usr/bin/env python3
"""CEGAR for selecting a prescribed mixed Hall witness motif."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

import ortools

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        OWNER,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from .integer_partition_master import IntegerPartitionMaster
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        OWNER,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from integer_partition_master import IntegerPartitionMaster


SCHEMA = "common-favorite-mixed-selection-cegar-v1"


def resident_graph(values, owner, partition):
    graph = feasible_graph(values, ((FAVORITE,),) + partition)
    return tuple(
        tuple(graph[agent][bundle] for bundle in range(1, N))
        for agent in range(N)
        if agent != owner
    )


def selection_motifs(values, residual, motif_type):
    motifs = []
    for partition_index, partition in enumerate(residual):
        for owner in range(N):
            if not threshold_passes(values, owner, partition):
                continue
            graph = resident_graph(values, owner, partition)
            if matching_rank(graph) != N - 2:
                continue
            if motif_type == "rank_two":
                motifs.append((owner, partition_index, None))
            else:
                for bundle in range(N - 1):
                    if not any(row[bundle] for row in graph):
                        motifs.append((owner, partition_index, bundle))
    return motifs


def add_motif_obstruction(master, owner, partition, zero_bundle, motif_index):
    full = ((FAVORITE,),) + partition
    masks = tuple(sum(1 << good for good in bundle) for bundle in full)
    owner_violations = []
    for target in range(1, N):
        for removed in full[target]:
            remainder = masks[target] ^ (1 << removed)
            if remainder:
                owner_violations.append(
                    master._violation(owner, masks[0], remainder)
                )

    residents = tuple(agent for agent in range(N) if agent != owner)
    feasible = {}
    for resident in residents:
        for bundle in range(N - 1):
            own_column = bundle + 1
            violations = master._edge_violations(
                resident,
                own_column,
                full,
                masks,
            )
            edge = master.model.NewBoolVar(
                f"mixed_motif_{motif_index}_resident_{resident}_bundle_{bundle}"
            )
            if violations:
                master.model.AddBoolAnd(
                    [violation.Not() for violation in violations]
                ).OnlyEnforceIf(edge)
                master.model.AddBoolOr(violations).OnlyEnforceIf(edge.Not())
            else:
                master.model.Add(edge == 1)
            feasible[resident, bundle] = edge

    clauses = 0
    bundle_pairs = (
        itertools.permutations(range(N - 1), 2)
        if zero_bundle is None
        else (
            tuple(bundle for bundle in range(N - 1) if bundle != zero_bundle),
            tuple(
                reversed(
                    tuple(
                        bundle
                        for bundle in range(N - 1)
                        if bundle != zero_bundle
                    )
                )
            ),
        )
    )
    bundle_pairs = tuple(bundle_pairs)
    for left, right in itertools.combinations(residents, 2):
        for first, second in bundle_pairs:
            zero_escape = (
                ()
                if zero_bundle is None
                else tuple(
                    feasible[resident, zero_bundle] for resident in residents
                )
            )
            master.model.AddBoolOr([
                *owner_violations,
                feasible[left, first].Not(),
                feasible[right, second].Not(),
                *zero_escape,
            ])
            clauses += 1
    expected_clauses = 18 if zero_bundle is None else 6
    if clauses != expected_clauses:
        raise AssertionError("rank-two motif clause census changed")
    return clauses


def run(
    shape,
    upper,
    motif_type,
    time_limit,
    workers,
    add_per_iteration,
    max_iterations,
    result_path,
    proto_path,
):
    if (
        shape not in SHAPES
        or motif_type not in {"rank_two", "zero_neighbor_rank_two"}
        or upper < 1
        or time_limit <= 0
        or workers < 1
        or add_per_iteration < 1
        or max_iterations < 1
        or result_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("invalid arguments or existing outputs")
    selected = SHAPES[shape]
    residual = tuple(residual_partitions())

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
    for partition in residual:
        master.add_partition_obstruction(((FAVORITE,),) + partition)

    learned = set()
    trace = []
    candidate = None
    solved = None
    started = time.time()
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
        motifs = [
            motif
            for motif in selection_motifs(values, residual, motif_type)
            if motif not in learned
        ]
        trace.append({
            "iteration": iteration,
            "learned_motif_count_before": len(learned),
            "unlearned_selection_motif_count": len(motifs),
            "values": [list(row) for row in values],
            "solver_status": solved.raw_status,
            "solver_wall_seconds": solved.wall_time_seconds,
        })
        if not motifs:
            candidate = values
            break
        for motif in motifs[:add_per_iteration]:
            owner, partition_index, zero_bundle = motif
            add_motif_obstruction(
                master,
                owner,
                residual[partition_index],
                zero_bundle,
                len(learned),
            )
            learned.add(motif)
    assert solved is not None

    status = (
        "ZERO_NEIGHBOR_SELECTION_COUNTEREXAMPLE"
        if candidate is not None
        else "BOUNDED_SELECTION_UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "MASTER_UNKNOWN"
        if solved.status != "SAT"
        else "ITERATION_LIMIT"
    )
    candidate_audit = None
    if candidate is not None:
        surviving_singletons = sum(
            matching_rank(
                feasible_graph(candidate, ((FAVORITE,),) + partition)
            )
            == N
            for partition in residual
        )
        if surviving_singletons:
            raise AssertionError("candidate gained favorite-singleton EFX")
        motifs = selection_motifs(candidate, residual, motif_type)
        if motifs:
            raise AssertionError("candidate retained the selected motif")
        candidate_audit = {
            "favorite_singleton_supporting_partition_count": 0,
            "threshold_pass_count": sum(
                threshold_passes(candidate, owner, partition)
                for partition in residual
                for owner in range(N)
            ),
            "surviving_selection_motif_count": 0,
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
        "upper": upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_shape": shape,
        "selected_residual_partition": [list(bundle) for bundle in selected],
        "selection_motif": motif_type,
        "favorite_singleton_partition_count": len(residual),
        "learned_motif_count": len(learned),
        "iterations": len(trace),
        "trace": trace,
        "solver_status": solved.raw_status,
        "solver_wall_seconds": solved.wall_time_seconds,
        "elapsed_seconds": time.time() - started,
        "values": [list(row) for row in candidate] if candidate else None,
        "candidate_audit": candidate_audit,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "A SAT candidate refutes only the named selection claim for "
            f"motif {motif_type}. It is not an EFX counterexample. UNSAT "
            "requires independent replay."
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
        "--motif",
        choices=("rank_two", "zero_neighbor_rank_two"),
        default="zero_neighbor_rank_two",
    )
    parser.add_argument("--time-limit", type=float, default=60)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=3)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.shape,
        args.upper,
        args.motif,
        args.time_limit,
        args.workers,
        args.add_per_iteration,
        args.max_iterations,
        args.result,
        args.proto,
    )


if __name__ == "__main__":
    main()
