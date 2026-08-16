#!/usr/bin/env python3
"""CEGAR for a small-step Hall-size-four row-merge radius cell."""

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
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        radius_partitions,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        radius_partitions,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-q4-small-step-radius-cegar-v1"
N = 4


def run(
    result_path,
    formula_path,
    d_size,
    radius,
    max_rounds,
    add_per_round,
    per_check_limit,
    warm_source=None,
):
    if result_path.exists() or formula_path.exists():
        raise ValueError("result and formula outputs must be new")
    if d_size < 1 or radius < 0 or max_rounds < 1 or add_per_round < 1:
        raise ValueError("positive sizes, rounds, and additions are required")
    sizes = (2, 1, 2, d_size)
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    small_step_goods = tuple(good for bundle in original[2:] for good in bundle)
    universe = tuple(sorted(radius_partitions(original, radius)))
    universe_set = set(universe)

    master = ParkabilityLRAMaster(N, m)
    solver = master.solver
    wall_rows = master.values
    epsilon = z3.Real("wall_epsilon")
    solver.add(epsilon > 0)
    perturb_good = w[0]
    post_row = tuple(
        value + epsilon if good == perturb_good else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])

    solver.add(zsum(wall_rows[0], u) == zsum(wall_rows[0], w))
    solver.add(wall_rows[0][critical_good] < wall_rows[0][w[0]])
    for target_index, target in enumerate(original):
        if target_index == 0:
            continue
        for removed in target:
            remainder = tuple(good for good in target if good != removed)
            if target_index == 1 and removed == critical_good:
                continue
            solver.add(zsum(wall_rows[0], u) > zsum(wall_rows[0], remainder))
    solver.add(
        *(epsilon < wall_rows[0][good] for good in small_step_goods)
    )

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    deficient_bundles = tuple(range(1, N))
    for agent in range(N):
        solver.add(z3.Not(post_edges[agent][0]))
    for size in range(1, N):
        for agents in itertools.combinations(range(N), size):
            solver.add(
                has_matching_expression(post_edges, agents, deficient_bundles)
            )

    active = []
    active_set = set()

    def add_partition(partition):
        if partition in active_set:
            return
        index = len(active)
        edges = edge_matrix(solver, post_rows, partition, f"radius_cut_{index}")
        solver.add(z3.Not(has_matching_expression(edges)))
        active.append(partition)
        active_set.add(partition)

    base_initial = pair_pivots(
        original,
        w,
        critical_good,
        complete_bundle_menu=True,
    )
    initial = list(base_initial)
    warm_source_sha256 = None
    if warm_source is not None:
        warm = json.loads(warm_source.read_text())
        if (
            warm.get("schema") != SCHEMA
            or warm.get("m") != m
            or warm.get("radius") != radius
            or warm.get("wall_partition")
            != [list(bundle) for bundle in original]
        ):
            raise ValueError("warm source describes a different radius cell")
        warm_source_sha256 = hashlib.sha256(warm_source.read_bytes()).hexdigest()
        for record in warm["rounds"]:
            for partition in record.get("learned_partitions", ()):
                candidate = tuple(tuple(bundle) for bundle in partition)
                if candidate not in initial:
                    initial.append(candidate)
    if any(partition not in universe_set for partition in initial):
        raise AssertionError("an initial bundle pivot lies outside the radius")
    for partition in initial:
        add_partition(partition)

    started = time.time()
    rounds = []
    terminal_values = None
    status = z3.unknown
    for round_index in range(max_rounds):
        cuts_before = len(active)
        solver.set(timeout=int(per_check_limit * 1000))
        check_started = time.time()
        status = solver.check()
        check_elapsed = time.time() - check_started
        record = {
            "round": round_index,
            "cuts_before_solve": cuts_before,
            "solver_status": str(status),
            "solver_wall_seconds": check_elapsed,
        }
        if status != z3.sat:
            record["reason_unknown"] = (
                solver.reason_unknown() if status == z3.unknown else None
            )
            rounds.append(record)
            break

        model = solver.model()
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        post_fractions = tuple(as_fraction(model, value) for value in post_row)
        wall_values, post_values_row = primitive_rows(
            wall_fractions, post_fractions
        )
        post_values = (post_values_row, *wall_values[1:])
        supports = []
        for partition in universe:
            count = matching_count(literal_graph(post_values, partition))
            if count:
                supports.append((partition, count))
        new_supports = [
            (partition, count)
            for partition, count in supports
            if partition not in active_set
        ]
        record.update(
            {
                "wall_values": [list(row) for row in wall_values],
                "post_wall_values": [list(row) for row in post_values],
                "radius_support_count": len(supports),
                "new_radius_support_count": len(new_supports),
                "new_radius_supporting_allocation_count": sum(
                    count for _partition, count in new_supports
                ),
            }
        )
        if not new_supports:
            terminal_values = (wall_values, post_values)
            rounds.append(record)
            break
        learned = new_supports[:add_per_round]
        for partition, _count in learned:
            add_partition(partition)
        record["learned_partition_count"] = len(learned)
        record["cuts_after_learning"] = len(active)
        record["learned_partitions"] = [
            [list(bundle) for bundle in partition]
            for partition, _count in learned
        ]
        rounds.append(record)
    else:
        status = z3.unknown

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    if status == z3.unsat:
        final_status = "RADIUS_CELL_VERIFIED"
    elif terminal_values is not None:
        final_status = "RADIUS_PIVOT_REFUTATION_FOUND"
    else:
        final_status = "CEGAR_INCOMPLETE"
    result = {
        "schema": SCHEMA,
        "status": final_status,
        "solver_status": str(status),
        "domain": "strictly positive additive real valuations",
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "bundle_sizes_excluding_critical_good": list(sizes),
        "minimal_hall_witness_size": 4,
        "radius": radius,
        "radius_partition_count": len(universe),
        "small_step_goods": list(small_step_goods),
        "base_initial_cut_count": len(base_initial),
        "initial_cut_count": len(initial),
        "warm_source": str(warm_source) if warm_source is not None else None,
        "warm_source_sha256": warm_source_sha256,
        "final_cut_count": len(active),
        "round_count": len(rounds),
        "rounds": rounds,
        "terminal_wall_values": (
            [list(row) for row in terminal_values[0]]
            if terminal_values is not None
            else None
        ),
        "terminal_post_wall_values": (
            [list(row) for row in terminal_values[1]]
            if terminal_values is not None
            else None
        ),
        "elapsed_seconds": time.time() - started,
        "max_rounds": max_rounds,
        "add_per_round": add_per_round,
        "per_check_time_limit_seconds": per_check_limit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT closes only this exact small-step Hall-size-four radius cell. "
            "SAT refutes only the radius bound, not complete EFX existence."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--d-size", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--add-per-round", type=int, default=64)
    parser.add_argument("--per-check-limit", type=float, default=300)
    parser.add_argument("--warm-source", type=Path)
    args = parser.parse_args()
    if args.per_check_limit <= 0:
        parser.error("--per-check-limit must be positive")
    run(
        args.result,
        args.formula,
        args.d_size,
        args.radius,
        args.max_rounds,
        args.add_per_round,
        args.per_check_limit,
        args.warm_source,
    )


if __name__ == "__main__":
    main()
