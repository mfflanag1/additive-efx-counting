#!/usr/bin/env python3
"""Extract a candidate-partition UNSAT core from a single-wall formula."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        canonical_partition,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        radius_partitions,
    )
except ImportError:
    from anneal import atomic_json
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        canonical_partition,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        radius_partitions,
    )


SCHEMA = "row-merge-single-wall-candidate-core-v1"
CANDIDATE = re.compile(r"candidate_(\d+)_a")


def split_assertions(formula_path):
    base = []
    definitions = {}
    obstructions = {}
    for assertion in z3.parse_smt2_file(str(formula_path)):
        indices = {int(value) for value in CANDIDATE.findall(assertion.sexpr())}
        if indices and assertion.decl().kind() == z3.Z3_OP_NOT:
            if len(indices) != 1:
                raise AssertionError("candidate obstruction mixes partition indices")
            index = indices.pop()
            if index in obstructions:
                raise AssertionError("duplicate candidate obstruction")
            obstructions[index] = assertion
        elif indices:
            if len(indices) != 1:
                raise AssertionError("candidate definition mixes partition indices")
            definitions.setdefault(indices.pop(), []).append(assertion)
        else:
            base.append(assertion)
    if (
        sorted(obstructions) != list(range(len(obstructions)))
        or set(definitions) != set(obstructions)
        or any(len(items) != 16 for items in definitions.values())
    ):
        raise AssertionError("candidate obstruction indices are not contiguous")
    return tuple(base), definitions, obstructions


def partition_distance(start, target):
    start_sets = tuple(set(bundle) for bundle in start)
    target_sets = tuple(set(bundle) for bundle in target)
    retained = max(
        sum(len(start_sets[index] & target_sets[order[index]]) for index in range(4))
        for order in itertools.permutations(range(4))
    )
    return sum(map(len, start)) - retained


def run(
    formula_path,
    result_path,
    core_formula_path,
    sizes,
    radius,
    time_limit,
    check_limit,
):
    if result_path.exists():
        raise ValueError("result output path already exists")
    if not formula_path.is_file():
        raise ValueError("formula path does not exist")
    base, definitions, obstructions = split_assertions(formula_path)
    original, w, _critical_good, m = make_bundles(sizes)
    candidates = tuple(sorted(radius_partitions(original, radius)))
    if len(candidates) != len(obstructions):
        raise AssertionError("reconstructed partition census disagrees with formula")

    solver = z3.SolverFor("QF_LRA")
    solver.set(unsat_core=True)
    solver.add(*base)
    solver.add(*(item for items in definitions.values() for item in items))
    selectors = {
        index: z3.Bool(f"core_candidate_{index}") for index in obstructions
    }
    for index, obstruction in obstructions.items():
        solver.add(z3.Implies(selectors[index], obstruction))

    solver.set(timeout=int(check_limit * 1000))
    base_status = solver.check()
    if base_status != z3.sat:
        raise AssertionError("formula without candidate obstructions is not SAT")

    started = time.time()
    full_status = solver.check(*(selectors[index] for index in sorted(selectors)))
    if full_status != z3.unsat:
        raise AssertionError(f"full candidate family did not replay UNSAT: {full_status}")
    name_to_index = {str(selector): index for index, selector in selectors.items()}
    initial_core = sorted(name_to_index[str(item)] for item in solver.unsat_core())
    active = list(initial_core)
    deletion_checks = []
    for index in tuple(initial_core):
        if time.time() - started >= time_limit:
            break
        trial = [candidate for candidate in active if candidate != index]
        remaining = max(1.0, min(check_limit, time_limit - (time.time() - started)))
        solver.set(timeout=int(remaining * 1000))
        status = solver.check(*(selectors[candidate] for candidate in trial))
        deletion_checks.append({"candidate_index": index, "status": str(status)})
        if status == z3.unsat:
            active = trial

    solver.set(timeout=int(check_limit * 1000))
    final_status = solver.check(*(selectors[index] for index in active))
    if final_status != z3.unsat:
        raise AssertionError("retained candidate core does not replay UNSAT")
    elapsed = time.time() - started
    status_by_index = {
        check["candidate_index"]: check["status"] for check in deletion_checks
    }
    deletion_minimal = all(status_by_index.get(index) == "sat" for index in active)
    core_solver = z3.SolverFor("QF_LRA")
    core_solver.add(*base)
    core_solver.add(
        *(item for index in active for item in definitions[index]),
        *(obstructions[index] for index in active),
    )
    core_formula = core_solver.to_smt2()
    if core_formula_path.exists():
        if core_formula_path.read_text() != core_formula:
            raise AssertionError("existing core formula disagrees with extraction")
    else:
        core_formula_path.parent.mkdir(parents=True, exist_ok=True)
        core_formula_path.write_text(core_formula)
    core_records = [
        {
            "candidate_index": index,
            "transfer_distance": partition_distance(
                canonical_partition(original), candidates[index]
            ),
            "partition": [list(bundle) for bundle in candidates[index]],
        }
        for index in active
    ]
    variables = tuple(
        tuple(z3.Real(f"value_{agent}_{good}") for good in range(m))
        for agent in range(4)
    )
    epsilon = z3.Real("wall_epsilon")
    perturb_good = w[0]
    deletion_boundaries = []
    for omitted in active:
        solver.set(timeout=int(check_limit * 1000))
        status = solver.check(
            *(selectors[index] for index in active if index != omitted)
        )
        if status != z3.sat:
            raise AssertionError("deletion-minimal core boundary did not replay SAT")
        model = solver.model()
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in variables
        )
        epsilon_fraction = as_fraction(model, epsilon)
        post_fraction = tuple(
            value + (epsilon_fraction if good == perturb_good else 0)
            for good, value in enumerate(wall_fractions[0])
        )
        wall_values, post_row = primitive_rows(wall_fractions, post_fraction)
        post_values = (post_row, *wall_values[1:])
        core_matching_counts = {
            index: matching_count(literal_graph(post_values, candidates[index]))
            for index in active
        }
        supported = [
            index for index, count in core_matching_counts.items() if count
        ]
        if supported != [omitted]:
            raise AssertionError("core deletion boundary support is not unique")
        deletion_boundaries.append(
            {
                "omitted_candidate_index": omitted,
                "wall_values": [list(row) for row in wall_values],
                "post_wall_values": [list(row) for row in post_values],
                "scaled_wall_epsilon": (
                    post_row[perturb_good] - wall_values[0][perturb_good]
                ),
                "supported_partition": [
                    list(bundle) for bundle in candidates[omitted]
                ],
                "supported_partition_feasibility_graph": [
                    list(row)
                    for row in literal_graph(post_values, candidates[omitted])
                ],
                "supported_partition_matching_count": core_matching_counts[omitted],
            }
        )
    result = {
        "schema": SCHEMA,
        "status": "CANDIDATE_CORE_EXTRACTED",
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula_path.read_bytes()).hexdigest(),
        "bundle_sizes_excluding_critical_good": list(sizes),
        "transfer_radius": radius,
        "candidate_partition_count": len(candidates),
        "base_assertion_count": len(base),
        "candidate_definition_count": sum(map(len, definitions.values())),
        "base_status": str(base_status),
        "full_status": str(full_status),
        "initial_unsat_core_size": len(initial_core),
        "retained_core_size": len(active),
        "retained_core": core_records,
        "deletion_boundary_count": len(deletion_boundaries),
        "deletion_boundaries": deletion_boundaries,
        "deletion_check_count": len(deletion_checks),
        "deletion_checks": deletion_checks,
        "deletion_minimal": deletion_minimal,
        "final_status": str(final_status),
        "core_formula": str(core_formula_path),
        "core_formula_sha256": hashlib.sha256(core_formula.encode()).hexdigest(),
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "per_check_time_limit_seconds": check_limit,
        "interpretation": (
            "The retained partitions suffice for the fixed seven-good "
            "Hall-size-four radius-two contradiction. This is proof-mining "
            "data, not a general EFX or pivot theorem."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--core-formula", type=Path, required=True)
    parser.add_argument("--bundle-sizes", default="2,1,2,1")
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--check-limit", type=float, default=60)
    args = parser.parse_args()
    sizes = tuple(int(value) for value in args.bundle_sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        parser.error("--bundle-sizes requires four positive integers")
    if args.radius < 0 or args.time_limit <= 0 or args.check_limit <= 0:
        parser.error("radius must be nonnegative and time limits positive")
    run(
        args.formula,
        args.result,
        args.core_formula,
        sizes,
        args.radius,
        args.time_limit,
        args.check_limit,
    )


if __name__ == "__main__":
    main()
