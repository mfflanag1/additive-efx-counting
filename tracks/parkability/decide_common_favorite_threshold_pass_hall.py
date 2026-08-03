#!/usr/bin/env python3
"""Decide whether one owner-threshold pass forces favorite-singleton EFX."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from lra_master import ParkabilityLRAMaster


SCHEMA = "common-favorite-threshold-pass-hall-lra-v1"
N = 4
M = 9
FAVORITE = 0
OWNER = 0
SHAPES = {
    "611": ((1, 2, 3, 4, 5, 6), (7,), (8,)),
    "521": ((1, 2, 3, 4, 5), (6, 7), (8,)),
    "431": ((1, 2, 3, 4), (5, 6, 7), (8,)),
    "422": ((1, 2, 3, 4), (5, 6), (7, 8)),
    "332": ((1, 2, 3), (4, 5, 6), (7, 8)),
}


def residual_partitions():
    residual = tuple(range(1, M))
    for partition in core.iter_unlabeled_nonempty_partitions(N - 1, M - 1):
        yield tuple(
            tuple(residual[index] for index in bundle) for bundle in partition
        )


def threshold_passes(values, owner, bundles):
    favorite = values[owner][FAVORITE]
    return all(
        favorite
        >= sum(values[owner][good] for good in bundle if good != removed)
        for bundle in bundles
        for removed in bundle
    )


def supported_partition(values, partition):
    return matching_rank(feasible_graph(values, partition)) == N


def deficient_bundle_sets(graph):
    witnesses = []
    for size in range(1, len(graph) + 1):
        for bundles in itertools.combinations(range(len(graph)), size):
            neighbors = tuple(
                agent
                for agent, row in enumerate(graph)
                if any(row[bundle] for bundle in bundles)
            )
            if len(neighbors) < len(bundles):
                witnesses.append({
                    "bundles": list(bundles),
                    "resident_neighbors": list(neighbors),
                })
    return witnesses


def run(shape, encoding, time_limit, integer_upper, result_path, formula_path):
    if shape not in SHAPES or time_limit <= 0:
        raise ValueError("invalid shape or time limit")
    if encoding not in {"matching_clauses", "hall_selectors"}:
        raise ValueError("invalid obstruction encoding")
    if integer_upper is not None and integer_upper < 1:
        raise ValueError("integer upper bound must be positive")
    if result_path.exists() or formula_path.exists():
        raise ValueError("new output paths are required")

    selected = SHAPES[shape]
    residual = tuple(residual_partitions())
    if len(residual) != 966:
        raise AssertionError("residual partition census changed")

    master = ParkabilityLRAMaster(N, M, integer_upper=integer_upper)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    favorite_value = master.values[OWNER][FAVORITE]
    for bundle in selected:
        for removed in bundle:
            master.solver.add(
                favorite_value
                >= sum(
                    master.values[OWNER][good]
                    for good in bundle
                    if good != removed
                )
            )
    for partition in residual:
        master.add_partition_obstruction(
            ((FAVORITE,),) + partition,
            encoding=encoding,
        )

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started

    status = (
        "THRESHOLD_PASS_WITHOUT_SINGLETON_EFX"
        if solved.status == "SAT"
        else "THRESHOLD_PASS_FORCES_SINGLETON_EFX_CANDIDATE"
        if solved.status == "UNSAT"
        else "MASTER_UNKNOWN"
    )
    candidate = None
    audit = None
    if solved.status == "SAT":
        candidate = solved.values
        assert candidate is not None
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
            if not supported_partition(candidate, partition):
                continue
            all_support.append(partition)
            support_shapes[tuple(sorted(map(len, partition), reverse=True))] += 1
            if (FAVORITE,) in partition:
                singleton_support.append(partition)
        if singleton_support:
            raise AssertionError("candidate has favorite-singleton EFX")
        literal_count = independent.count_complete_efx0(candidate)
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
            "complete_efx_allocation_count": literal_count,
            "supporting_partition_count_by_shape": {
                "".join(map(str, key)): value
                for key, value in sorted(support_shapes.items())
            },
        }

    result = {
        "schema": SCHEMA,
        "status": status,
        "n": N,
        "m": M,
        "domain": (
            f"positive integers in [1,{integer_upper}]"
            if integer_upper is not None
            else "strictly positive reals normalized per row"
        ),
        "integer_upper": integer_upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_shape": shape,
        "selected_residual_partition": [list(bundle) for bundle in selected],
        "selected_owner_threshold_pass": True,
        "favorite_singleton_partition_count": len(residual),
        "obstruction_encoding": encoding,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "solver_wall_seconds": elapsed,
        "values": [list(row) for row in candidate] if candidate else None,
        "values_sha256": (
            hashlib.sha256(
                json.dumps(candidate, separators=(",", ":")).encode()
            ).hexdigest()
            if candidate
            else None
        ),
        "candidate_audit": audit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "SAT refutes only the shortcut that any owner-threshold-passing "
            "residual partition forces favorite-singleton EFX. It does not "
            "refute balanced EFX, the common-favorite dichotomy, or general EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=tuple(SHAPES), required=True)
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--integer-upper", type=int)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.shape,
        args.encoding,
        args.time_limit,
        args.integer_upper,
        args.result,
        args.formula,
    )


if __name__ == "__main__":
    main()
