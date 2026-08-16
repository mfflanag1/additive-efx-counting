#!/usr/bin/env python3
"""Branch the open q=4 exchange-chain gate on explicit Hall witnesses."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        graph,
        matching_count,
        minimal_hall_witnesses,
    )
    from .core import validate_values
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_expression,
        make_bundles,
        primitive_rows,
    )
except ImportError:
    from analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        graph,
        matching_count,
        minimal_hall_witnesses,
    )
    from core import validate_values
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_expression,
        make_bundles,
        primitive_rows,
    )


SCHEMA = "row-merge-q4-chain-hall-witness-probe-v1"
N = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_hall_witness(solver, rows, candidate, agents):
    feasible = tuple(
        tuple(
            edge_expression(rows[agent], candidate, bundle)
            for bundle in range(N)
        )
        for agent in range(N)
    )
    neighborhood = tuple(
        z3.Or(*(feasible[agent][bundle] for agent in agents))
        for bundle in range(N)
    )
    for forbidden in itertools.combinations(neighborhood, len(agents)):
        solver.add(z3.Or(*(z3.Not(neighbor) for neighbor in forbidden)))


def decode_model(model, wall_rows, post_row):
    wall_fractions = tuple(
        tuple(as_fraction(model, value) for value in row) for row in wall_rows
    )
    post_fractions = tuple(as_fraction(model, value) for value in post_row)
    wall_values, post_values_row = primitive_rows(wall_fractions, post_fractions)
    return wall_values, (post_values_row, *wall_values[1:])


def support_records(values, menu):
    return tuple(
        {
            "partition": [list(bundle) for bundle in candidate],
            "matching_count": count,
        }
        for candidate in menu
        if (count := matching_count(graph(values, candidate)))
    )


def run(
    base_path: Path,
    target_source_path: Path,
    target_indices: tuple[int, ...],
    time_limit: float,
    output_path: Path,
) -> None:
    if output_path.exists() or time_limit <= 0:
        raise ValueError("new output and positive time limit are required")
    base_record = json.loads(base_path.read_text())
    formula_path = Path(base_record["formula"])
    if (
        base_record.get("schema") != "row-merge-q4-exchange-chain-cegar-v1"
        or base_record.get("initial_cut_count") != 32
        or base_record.get("final_cut_count") != 32
        or not formula_path.is_file()
        or sha256(formula_path) != base_record["formula_sha256"]
    ):
        raise AssertionError("base is not the frozen 32-cut formula")
    target_source = json.loads(target_source_path.read_text())
    if (
        target_source.get("schema") != "row-merge-q4-exchange-chain-cegar-v1"
        or target_source.get("m") != 9
        or target_source["rounds"][0].get("solver_status") != "sat"
    ):
        raise AssertionError("target source has no exact SAT model")

    original, w, _critical_good, m = make_bundles((2, 1, 2, 3))
    menu = exchange_chain_partitions(original, 3)
    target_values = validate_values(
        target_source["rounds"][0]["post_wall_values"],
        expected_n=N,
        expected_m=m,
        lower=1,
    )
    targets = tuple(
        candidate
        for candidate in menu
        if matching_count(graph(target_values, candidate))
    )
    if len(menu) != 515 or len(targets) != 9:
        raise AssertionError("the nine-repair target census changed")
    if (
        not target_indices
        or len(set(target_indices)) != len(target_indices)
        or any(index < 0 or index >= len(targets) for index in target_indices)
    ):
        raise ValueError("target indices must be distinct members of 0..8")

    assertions = z3.parse_smt2_file(str(formula_path))
    solver = z3.SolverFor("QF_LRA")
    solver.add(assertions)
    wall_rows = tuple(
        tuple(z3.Real(f"value_{agent}_{good}") for good in range(m))
        for agent in range(N)
    )
    epsilon = z3.Real("wall_epsilon")
    post_row = tuple(
        value + epsilon if good == w[0] else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])

    records = []
    for target_index in target_indices:
        candidate = targets[target_index]
        branches = []
        for size in range(2, N + 1):
            for agents in itertools.combinations(range(N), size):
                solver.push()
                add_hall_witness(solver, post_rows, candidate, agents)
                solver.set(timeout=round(time_limit * 1000))
                started = time.time()
                status = solver.check()
                elapsed = time.time() - started
                branch = {
                    "agents": list(agents),
                    "solver_status": str(status),
                    "solver_wall_seconds": elapsed,
                    "reason_unknown": (
                        solver.reason_unknown() if status == z3.unknown else None
                    ),
                }
                if status == z3.sat:
                    wall_values, post_values = decode_model(
                        solver.model(), wall_rows, post_row
                    )
                    candidate_graph = graph(post_values, candidate)
                    neighborhood = tuple(
                        bundle
                        for bundle in range(N)
                        if any(candidate_graph[agent][bundle] for agent in agents)
                    )
                    if (
                        len(neighborhood) >= len(agents)
                        or matching_count(candidate_graph)
                    ):
                        raise AssertionError("decoded model lost its Hall witness")
                    supports = support_records(post_values, menu)
                    branch.update(
                        {
                            "wall_values": [list(row) for row in wall_values],
                            "post_wall_values": [list(row) for row in post_values],
                            "witness_neighborhood": list(neighborhood),
                            "minimal_hall_witnesses": [
                                {
                                    "agents": list(witness_agents),
                                    "neighbors": list(witness_neighbors),
                                }
                                for witness_agents, witness_neighbors in minimal_hall_witnesses(
                                    candidate_graph
                                )
                            ],
                            "chain_support_count": len(supports),
                            "chain_supports": supports,
                        }
                    )
                branches.append(branch)
                solver.pop()
        statuses = [branch["solver_status"] for branch in branches]
        records.append(
            {
                "target_index": target_index,
                "partition": [list(bundle) for bundle in candidate],
                "target_model_matching_count": matching_count(
                    graph(target_values, candidate)
                ),
                "branch_count": len(branches),
                "sat_branch_count": statuses.count("sat"),
                "unsat_branch_count": statuses.count("unsat"),
                "unknown_branch_count": statuses.count("unknown"),
                "branches": branches,
            }
        )

    if all(record["unsat_branch_count"] == 11 for record in records):
        final_status = "TARGET_REPAIR_FORCED"
    elif any(record["sat_branch_count"] for record in records):
        final_status = "HALL_OBSTRUCTION_BRANCHES_SURVIVE"
    else:
        final_status = "HALL_WITNESS_PROBE_INCOMPLETE"
    result = {
        "schema": SCHEMA,
        "status": final_status,
        "domain": "strictly positive additive real valuations",
        "base": str(base_path),
        "base_sha256": sha256(base_path),
        "base_formula": str(formula_path),
        "base_formula_sha256": sha256(formula_path),
        "base_cut_count": 32,
        "target_source": str(target_source_path),
        "target_source_sha256": sha256(target_source_path),
        "chain_partition_count": len(menu),
        "target_model_support_count": len(targets),
        "target_indices": list(target_indices),
        "per_branch_time_limit_seconds": time_limit,
        "records": records,
        "interpretation": (
            "Each branch fixes the deficient agent subset witnessing failure "
            "of one remaining exchange-chain repair. SAT branches give exact "
            "successor models; UNSAT branches exclude that Hall witness."
        ),
        "claim_boundary": (
            "This is a fixed-graph, fixed-cut proof-mining probe. It does not "
            "decide the complete exchange-chain menu or general additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--target-source", type=Path, required=True)
    parser.add_argument("--target-index", type=int, action="append", required=True)
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.base,
        args.target_source,
        tuple(args.target_index),
        args.time_limit,
        args.output,
    )


if __name__ == "__main__":
    main()
