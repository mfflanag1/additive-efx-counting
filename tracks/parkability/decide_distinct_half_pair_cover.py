#!/usr/bin/env python3
"""Test the safe-pair normal form in the distinct half-favorite branch."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .audit_favorite_singleton_hall_boundaries import residual_partitions
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from audit_favorite_singleton_hall_boundaries import residual_partitions
    from lra_master import ParkabilityLRAMaster


SCHEMA = "distinct-half-pair-cover-lra-result-v1"
N = 4
M = 9
FAVORITE = 0
REPRESENTATIVES = (1, 2, 3, 4)

Partition = tuple[tuple[int, ...], ...]
PairState = tuple[tuple[int, ...], ...]


def pair_state_universe() -> tuple[PairState, ...]:
    states = []
    for partition in core.iter_unlabeled_nonempty_partitions(5, M):
        if tuple(sorted(map(len, partition), reverse=True)) != (2, 2, 2, 2, 1):
            continue
        states.append(tuple(bundle for bundle in partition if len(bundle) == 2))
    result = tuple(states)
    if len(result) != 945:
        raise AssertionError("four-pair state universe changed")
    return result


def balanced_state_universe() -> tuple[Partition, ...]:
    result = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
    )
    if len(result) != 1260:
        raise AssertionError("balanced state universe changed")
    return result


def favorite_pair_balanced_universe() -> tuple[Partition, ...]:
    result = tuple(
        partition
        for partition in balanced_state_universe()
        if len(next(bundle for bundle in partition if FAVORITE in bundle)) == 2
    )
    if len(result) != 840:
        raise AssertionError("favorite-pair balanced universe changed")
    return result


def favorite_triple_balanced_universe() -> tuple[Partition, ...]:
    result = tuple(
        partition
        for partition in balanced_state_universe()
        if len(next(bundle for bundle in partition if FAVORITE in bundle)) == 3
    )
    if len(result) != 420:
        raise AssertionError("favorite-triple balanced universe changed")
    return result


def add_branch_constraints(master: ParkabilityLRAMaster) -> None:
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    for observer, representative in enumerate(REPRESENTATIVES):
        row = master.values[observer]
        favorite = row[FAVORITE]
        master.solver.add(2 * row[representative] > favorite)
        for partition in residual_partitions():
            master.solver.add(
                z3.Or(
                    *(
                        master._sum(
                            observer,
                            tuple(good for good in bundle if good != removed),
                        )
                        > favorite
                        for bundle in partition
                        for removed in bundle
                    )
                )
            )


def has_perfect_matching(graph: tuple[tuple[bool, ...], ...]) -> bool:
    return any(
        all(graph[observer][matching[observer]] for observer in range(N))
        for matching in itertools.permutations(range(N))
    )


def supported_pair_states(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[PairState, ...],
) -> tuple[PairState, ...]:
    return tuple(
        state
        for state in universe
        if has_perfect_matching(
            tuple(
                tuple(
                    sum(row[good] for good in pair) >= row[FAVORITE]
                    for pair in state
                )
                for row in values
            )
        )
    )


def add_pair_state_obstruction(
    master: ParkabilityLRAMaster,
    state: PairState,
) -> None:
    for matching in itertools.permutations(range(N)):
        master.solver.add(
            z3.Or(
                *(
                    master._sum(observer, state[matching[observer]])
                    < master.values[observer][FAVORITE]
                    for observer in range(N)
                )
            )
        )


def favorite_dominated(
    values: tuple[tuple[int, ...], ...],
    state: Partition,
) -> bool:
    for observer, row in enumerate(values):
        favorite = row[FAVORITE]
        for bundle in state:
            for removed in bundle:
                if (
                    sum(row[good] for good in bundle if good != removed)
                    > favorite
                ):
                    return False
    graph = tuple(
        tuple(
            sum(row[good] for good in bundle) >= row[FAVORITE]
            for bundle in state
        )
        for row in values
    )
    return has_perfect_matching(graph)


def supported_balanced_states(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    return tuple(state for state in universe if favorite_dominated(values, state))


def supported_efx_states(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    return tuple(
        state
        for state in universe
        if matching_rank(feasible_graph(values, state)) == N
    )


def favorite_triple_pair_graph(values, state):
    triple = next(bundle for bundle in state if FAVORITE in bundle)
    lows = tuple(good for good in triple if good != FAVORITE)
    pairs = tuple(bundle for bundle in state if bundle != triple)
    return tuple(
        tuple(
            sum(row[good] for good in pair)
            >= row[FAVORITE] + max(row[good] for good in lows)
            for pair in pairs
        )
        for row in values
    )


def supported_favorite_triple_states(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    return tuple(
        state
        for state in universe
        if any(
            all(
                favorite_triple_pair_graph(values, state)[agent][pair]
                for pair, agent in enumerate(agents)
            )
            for agents in itertools.permutations(range(N), 3)
        )
    )


def add_favorite_triple_state_obstruction(
    master: ParkabilityLRAMaster,
    state: Partition,
) -> None:
    triple = next(bundle for bundle in state if FAVORITE in bundle)
    lows = tuple(good for good in triple if good != FAVORITE)
    pairs = tuple(bundle for bundle in state if bundle != triple)
    for agents in itertools.permutations(range(N), 3):
        master.solver.add(
            z3.Or(
                *(
                    master._sum(agent, pairs[pair])
                    < (
                        master.values[agent][FAVORITE]
                        + master.values[agent][low]
                    )
                    for pair, agent in enumerate(agents)
                    for low in lows
                )
            )
        )


def supported_floor_states(
    values: tuple[tuple[int, ...], ...],
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    return tuple(
        state
        for state in universe
        if has_perfect_matching(
            tuple(
                tuple(
                    sum(row[good] for good in bundle) >= row[FAVORITE]
                    for bundle in state
                )
                for row in values
            )
        )
    )


def add_floor_state_obstruction(
    master: ParkabilityLRAMaster,
    state: Partition,
) -> None:
    for matching in itertools.permutations(range(N)):
        master.solver.add(
            z3.Or(
                *(
                    master._sum(observer, state[matching[observer]])
                    < master.values[observer][FAVORITE]
                    for observer in range(N)
                )
            )
        )


def add_floor_state_hall_obstruction(
    master: ParkabilityLRAMaster,
    state: Partition,
) -> None:
    witnesses = []
    for observer_mask in range(1, 1 << N):
        observers = tuple(
            observer
            for observer in range(N)
            if observer_mask & (1 << observer)
        )
        for neighborhood_size in range(len(observers)):
            for neighborhood in itertools.combinations(
                range(N),
                neighborhood_size,
            ):
                allowed = set(neighborhood)
                witnesses.append(
                    z3.And(
                        *(
                            master._sum(observer, state[bundle])
                            < master.values[observer][FAVORITE]
                            for observer in observers
                            for bundle in range(N)
                            if bundle not in allowed
                        )
                    )
                )
    master.solver.add(z3.Or(*witnesses))


def add_balanced_state_obstruction(
    master: ParkabilityLRAMaster,
    state: Partition,
) -> None:
    target_violations = tuple(
        master._sum(
            observer,
            tuple(good for good in bundle if good != removed),
        )
        > master.values[observer][FAVORITE]
        for observer in range(N)
        for bundle in state
        for removed in bundle
    )
    for matching in itertools.permutations(range(N)):
        master.solver.add(
            z3.Or(
                *target_violations,
                *(
                    master._sum(observer, state[matching[observer]])
                    < master.values[observer][FAVORITE]
                    for observer in range(N)
                ),
            )
        )


def audit_branch(values: tuple[tuple[int, ...], ...]) -> None:
    for observer, representative in enumerate(REPRESENTATIVES):
        row = values[observer]
        favorite = row[FAVORITE]
        if any(favorite <= row[good] for good in range(1, M)):
            raise AssertionError("model lost its strict common favorite")
        if 2 * row[representative] <= favorite:
            raise AssertionError("model lost its fixed half-favorite representative")
        for partition in residual_partitions():
            threshold = max(
                sum(row[good] for good in bundle)
                - min(row[good] for good in bundle)
                for bundle in partition
            )
            if threshold <= favorite:
                raise AssertionError("model lost universal threshold failure")


def run(
    *,
    result_path: Path,
    smt2_path: Path,
    time_limit_s: float,
    add_per_iteration: int,
    max_iterations: int,
    target: str,
    seed_partition_path: Path | None,
) -> dict:
    if target == "pair-cover":
        universe = pair_state_universe()
        supported = supported_pair_states
        add_obstruction = add_pair_state_obstruction
        target_description = (
            "Four disjoint pairs assignable to the four agents so that "
            "each owner values its pair at least as much as its favorite."
        )
    elif target == "balanced-favorite-dominated":
        universe = balanced_state_universe()
        supported = supported_balanced_states
        add_obstruction = add_balanced_state_obstruction
        target_description = (
            "A balanced partition whose deletion remainders are bounded "
            "by every observer's favorite and whose bundles can be assigned "
            "so every owner receives favorite value."
        )
    elif target == "favorite-pair-balanced-efx":
        universe = favorite_pair_balanced_universe()
        supported = supported_efx_states
        add_obstruction = None
        target_description = (
            "A balanced EFX-supporting partition in which the common "
            "favorite belongs to a two-good bundle."
        )
    elif target == "favorite-triple-balanced-efx":
        universe = favorite_triple_balanced_universe()
        supported = supported_favorite_triple_states
        add_obstruction = add_favorite_triple_state_obstruction
        target_description = (
            "A balanced EFX-supporting partition in which the common "
            "favorite belongs to the three-good bundle, encoded by the "
            "exact three-pair Hall criterion."
        )
    elif target == "favorite-pair-balanced-floor":
        universe = favorite_pair_balanced_universe()
        supported = supported_floor_states
        add_obstruction = add_floor_state_obstruction
        target_description = (
            "A balanced partition with the common favorite in a pair, "
            "assignable so every owner receives at least favorite value."
        )
    elif target == "favorite-pair-balanced-floor-hall":
        universe = favorite_pair_balanced_universe()
        supported = supported_floor_states
        add_obstruction = add_floor_state_hall_obstruction
        target_description = (
            "Hall-selector replay of the balanced favorite-pair owner-floor "
            "target."
        )
    else:
        raise ValueError("unknown target")
    master = ParkabilityLRAMaster(N, M)
    if target == "favorite-pair-balanced-efx":
        add_obstruction = (
            lambda _master, state: master.add_partition_obstruction(state)
        )
    add_branch_constraints(master)
    pool: set[PairState] = set()
    if seed_partition_path is not None:
        source = json.loads(seed_partition_path.read_text())
        for raw_state in source.get("partitions", []):
            state = tuple(tuple(bundle) for bundle in raw_state)
            if state not in universe:
                raise ValueError("seed partition lies outside the target universe")
            if state not in pool:
                add_obstruction(master, state)
                pool.add(state)
    trace = []
    status = "ITERATION_LIMIT"
    reason_unknown = None
    solver_status = None
    result_values = None
    started = time.time()

    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit_s)
        solver_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        audit_branch(values)
        survivors = tuple(
            state
            for state in supported(values, universe)
            if state not in pool
        )
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(pool),
            "supported_state_count": len(survivors),
            "values": [list(row) for row in values],
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"supported_states={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "ZERO_TARGET_STATE"
            result_values = values
            break
        for state in survivors[:add_per_iteration]:
            add_obstruction(master, state)
            pool.add(state)

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solver_status,
        "reason_unknown": reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "favorite": FAVORITE,
        "fixed_half_favorite_representatives": list(REPRESENTATIVES),
        "universal_owner_threshold_failure": True,
        "target_kind": target,
        "target": target_description,
        "target_state_count": len(universe),
        "pool_size": len(pool),
        "seed_partition_path": (
            str(seed_partition_path.resolve())
            if seed_partition_path is not None
            else None
        ),
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE would prove, subject to independent replay, "
            "the selected sufficient cover in the four-distinct-"
            "representatives branch. ZERO_TARGET_STATE would refute only "
            "that proposed normal form, not EFX existence."
        ),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--add", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=50)
    parser.add_argument("--seed-partitions", type=Path)
    parser.add_argument(
        "--target",
        choices=(
            "pair-cover",
            "balanced-favorite-dominated",
            "favorite-pair-balanced-efx",
            "favorite-triple-balanced-efx",
            "favorite-pair-balanced-floor",
            "favorite-pair-balanced-floor-hall",
        ),
        default="pair-cover",
    )
    args = parser.parse_args()
    if args.time_limit < 0 or args.add < 1 or args.max_iterations < 1:
        parser.error("invalid search limits")
    result = run(
        result_path=args.result,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        target=args.target,
        seed_partition_path=args.seed_partitions,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
