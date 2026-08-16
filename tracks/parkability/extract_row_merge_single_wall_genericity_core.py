#!/usr/bin/env python3
"""Extract the subset-order assumptions used by a single-wall pivot core."""

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
        disjoint_subset_pairs,
        edge_matrix,
        has_matching_expression,
        make_bundles,
        primitive_rows,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        disjoint_subset_pairs,
        edge_matrix,
        has_matching_expression,
        make_bundles,
        primitive_rows,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-single-wall-genericity-core-v1"
N = 4


def model_values(model, wall_rows, post_row):
    wall_fractions = tuple(
        tuple(as_fraction(model, value) for value in row) for row in wall_rows
    )
    post_fractions = tuple(as_fraction(model, value) for value in post_row)
    wall_values, post_values = primitive_rows(wall_fractions, post_fractions)
    return [list(row) for row in wall_values], list(post_values)


def run(source_path, output_path, core_formula_path, time_limit, check_limit):
    if output_path.exists():
        raise ValueError("output must be new")
    source = json.loads(source_path.read_text())
    if source.get("schema") != "row-merge-single-wall-candidate-core-v1":
        raise ValueError("unexpected source schema")
    sizes = tuple(source["bundle_sizes_excluding_critical_good"])
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    candidates = tuple(
        tuple(tuple(bundle) for bundle in record["partition"])
        for record in source["retained_core"]
    )

    master = ParkabilityLRAMaster(N, m)
    solver = master.solver
    solver.set(unsat_core=True)
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

    critical_pair = tuple(sorted((u, w)))
    generic_records = []
    generic_constraints = []
    generic_implications = []
    selectors = []
    for index, (left, right) in enumerate(disjoint_subset_pairs(m)):
        if tuple(sorted((left, right))) == critical_pair:
            continue
        wall_left = zsum(wall_rows[0], left)
        wall_right = zsum(wall_rows[0], right)
        post_left = zsum(post_row, left)
        post_right = zsum(post_row, right)
        selector = z3.Bool(f"generic_pair_{index}")
        constraint = z3.And(
            wall_left != wall_right,
            z3.Or(
                z3.And(wall_left > wall_right, post_left > post_right),
                z3.And(wall_left < wall_right, post_left < post_right),
            ),
        )
        implication = z3.Implies(selector, constraint)
        solver.add(implication)
        selectors.append(selector)
        generic_constraints.append(constraint)
        generic_implications.append(implication)
        generic_records.append(
            {
                "selector": str(selector),
                "left": list(left),
                "right": list(right),
                "perturb_good_side": (
                    "left"
                    if perturb_good in left
                    else "right"
                    if perturb_good in right
                    else "neither"
                ),
            }
        )

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))

    deficient_agents = tuple(range(N))
    deficient_bundles = tuple(range(1, N))
    for agent in deficient_agents:
        for bundle in range(N):
            if bundle not in deficient_bundles:
                solver.add(z3.Not(post_edges[agent][bundle]))
    for size in range(1, N):
        for agents in itertools.combinations(deficient_agents, size):
            solver.add(
                has_matching_expression(post_edges, agents, deficient_bundles)
            )

    for index, partition in enumerate(candidates):
        edges = edge_matrix(solver, post_rows, partition, f"core_candidate_{index}")
        solver.add(z3.Not(has_matching_expression(edges)))

    solver.set(timeout=int(check_limit * 1000))
    relaxed_status = solver.check()
    if relaxed_status != z3.sat:
        raise AssertionError(f"relaxed core is not SAT: {relaxed_status}")
    relaxed_wall, relaxed_post = model_values(
        solver.model(), wall_rows, post_row
    )

    solver.set(timeout=int(check_limit * 1000))
    started = time.time()
    full_status = solver.check(*selectors)
    if full_status != z3.unsat:
        raise AssertionError(f"full genericity family is not UNSAT: {full_status}")
    name_to_index = {str(selector): index for index, selector in enumerate(selectors)}
    initial = sorted(name_to_index[str(item)] for item in solver.unsat_core())
    active = list(initial)
    deletion_checks = []
    for index in tuple(initial):
        if time.time() - started >= time_limit:
            break
        trial = [candidate for candidate in active if candidate != index]
        remaining = max(1.0, min(check_limit, time_limit - (time.time() - started)))
        solver.set(timeout=int(remaining * 1000))
        status = solver.check(*(selectors[candidate] for candidate in trial))
        deletion_checks.append({"core_position": index, "status": str(status)})
        if status == z3.unsat:
            active = trial

    solver.set(timeout=int(check_limit * 1000))
    final_status = solver.check(*(selectors[index] for index in active))
    if final_status != z3.unsat:
        raise AssertionError(f"retained genericity core is not UNSAT: {final_status}")
    deletion_status = {
        record["core_position"]: record["status"] for record in deletion_checks
    }
    deletion_minimal = all(
        deletion_status.get(index) == "sat" for index in active
    )
    retained = [
        {
            "core_position": index,
            **generic_records[index],
        }
        for index in active
    ]
    record_to_index = {
        (tuple(record["left"]), tuple(record["right"])): index
        for index, record in enumerate(generic_records)
    }
    canonical_indices = [
        record_to_index[(tuple(sorted((*u, good))), tuple(w))]
        for good in original[2]
    ]
    solver.set(timeout=int(check_limit * 1000))
    canonical_status = solver.check(
        *(selectors[index] for index in canonical_indices)
    )
    if canonical_status != z3.unsat:
        raise AssertionError(
            f"the two comparison canonical core is not UNSAT: {canonical_status}"
        )
    canonical_deletions = []
    for omitted in canonical_indices:
        solver.set(timeout=int(check_limit * 1000))
        status = solver.check(
            *(
                selectors[index]
                for index in canonical_indices
                if index != omitted
            )
        )
        canonical_deletions.append(
            {"core_position": omitted, "status": str(status)}
        )
    if any(record["status"] != "sat" for record in canonical_deletions):
        raise AssertionError("the two comparison canonical core is not minimal")

    generic_implication_sexprs = {
        implication.sexpr() for implication in generic_implications
    }
    core_solver = z3.SolverFor("QF_LRA")
    core_solver.add(
        *(
            assertion
            for assertion in solver.assertions()
            if assertion.sexpr() not in generic_implication_sexprs
        ),
        *(generic_constraints[index] for index in canonical_indices),
    )
    core_formula = core_solver.to_smt2()
    if core_formula_path.exists():
        if core_formula_path.read_text() != core_formula:
            raise AssertionError("existing core formula disagrees with extraction")
    else:
        core_formula_path.parent.mkdir(parents=True, exist_ok=True)
        core_formula_path.write_text(core_formula)
    canonical_core = [
        {
            "core_position": index,
            **generic_records[index],
            "equivalent_small_step_bound": (
                f"wall_epsilon < value_0_{good}"
            ),
        }
        for index, good in zip(canonical_indices, original[2])
    ]
    result = {
        "schema": SCHEMA,
        "status": "GENERICITY_ASSUMPTION_CORE_EXTRACTED",
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "critical_equality": {"left": list(u), "right": list(w)},
        "perturbed_good": perturb_good,
        "candidate_partition_count": len(candidates),
        "genericity_pair_count": len(selectors),
        "relaxed_status": str(relaxed_status),
        "relaxed_wall_values": relaxed_wall,
        "relaxed_post_wall_moving_row": relaxed_post,
        "full_status": str(full_status),
        "initial_core_size": len(initial),
        "retained_core_size": len(active),
        "retained_core": retained,
        "deletion_checks": deletion_checks,
        "deletion_minimal": deletion_minimal,
        "final_status": str(final_status),
        "canonical_core_status": str(canonical_status),
        "canonical_core_size": len(canonical_indices),
        "canonical_core": canonical_core,
        "canonical_core_deletion_checks": canonical_deletions,
        "canonical_core_deletion_minimal": True,
        "small_step_condition": (
            "0 < wall_epsilon < min("
            + ", ".join(f"value_0_{good}" for good in original[2])
            + ")"
        ),
        "core_formula": str(core_formula_path),
        "core_formula_sha256": hashlib.sha256(core_formula.encode()).hexdigest(),
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds": time_limit,
        "per_check_time_limit_seconds": check_limit,
        "claim_boundary": (
            "The retained subset-order assumptions suffice for the fixed "
            "seven-partition, seven-good, Hall-size-four contradiction. This "
            "is proof-mining data, not a general wall-pivot or EFX theorem."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--core-formula", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--check-limit", type=float, default=120)
    args = parser.parse_args()
    if args.time_limit <= 0 or args.check_limit <= 0:
        parser.error("time limits must be positive")
    run(
        args.source,
        args.output,
        args.core_formula,
        args.time_limit,
        args.check_limit,
    )


if __name__ == "__main__":
    main()
