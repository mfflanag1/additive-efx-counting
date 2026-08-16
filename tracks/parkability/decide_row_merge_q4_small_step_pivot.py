#!/usr/bin/env python3
"""Decide a pair-complete pivot lemma for a small Hall-size-four wall step."""

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
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        canonical_partition,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        canonical_partition,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-q4-small-step-pair-pivot-lra-v1"
N = 4


def pair_pivots(original, w, critical_good, complete_bundle_menu=False):
    u = original[0]
    if len(u) != 2 or len(w) != 1 or len(original[2]) != 2:
        raise ValueError("the pair-pivot menu requires |U|=2, |W|=1, |C|=2")
    left, right = u
    remainder = w[0]
    v = original[1]
    pivots = [
        canonical_partition(((*u, critical_good), w, original[2], original[3])),
        canonical_partition(
            ((left, remainder), (right, critical_good), original[2], original[3])
        ),
        canonical_partition(
            ((left, critical_good), (right, remainder), original[2], original[3])
        ),
    ]
    for pair_index in (2, 3):
        pair = original[pair_index]
        if len(pair) < 2 or (len(pair) != 2 and not complete_bundle_menu):
            continue
        other = original[5 - pair_index]
        pivots.extend(
            canonical_partition(((*u, good), v, tuple(g for g in pair if g != good), other))
            for good in pair
        )
        for mask in range(1, (1 << len(pair)) - 1):
            left_part = tuple(
                good for index, good in enumerate(pair) if mask & (1 << index)
            )
            right_part = tuple(good for good in pair if good not in left_part)
            pivots.append(
                canonical_partition(
                    ((left, *left_part), (right, *right_part), v, other)
                )
            )
    if len(set(pivots)) != len(pivots):
        raise AssertionError("the pivot menu contains duplicate partitions")
    return tuple(pivots)


def run(
    result_path,
    formula_path,
    d_size,
    time_limit,
    complete_bundle_menu=False,
):
    if result_path.exists() or formula_path.exists():
        raise ValueError("result and formula outputs must be new")
    if d_size < 1:
        raise ValueError("the fourth bundle must be nonempty")
    sizes = (2, 1, 2, d_size)
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    small_step_goods = tuple(good for bundle in original[2:] for good in bundle)
    pivots = pair_pivots(
        original,
        w,
        critical_good,
        complete_bundle_menu=complete_bundle_menu,
    )

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
    solver.add(*(epsilon < wall_rows[0][good] for good in small_step_goods))

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

    for index, partition in enumerate(pivots):
        edges = edge_matrix(solver, post_rows, partition, f"pivot_{index}")
        solver.add(z3.Not(has_matching_expression(edges)))

    solver.set(timeout=int(time_limit * 1000))
    started = time.time()
    status = solver.check()
    elapsed = time.time() - started
    wall_values = None
    post_values = None
    pivot_matching_counts = None
    if status == z3.sat:
        model = solver.model()
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        post_fractions = tuple(as_fraction(model, value) for value in post_row)
        wall_values, post_values_row = primitive_rows(
            wall_fractions, post_fractions
        )
        post_values = (post_values_row, *wall_values[1:])
        pivot_matching_counts = [
            matching_count(literal_graph(post_values, partition))
            for partition in pivots
        ]
        if any(pivot_matching_counts):
            raise AssertionError("a blocked pivot has a literal perfect matching")

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": (
            "row-merge-q4-small-step-bundle-pivot-lra-v1"
            if complete_bundle_menu
            else SCHEMA
        ),
        "status": (
            (
                "BUNDLE_PIVOT_LEMMA_VERIFIED"
                if complete_bundle_menu
                else "PAIR_PIVOT_LEMMA_VERIFIED"
            )
            if status == z3.unsat
            else (
                "BUNDLE_PIVOT_LEMMA_REFUTED"
                if complete_bundle_menu
                else "PAIR_PIVOT_LEMMA_REFUTED"
            )
            if status == z3.sat
            else "MASTER_UNKNOWN"
        ),
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "domain": "strictly positive additive real valuations",
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "bundle_sizes_excluding_critical_good": list(sizes),
        "minimal_hall_witness_size": 4,
        "critical_equality": {"left": list(u), "right": list(w)},
        "critical_good": critical_good,
        "perturbed_good": perturb_good,
        "small_step_goods": list(small_step_goods),
        "small_step_condition": (
            "0 < wall_epsilon < min("
            + ", ".join(f"value_0_{good}" for good in small_step_goods)
            + ")"
        ),
        "pivot_count": len(pivots),
        "menu_scope": (
            "all nontrivial splits of each noncritical nonsingleton bundle"
            if complete_bundle_menu
            else "pair transfers and cross-pairings"
        ),
        "pivots": [[list(bundle) for bundle in partition] for partition in pivots],
        "wall_values": (
            [list(row) for row in wall_values] if wall_values else None
        ),
        "post_wall_values": (
            [list(row) for row in post_values] if post_values else None
        ),
        "pivot_matching_counts": pivot_matching_counts,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT proves that at least one of the displayed pair pivots "
            "supports complete EFX in this exact wall cell. The fourth bundle "
            "size is fixed by this formula; compression is a separate argument."
            if status == z3.unsat
            else "SAT refutes the pair-pivot lemma in this exact wall cell."
            if status == z3.sat
            else "The exact-real master reached its resource boundary."
        ),
        "claim_boundary": (
            "This is a local row-merge wall lemma, not a proof of row-merge "
            "continuation or general complete EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--d-size", type=int, default=2)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--complete-bundle-menu", action="store_true")
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("--time-limit must be positive")
    run(
        args.result,
        args.formula,
        args.d_size,
        args.time_limit,
        args.complete_bundle_menu,
    )


if __name__ == "__main__":
    main()
