#!/usr/bin/env python3
"""Minimize singleton repairs in the bounded rank-one bridge cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

import ortools
from ortools.sat.python import cp_model

try:
    from . import core
    from .anneal import atomic_json
    from .audit_common_favorite_rank1_bridge_checkpoint import (
        BRIDGE_ORBIT,
        OUTSIDE_REPAIR_ORBIT,
    )
    from .audit_common_favorite_rank1_radius2_orbits import (
        contested_family,
        orbit_signature,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        resident_graph,
    )
    from .decide_common_favorite_rank1_triple_conversion_cpsat import (
        add_cell_symmetry,
        add_rank_one_premise,
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
    from anneal import atomic_json
    from audit_common_favorite_rank1_bridge_checkpoint import (
        BRIDGE_ORBIT,
        OUTSIDE_REPAIR_ORBIT,
    )
    from audit_common_favorite_rank1_radius2_orbits import (
        contested_family,
        orbit_signature,
    )
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        resident_graph,
    )
    from decide_common_favorite_rank1_triple_conversion_cpsat import (
        add_cell_symmetry,
        add_rank_one_premise,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
    from integer_partition_master import IntegerPartitionMaster


SCHEMA = "common-favorite-rank1-bridge-singleton-optimization-cpsat-v1"
SECOND_OUTSIDE_REPAIR_ORBIT = "partnerB_tripleACC_pairsAA_BB"


def canonical_partition(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def singleton_partitions():
    return tuple(
        canonical_partition(((FAVORITE,),) + residual)
        for residual in residual_partitions()
    )


def repair_partitions(repair_family):
    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested = contested_family(neighborhood)
    bridge = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition) == BRIDGE_ORBIT
    )
    union = tuple(sorted(set(contested) | set(bridge)))
    if len(contested) != 21 or len(bridge) != 9 or len(union) != 30:
        raise AssertionError("bridge-family census changed")
    if repair_family == "bridge30":
        return union
    outside = tuple(
        partition
        for partition in neighborhood
        if orbit_signature(partition)
        in {OUTSIDE_REPAIR_ORBIT, SECOND_OUTSIDE_REPAIR_ORBIT}
    )
    extended = tuple(sorted(set(union) | set(outside)))
    if len(outside) != 15 or len(extended) != 45:
        raise AssertionError("extended bridge-family census changed")
    return extended


def supporting_singletons(values, universe):
    return tuple(
        partition
        for partition in universe
        if matching_rank(feasible_graph(values, partition)) == N
    )


def in_rank_one_cell(values):
    return (
        all(row[FAVORITE] > max(row[1:]) for row in values)
        and threshold_passes(values, OWNER, RESIDUAL)
        and resident_graph(values) == ((True, False, False),) * 3
    )


def in_cell(values, blocked):
    return in_rank_one_cell(values) and not any(
        matching_rank(feasible_graph(values, partition)) == N
        for partition in blocked
    )


def cell_symmetric(values):
    if any(values[left] < values[left + 1] for left in range(1, N - 1)):
        return False
    return all(
        all(
            tuple(values[observer][left] for observer in range(N))
            >= tuple(values[observer][right] for observer in range(N))
            for left, right in zip(group, group[1:])
        )
        for group in RESIDUAL
    )


def canonicalize_cell(values):
    candidates = []
    for residents in itertools.permutations(range(1, N)):
        row_order = (OWNER,) + residents
        for first in itertools.permutations(RESIDUAL[0]):
            for second in itertools.permutations(RESIDUAL[1]):
                for third in itertools.permutations(RESIDUAL[2]):
                    good_order = (FAVORITE,) + first + second + third
                    transformed = tuple(
                        tuple(values[row][good] for good in good_order)
                        for row in row_order
                    )
                    if cell_symmetric(transformed):
                        candidates.append(transformed)
    if not candidates:
        raise AssertionError("cell orbit has no symmetry representative")
    return max(candidates)


def seed_models(
    seed_paths,
    upper,
    blocked,
    use_cell_symmetry,
    resident_equality_pair,
):
    records = []
    pool_models = []
    hint_models = []
    for path in seed_paths:
        raw = json.loads(path.read_text())
        candidates = []
        if raw.get("values") is not None:
            candidates.append(raw["values"])
        if raw.get("best_values") is not None:
            candidates.append(raw["best_values"])
        candidates.extend(
            record["values"]
            for record in raw.get("cegar_trace", [])
            if record.get("values") is not None
        )
        pool_accepted = 0
        hint_accepted = 0
        for candidate in candidates:
            values = core.validate_values(
                candidate,
                expected_n=N,
                expected_m=M,
                lower=1,
                upper=upper,
            )
            if not in_rank_one_cell(values):
                continue
            if use_cell_symmetry:
                values = canonicalize_cell(values)
            pool_models.append(values)
            pool_accepted += 1
            if in_cell(values, blocked) and (
                resident_equality_pair is None
                or values[int(resident_equality_pair[0])]
                == values[int(resident_equality_pair[1])]
            ):
                hint_models.append(values)
                hint_accepted += 1
        records.append({
            "source": str(path),
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "candidate_model_count": len(candidates),
            "pool_model_count": pool_accepted,
            "feasible_hint_model_count": hint_accepted,
        })
    return tuple(pool_models), tuple(hint_models), records


def build_master(upper, use_cell_symmetry, blocked, resident_equality_pair):
    master = IntegerPartitionMaster(N, M, upper)
    if use_cell_symmetry:
        add_cell_symmetry(master)
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
    if resident_equality_pair is not None:
        first = int(resident_equality_pair[0])
        second = int(resident_equality_pair[1])
        for good in range(M):
            master.model.Add(
                master.values[first][good] == master.values[second][good]
            )
    for partition in blocked:
        master.add_partition_obstruction(partition)
    return master


def solve(master, time_limit, workers, random_seed):
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status = solver.Solve(master.model)
    raw_status = solver.StatusName(status)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = tuple(
            tuple(solver.Value(value) for value in row)
            for row in master.values
        )
    else:
        values = None
    return solver, raw_status, values


def run(
    upper,
    repair_family,
    use_cell_symmetry,
    add_per_iteration,
    max_iterations,
    time_limit,
    workers,
    random_seed,
    resident_equality_pair,
    seed_paths,
    result_path,
    proto_path,
):
    if (
        upper < 1
        or repair_family not in {"bridge30", "bridge45"}
        or add_per_iteration < 1
        or max_iterations < 1
        or time_limit <= 0
        or workers < 1
        or resident_equality_pair not in {None, "12", "23"}
        or result_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("valid bounds and new output paths are required")
    universe = singleton_partitions()
    blocked = repair_partitions(repair_family)
    pool_seeds, hint_seeds, seed_records = seed_models(
        seed_paths,
        upper,
        blocked,
        use_cell_symmetry,
        resident_equality_pair,
    )
    if not pool_seeds:
        raise ValueError("at least one rank-one pool seed model is required")

    pool = []
    pool_set = set()
    for values in pool_seeds:
        for partition in supporting_singletons(values, universe):
            if partition not in pool_set:
                pool.append(partition)
                pool_set.add(partition)
    if not pool:
        raise AssertionError("seed unexpectedly refutes the bridge lemma")

    master = build_master(
        upper,
        use_cell_symmetry,
        blocked,
        resident_equality_pair,
    )
    activations = []

    def add_to_pool(partition):
        activation = master.model.NewBoolVar(
            f"singleton_obstructed_{len(activations)}"
        )
        if not master.add_partition_obstruction(
            partition,
            activation=activation,
        ):
            raise AssertionError("pooled singleton partition was duplicated")
        activations.append(activation)

    for partition in pool:
        add_to_pool(partition)

    hint = (
        min(
            hint_seeds,
            key=lambda values: len(supporting_singletons(values, universe)),
        )
        if hint_seeds
        else None
    )
    if hint is not None:
        for row_variables, row_values in zip(master.values, hint):
            for variable, value in zip(row_variables, row_values):
                master.model.AddHint(variable, value)
        for activation, partition in zip(activations, pool):
            master.model.AddHint(
                activation,
                int(matching_rank(feasible_graph(hint, partition)) != N),
            )

    started = time.time()
    trace = []
    best_values = hint
    best_support = supporting_singletons(hint, universe) if hint is not None else None
    exact_minimum = None
    terminal_status = "ITERATION_LIMIT"
    last_solver = None
    last_raw_status = None

    for iteration in range(1, max_iterations + 1):
        master.model.Maximize(sum(activations))
        solver, raw_status, values = solve(
            master,
            time_limit,
            workers,
            random_seed + iteration - 1,
        )
        last_solver = solver
        last_raw_status = raw_status
        record = {
            "iteration": iteration,
            "pool_size_before": len(pool),
            "solver_status": raw_status,
            "solver_wall_seconds": solver.WallTime(),
            "conflicts": solver.NumConflicts(),
            "branches": solver.NumBranches(),
        }
        if values is None:
            trace.append(record)
            print(json.dumps({"progress": record}), flush=True)
            terminal_status = "MASTER_UNKNOWN" if raw_status == "UNKNOWN" else raw_status
            break
        if not in_cell(values, blocked) or (
            resident_equality_pair is not None
            and values[int(resident_equality_pair[0])]
            != values[int(resident_equality_pair[1])]
        ):
            raise AssertionError("decoded optimization model left the decision cell")
        support = supporting_singletons(values, universe)
        support_set = set(support)
        pooled_support_count = sum(partition in support_set for partition in pool)
        outside = tuple(partition for partition in support if partition not in pool_set)
        objective = int(round(solver.ObjectiveValue()))
        best_bound = solver.BestObjectiveBound()
        if raw_status == "OPTIMAL" and len(pool) - objective != pooled_support_count:
            raise AssertionError("optimal activation objective failed exact replay")
        if best_support is None or len(support) < len(best_support):
            best_values = values
            best_support = support
        record.update({
            "objective_obstructed_pool_count": objective,
            "best_objective_bound": best_bound,
            "pooled_singleton_support_count": pooled_support_count,
            "all_singleton_support_count": len(support),
            "supported_outside_pool_count": len(outside),
            "values": [list(row) for row in values],
        })
        if not outside:
            trace.append(record)
            print(json.dumps({"progress": record}), flush=True)
            if raw_status == "OPTIMAL":
                exact_minimum = len(support)
                terminal_status = "OPTIMAL_FIXED_POINT"
            else:
                terminal_status = "FEASIBLE_FIXED_POINT"
            break
        added = outside[:add_per_iteration]
        for partition in added:
            pool.append(partition)
            pool_set.add(partition)
            add_to_pool(partition)
        record["new_singleton_partition_count"] = len(added)
        trace.append(record)
        print(json.dumps({"progress": record}), flush=True)
    if last_solver is None or last_raw_status is None:
        raise AssertionError("CP-SAT performed no solve")

    elapsed = time.time() - started
    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_path.read_bytes()
    if exact_minimum == 0:
        status = (
            "BOUNDED_RANK1_BRIDGE_LEMMA_REFUTED"
            if repair_family == "bridge30"
            else "BOUNDED_RANK1_EXTENDED_BRIDGE_LEMMA_REFUTED"
        )
    elif exact_minimum is not None:
        status = (
            "BOUNDED_RANK1_BRIDGE_SINGLETON_FLOOR_CERTIFIED"
            if repair_family == "bridge30"
            else "BOUNDED_RANK1_EXTENDED_BRIDGE_SINGLETON_FLOOR_CERTIFIED"
        )
    elif best_support is not None and (
        not hint_seeds
        or len(best_support)
        < min(
            len(supporting_singletons(values, universe))
            for values in hint_seeds
        )
    ):
        status = "IMPROVED_SINGLETON_UPPER_BOUND"
    else:
        status = "SEARCH_BOUNDARY"
    result = {
        "schema": SCHEMA,
        "status": status,
        "terminal_status": terminal_status,
        "n": N,
        "m": M,
        "domain": f"positive integers in [1,{upper}]",
        "upper": upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_partition": [list(bundle) for bundle in RESIDUAL],
        "resident_rank_one_common_bundle": list(RESIDUAL[0]),
        "repair_family": repair_family,
        "cell_symmetry": use_cell_symmetry,
        "resident_equality_pair": resident_equality_pair,
        "repair_partition_count": len(blocked),
        "bridge_union_partition_count": 30,
        "favorite_singleton_partition_count": len(universe),
        "initial_singleton_pool_size": len(
            set(
                partition
                for values in pool_seeds
                for partition in supporting_singletons(values, universe)
            )
        ),
        "terminal_singleton_pool_size": len(pool),
        "exact_minimum_singleton_support_count": exact_minimum,
        "best_singleton_support_count": (
            len(best_support) if best_support is not None else None
        ),
        "best_values": (
            [list(row) for row in best_values]
            if best_values is not None
            else None
        ),
        "seed_imports": seed_records,
        "cegar_trace": trace,
        "time_limit_seconds_per_iteration": time_limit,
        "max_iterations": max_iterations,
        "add_per_iteration": add_per_iteration,
        "workers": workers,
        "random_seed": random_seed,
        "elapsed_seconds": elapsed,
        "final_solver_status": last_raw_status,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "A zero witness refutes only the selected local repair-family lemma. "
            "A positive optimum certifies only this bounded integer cell. "
            "Neither outcome resolves complete additive EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=6)
    parser.add_argument(
        "--repair-family",
        choices=("bridge30", "bridge45"),
        default="bridge30",
    )
    parser.add_argument("--cell-symmetry", action="store_true")
    parser.add_argument("--add-per-iteration", type=int, default=128)
    parser.add_argument("--max-iterations", type=int, default=8)
    parser.add_argument("--time-limit", type=float, default=60)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--resident-equality-pair", choices=("12", "23"))
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.upper,
        args.repair_family,
        args.cell_symmetry,
        args.add_per_iteration,
        args.max_iterations,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.resident_equality_pair,
        args.seed,
        args.result,
        args.proto,
    )


if __name__ == "__main__":
    main()
