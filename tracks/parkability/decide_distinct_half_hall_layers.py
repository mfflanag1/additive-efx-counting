#!/usr/bin/env python3
"""Exact-real decision workbench for Hall-witness layers of the EFX gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
        sorted_descending,
    )
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
        sorted_descending,
    )


SCHEMA = "distinct-half-hall-layer-lra-result-v1"
N = 4
M = 9
FAVORITE = 0


def edge_rejection(master, observer, own_bundle, partition):
    own = master._sum(observer, partition[own_bundle])
    return z3.Or(
        *(
            master._sum(observer, tuple(good for good in target if good != removed))
            > own
            for target_index, target in enumerate(partition)
            if target_index != own_bundle
            for removed in target
        )
    )


def hall_witnesses(master, partition, maximum_size):
    reject = tuple(
        tuple(
            edge_rejection(master, observer, own_bundle, partition)
            for own_bundle in range(N)
        )
        for observer in range(N)
    )
    witnesses = []
    for size in range(2, maximum_size + 1):
        for observers in itertools.combinations(range(N), size):
            for allowed_bundles in itertools.combinations(range(N), size - 1):
                allowed = set(allowed_bundles)
                witnesses.append(
                    z3.And(
                        *(
                            reject[observer][bundle]
                            for observer in observers
                            for bundle in range(N)
                            if bundle not in allowed
                        )
                    )
                )
    return witnesses


def add_branch(master, rank_branch, *, threshold_encoding="cardinal"):
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    for observer in range(N):
        master.solver.add(
            2 * master.values[observer][observer + 1]
            > master.values[observer][FAVORITE]
        )
    if threshold_encoding == "cardinal":
        add_universal_threshold_failure_cardinal(master)
    elif threshold_encoding == "sorting":
        add_universal_threshold_failure(master)
    else:
        raise ValueError("threshold encoding must be cardinal or sorting")
    if rank_branch is not None:
        for observer, branch in enumerate(rank_branch):
            ordered = sorted_descending(master.values[observer][1:])
            favorite = master.values[observer][FAVORITE]
            master.solver.add(
                ordered[2] + ordered[6] > favorite
                if branch == "B"
                else ordered[3] + ordered[4] > favorite
            )


def minimum_hall_witness_size(values, partition):
    graph = tuple(
        tuple(
            all(
                own_bundle == target_index
                or sum(row[good] for good in partition[own_bundle])
                >= sum(row[good] for good in target if good != removed)
                for target_index, target in enumerate(partition)
                for removed in target
            )
            for own_bundle in range(N)
        )
        for row in values
    )
    for size in (2, 3, 4):
        for observers in itertools.combinations(range(N), size):
            neighborhood = {
                bundle
                for bundle in range(N)
                if any(graph[observer][bundle] for observer in observers)
            }
            if len(neighborhood) < size:
                return size
    return None


def run(
    result_path: Path,
    smt2_path: Path,
    target: str,
    time_limit: float,
    rank_branch: str | None,
):
    maximum_size = {"two": 2, "three": 3, "full": 4}[target]
    universe = favorite_pair_balanced_universe()
    master = ParkabilityLRAMaster(N, M)
    add_branch(master, rank_branch)
    for partition in universe:
        master.solver.add(z3.Or(*hall_witnesses(master, partition, maximum_size)))

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    values = solved.values
    if values is not None:
        audit_threshold_failure(values)
        if any(
            minimum_hall_witness_size(values, partition) is None
            or minimum_hall_witness_size(values, partition) > maximum_size
            for partition in universe
        ):
            raise AssertionError("model does not satisfy every layered obstruction")
    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    status = (
        "UNSAT_CANDIDATE" if solved.status == "UNSAT"
        else "SAT_LAYER_OBSTRUCTION" if solved.status == "SAT"
        else "MASTER_UNKNOWN"
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "favorite": FAVORITE,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "rank_disjunct_branch": rank_branch,
        "target": target,
        "maximum_allowed_hall_witness_size": maximum_size,
        "target_partition_count": len(universe),
        "elapsed_seconds": elapsed,
        "values": [list(row) for row in values] if values is not None else None,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE says every profile in the branch has a "
            "favorite-pair balanced partition with no Hall witness up to "
            f"size {maximum_size}. Only target=full is the EFX statement."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--target", choices=("two", "three", "full"), required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--rank-branch")
    args = parser.parse_args()
    if args.time_limit < 0:
        parser.error("time limit cannot be negative")
    if args.rank_branch is not None and (
        len(args.rank_branch) != N or set(args.rank_branch) - {"B", "C"}
    ):
        parser.error("rank branch must be a four-character B/C string")
    result = run(
        args.result,
        args.smt2,
        args.target,
        args.time_limit,
        args.rank_branch,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
