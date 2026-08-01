#!/usr/bin/env python3
"""Exact-real search for a two-swap trapped EFX-matching-rank state."""

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
    from .audit_distinct_half_rank_augmentation import (
        FAVORITE,
        M,
        N,
        audit_branch,
        build_state_graph,
        canonical,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .lra_master import ParkabilityLRAMaster
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
    )
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import (
        FAVORITE,
        M,
        N,
        audit_branch,
        build_state_graph,
        canonical,
    )
    from audit_matching_augmentation import feasible_graph, matching_rank
    from lra_master import ParkabilityLRAMaster
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
    )


SCHEMA = "distinct-half-local-rank-augmentation-lra-result-v1"
START = canonical(((0, 1), (2, 3, 4), (5, 6), (7, 8)))


def add_half_matching(master):
    master.solver.add(
        z3.Or(
            *(
                z3.And(
                    *(
                        2 * master.values[agent][goods[agent]]
                        > master.values[agent][FAVORITE]
                        for agent in range(N)
                    )
                )
                for goods in itertools.permutations(range(1, M), N)
            )
        )
    )


def add_fixed_representatives(master, representatives):
    for agent, good in enumerate(representatives):
        master.solver.add(
            2 * master.values[agent][good]
            > master.values[agent][FAVORITE]
        )


def feasible_edges(master, partition, prefix):
    edges = tuple(
        tuple(z3.Bool(f"{prefix}_agent_{agent}_bundle_{bundle}") for bundle in range(N))
        for agent in range(N)
    )
    for agent in range(N):
        for own_bundle in range(N):
            own = master._sum(agent, partition[own_bundle])
            comparisons = tuple(
                own
                >= master._sum(
                    agent,
                    tuple(good for good in target if good != removed),
                )
                for target_bundle, target in enumerate(partition)
                if target_bundle != own_bundle
                for removed in target
            )
            master.solver.add(edges[agent][own_bundle] == z3.And(*comparisons))
    return edges


def rank_at_least(edges, rank):
    return z3.Or(
        *(
            z3.And(
                *(edges[agents[index]][bundles[index]] for index in range(rank))
            )
            for agents in itertools.combinations(range(N), rank)
            for bundles in itertools.permutations(range(N), rank)
        )
    )


def run(
    result_path,
    smt2_path,
    target_rank,
    time_limit,
    representatives,
    start_matching,
):
    universe, neighbors = build_state_graph()
    positions = {partition: index for index, partition in enumerate(universe)}
    start = positions[START]
    first = neighbors[start]
    radius_two = tuple(sorted({start, *first, *(item for p in first for item in neighbors[p])}))

    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure_cardinal(master)
    if representatives is None:
        add_half_matching(master)
    else:
        add_fixed_representatives(master, representatives)

    rank_ge = {}
    edges_by_position = {}
    for position in radius_two:
        edges = feasible_edges(master, universe[position], f"state_{position}")
        edges_by_position[position] = edges
        for rank in (target_rank, target_rank + 1):
            variable = z3.Bool(f"state_{position}_rank_ge_{rank}")
            master.solver.add(variable == rank_at_least(edges, rank))
            rank_ge[position, rank] = variable

    if start_matching is None:
        master.solver.add(rank_ge[start, target_rank])
    else:
        master.solver.add(
            *(edges_by_position[start][agent][bundle]
              for agent, bundle in enumerate(start_matching))
        )
    master.solver.add(z3.Not(rank_ge[start, target_rank + 1]))
    for neighbor in first:
        master.solver.add(z3.Not(rank_ge[neighbor, target_rank + 1]))
        for second in neighbors[neighbor]:
            master.solver.add(
                z3.Or(
                    z3.Not(rank_ge[neighbor, target_rank]),
                    z3.Not(rank_ge[second, target_rank + 1]),
                )
            )

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    values = solved.values
    if values is not None:
        audited_representatives = audit_branch(values)
        if representatives is not None and any(
            2 * values[agent][good] <= values[agent][FAVORITE]
            for agent, good in enumerate(representatives)
        ):
            raise AssertionError("model lost its fixed representatives")
        ranks = {
            position: matching_rank(feasible_graph(values, universe[position]))
            for position in radius_two
        }
        if ranks[start] != target_rank:
            raise AssertionError("model lost the target starting rank")
        if any(ranks[position] > target_rank for position in first):
            raise AssertionError("model has a one-swap rank augmentation")
        if any(
            ranks[first_position] == target_rank
            and ranks[second_position] > target_rank
            for first_position in first
            for second_position in neighbors[first_position]
        ):
            raise AssertionError("model has a two-swap plateau augmentation")
    else:
        audited_representatives = None

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    status = (
        "UNSAT_CANDIDATE"
        if solved.status == "UNSAT"
        else "TWO_SWAP_TRAP_FOUND"
        if solved.status == "SAT"
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
        "universal_owner_threshold_failure": True,
        "existential_half_favorite_matching": representatives is None,
        "representative_mode": (
            "existential" if representatives is None else "fixed_orbit"
        ),
        "fixed_half_favorite_representatives": (
            list(representatives) if representatives is not None else None
        ),
        "target_starting_rank": target_rank,
        "fixed_start_partial_matching": (
            list(start_matching) if start_matching is not None else None
        ),
        "fixed_start_partition": [list(bundle) for bundle in START],
        "first_neighbor_count": len(first),
        "radius_two_partition_count": len(radius_two),
        "elapsed_seconds": elapsed,
        "values": [list(row) for row in values] if values is not None else None,
        "half_favorite_representatives": (
            list(audited_representatives)
            if audited_representatives is not None
            else None
        ),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE proves, subject to independent replay, that a "
            f"rank-{target_rank} favorite-pair state in the exact branch "
            "cannot avoid higher matching rank for two swaps: the first "
            "swap may preserve rank and the second must augment."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--rank", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument(
        "--representatives",
        help="four comma-separated distinct residual goods for a fixed orbit",
    )
    parser.add_argument(
        "--start-matching",
        help="rank-many comma-separated distinct bundles matched to agents 0,1,...",
    )
    args = parser.parse_args()
    if args.time_limit < 0:
        parser.error("time limit cannot be negative")
    representatives = None
    if args.representatives is not None:
        try:
            representatives = tuple(
                int(item) for item in args.representatives.split(",")
            )
        except ValueError:
            parser.error("representatives must be integers")
        if (
            len(representatives) != N
            or len(set(representatives)) != N
            or any(not 1 <= good < M for good in representatives)
        ):
            parser.error("representatives must be four distinct residual goods")
    start_matching = None
    if args.start_matching is not None:
        try:
            start_matching = tuple(
                int(item) for item in args.start_matching.split(",")
            )
        except ValueError:
            parser.error("start matching must be integers")
        if (
            len(start_matching) != args.rank
            or len(set(start_matching)) != args.rank
            or any(not 0 <= bundle < N for bundle in start_matching)
        ):
            parser.error("start matching must name rank-many distinct bundles")
    result = run(
        args.result,
        args.smt2,
        args.rank,
        args.time_limit,
        representatives,
        start_matching,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
