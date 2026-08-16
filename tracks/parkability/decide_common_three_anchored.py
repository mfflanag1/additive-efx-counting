#!/usr/bin/env python3
"""Decide the anchored-balanced lemma in the common-three branch."""

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
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from lra_master import ParkabilityLRAMaster


SCHEMA = "common-three-anchored-lra-result-v1"
N = 4
M = 9
FAVORITE = 0
HIGH_GOODS = (1, 2, 3)
LOW_GOODS = (4, 5, 6, 7, 8)


Partition = tuple[tuple[int, ...], ...]


def anchored_partitions() -> tuple[Partition, ...]:
    """Return all anchor-separated partitions of shape 3+2+2+2."""
    partitions = set()
    anchors = (FAVORITE,) + HIGH_GOODS
    for assignment in itertools.product(range(N), repeat=len(LOW_GOODS)):
        counts = tuple(assignment.count(slot) for slot in range(N))
        if sorted(counts) != [1, 1, 1, 2]:
            continue
        partitions.add(
            tuple(
                sorted(
                    (anchor,)
                    + tuple(
                        low
                        for low, slot_assigned in zip(LOW_GOODS, assignment)
                        if slot_assigned == slot
                    )
                    for slot, anchor in enumerate(anchors)
                )
            )
        )
    result = tuple(sorted(partitions))
    if len(result) != 240:
        raise AssertionError("anchored partition universe changed")
    return result


def add_common_three_constraints(master: ParkabilityLRAMaster) -> None:
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    master.add_favorite_pattern_stabilizer((FAVORITE,) * N)
    for observer, row in enumerate(master.values):
        favorite = row[FAVORITE]
        master.solver.add(
            *(2 * row[good] > favorite for good in HIGH_GOODS),
            *(2 * row[good] <= favorite for good in LOW_GOODS),
        )
        master.solver.add(
            z3.Or(
                *(
                    z3.And(
                        *(
                            row[high] + row[low] > favorite
                            for high in HIGH_GOODS
                            for low in LOW_GOODS
                            if low != exceptional_low
                        )
                    )
                    for exceptional_low in LOW_GOODS
                )
            )
        )


def audit_branch(values: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    qualifying_counts = []
    for row in values:
        favorite = row[FAVORITE]
        if not all(favorite > row[good] for good in range(1, M)):
            raise AssertionError("model lost its strict common favorite")
        if not all(2 * row[good] > favorite for good in HIGH_GOODS):
            raise AssertionError("model lost a common high good")
        if not all(2 * row[good] <= favorite for good in LOW_GOODS):
            raise AssertionError("model gained an extra high good")
        qualifying_lows = tuple(
            low
            for low in LOW_GOODS
            if all(row[high] + row[low] > favorite for high in HIGH_GOODS)
        )
        if len(qualifying_lows) < 4:
            raise AssertionError("model violated the first-wall branch")
        qualifying_counts.append(len(qualifying_lows))
    return tuple(qualifying_counts)


def supported_partitions(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    audit_branch(values)
    return tuple(
        partition
        for partition in universe
        if matching_rank(feasible_graph(values, partition)) == N
    )


def audit_model(values: tuple[tuple[int, ...], ...], universe: tuple[Partition, ...]) -> dict:
    qualifying_counts = audit_branch(values)
    supported = tuple(
        supported_partitions(values, universe)
    )
    if supported:
        raise AssertionError("model supports a target anchored partition")
    return {
        "strict_common_favorite": True,
        "shared_half_favorite_set": list(HIGH_GOODS),
        "qualifying_low_counts": list(qualifying_counts),
        "supported_target_partitions": 0,
    }


def run(
    *,
    result_path: Path,
    smt2_path: Path,
    time_limit_s: float,
    encoding: str,
    cegar_add: int,
    max_iterations: int,
) -> dict:
    universe = anchored_partitions()
    master = ParkabilityLRAMaster(N, M)
    add_common_three_constraints(master)
    started = time.time()
    trace = []
    values = None
    if cegar_add == 0:
        for partition in universe:
            master.add_partition_obstruction(partition, encoding=encoding)
        solved = master.solve(time_limit_s=time_limit_s)
        status = solved.status
        values = solved.values
    else:
        solved = None
        status = "ITERATION_LIMIT"
        pool = set()
        for iteration in range(1, max_iterations + 1):
            solved = master.solve(time_limit_s=time_limit_s)
            if solved.status != "SAT":
                status = solved.status
                break
            assert solved.values is not None
            survivors = tuple(
                partition
                for partition in supported_partitions(solved.values, universe)
                if partition not in pool
            )
            trace.append({
                "iteration": iteration,
                "pool_size_before": len(pool),
                "supported_partition_count": len(survivors),
                "values": [list(row) for row in solved.values],
            })
            print(
                f"iteration={iteration} pool={len(pool)} "
                f"supported_partitions={len(survivors)}",
                flush=True,
            )
            if not survivors:
                status = "SAT_TARGET_OBSTRUCTION"
                values = solved.values
                break
            for partition in survivors[:cegar_add]:
                master.add_partition_obstruction(partition, encoding=encoding)
                pool.add(partition)
        assert solved is not None
    elapsed_seconds = time.time() - started
    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)

    semantic_audit = None
    if values is not None:
        semantic_audit = audit_model(values, universe)
    result = {
        "schema": SCHEMA,
        "status": solved.status,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "favorite": FAVORITE,
        "shared_half_favorite_set": list(HIGH_GOODS),
        "low_goods": list(LOW_GOODS),
        "branch": (
            "Each agent has at least four low goods that pair above its "
            "favorite with every shared high good."
        ),
        "target_family": (
            "All anchor-separated partitions of shape 3+2+2+2 with one "
            "anchor from {0,1,2,3} in each bundle."
        ),
        "target_partition_count": len(universe),
        "cegar_add": cegar_add,
        "max_iterations": max_iterations,
        "pool_size": master.pool_size,
        "trace": trace,
        "obstruction_encoding": encoding,
        "symmetry": "common-favorite row lex and unused-good column lex",
        "elapsed_seconds": elapsed_seconds,
        "values": [list(row) for row in values] if values is not None else None,
        "semantic_audit": semantic_audit,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT proves the target anchored family contains an EFX "
            "allocation throughout this common-three subbranch. SAT is "
            "only a counterexample to that target family, not to EFX existence."
        ),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=1200)
    parser.add_argument(
        "--cegar-add",
        type=int,
        default=0,
        help="add this many surviving partitions per iteration; zero loads all",
    )
    parser.add_argument("--max-iterations", type=int, default=50)
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "inline_matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    args = parser.parse_args()
    if args.time_limit < 0 or args.cegar_add < 0 or args.max_iterations < 1:
        parser.error("time limit cannot be negative")
    result = run(
        result_path=args.result,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
        encoding=args.encoding,
        cegar_add=args.cegar_add,
        max_iterations=args.max_iterations,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
