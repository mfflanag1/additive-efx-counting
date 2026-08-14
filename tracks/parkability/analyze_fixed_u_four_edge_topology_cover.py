#!/usr/bin/env python3
"""Find a minimum transfer-topology cover of exact adversarial profiles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)
from .analyze_fixed_u_no_go_response_relations import SUPPORT


def topology(allocation):
    initial = provenance_holder(SUPPORT)
    final = {
        good: owner for owner, goods in allocation.items() for good in goods
    }
    return tuple(sorted({
        (initial[good], final[good])
        for good in initial if initial[good] != final[good]
    }))


def charity_hamiltonian_paths():
    return {
        tuple(sorted((left, right) for left, right in zip(("charity", *order), order)))
        for order in itertools.permutations(("r", "q", "d", "s"))
    }


def functional_topology(graph):
    return len({source for source, _ in graph}) == len(graph)


def minimum_cover(profiles, allowed):
    ordered = sorted(allowed)
    choose = [z3.Bool(f"choose_cover_{index}") for index in range(len(ordered))]
    optimizer = z3.Optimize()
    for profile in profiles:
        indices = [
            index for index, graph in enumerate(ordered)
            if graph in profile["feasible_topologies"]
        ]
        optimizer.add(z3.Or(*(choose[index] for index in indices)) if indices
                      else z3.BoolVal(False))
    optimizer.minimize(z3.Sum(*(z3.If(variable, 1, 0) for variable in choose)))
    status = optimizer.check()
    selected = []
    if status == z3.sat:
        model = optimizer.model()
        selected = [graph for graph, variable in zip(ordered, choose)
                    if z3.is_true(model.eval(variable, model_completion=True))]
    return status, selected


def analyze(source: Path, maximum_iteration=None):
    script = Path(__file__).resolve()
    source_bytes = source.read_bytes()
    payload = json.loads(source_bytes)
    rounds = [
        record for record in payload["rounds"]
        if record.get("values")
        and (maximum_iteration is None or record["iteration"] <= maximum_iteration)
    ]
    allocation_menu = tuple(allocations_with_at_most_edges(4, SUPPORT))
    profiles = []
    all_topologies = set()
    for record in rounds:
        values = {
            owner: {good: Fraction(amount) for good, amount in row.items()}
            for owner, row in record["values"].items()
        }
        feasible = set()
        witness_count = 0
        for allocation in allocation_menu:
            if complete_efx(values, allocation):
                feasible.add(topology(allocation))
                witness_count += 1
        all_topologies.update(feasible)
        profiles.append({
            "iteration": record["iteration"],
            "feasible_topologies": feasible,
            "complete_efx_allocation_count": witness_count,
            "minimum_edge_count": min(map(len, feasible)) if feasible else None,
            "functional_topologies": {
                graph for graph in feasible if functional_topology(graph)
            },
        })

    status, selected = minimum_cover(profiles, all_topologies)
    path_status, selected_paths = minimum_cover(profiles, charity_hamiltonian_paths())
    functional_status, selected_functional = minimum_cover(
        profiles, {graph for graph in all_topologies if functional_topology(graph)}
    )

    profile_rows = []
    path_family = charity_hamiltonian_paths()
    for profile in profiles:
        profile_rows.append({
            "iteration": profile["iteration"],
            "minimum_edge_count": profile["minimum_edge_count"],
            "complete_efx_allocation_count": profile["complete_efx_allocation_count"],
            "feasible_topology_count": len(profile["feasible_topologies"]),
            "feasible_functional_topology_count": len(
                profile["functional_topologies"]
            ),
            "feasible_charity_hamiltonian_path_count": len(
                profile["feasible_topologies"] & path_family
            ),
            "selected_cover_hits": [
                [list(edge) for edge in graph]
                for graph in selected if graph in profile["feasible_topologies"]
            ],
        })
    return {
        "schema": "fixed-u-four-edge-topology-cover-analysis-v1",
        "source": f"results/{source.name}",
        "selected_rounds_sha256": hashlib.sha256(
            json.dumps(rounds, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_round_count": len(rounds),
        "maximum_iteration": maximum_iteration,
        "allocation_menu_count": len(allocation_menu),
        "distinct_feasible_topology_count": len(all_topologies),
        "minimum_cover_status": str(status),
        "minimum_cover_size": len(selected) if status == z3.sat else None,
        "minimum_cover": [
            [list(edge) for edge in graph] for graph in selected
        ],
        "charity_hamiltonian_path_count": 24,
        "hamiltonian_path_cover_status": str(path_status),
        "hamiltonian_path_cover_size": (
            len(selected_paths) if path_status == z3.sat else None
        ),
        "hamiltonian_path_cover": [
            [list(edge) for edge in graph] for graph in selected_paths
        ],
        "functional_topology_cover_status": str(functional_status),
        "functional_topology_cover_size": (
            len(selected_functional) if functional_status == z3.sat else None
        ),
        "functional_topology_cover": [
            [list(edge) for edge in graph] for graph in selected_functional
        ],
        "profiles": profile_rows,
        "claim_boundary": (
            "exact descriptive topology cover of the finite rational profiles in "
            "the recorded source snapshot. A topology covering every observed "
            "profile is not a universally feasible packet selector."
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iteration", type=int)
    args = parser.parse_args()
    result = analyze(args.source, args.maximum_iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "profiles": result["source_round_count"],
        "topologies": result["distinct_feasible_topology_count"],
        "minimum_cover_size": result["minimum_cover_size"],
        "minimum_cover": result["minimum_cover"],
    }, indent=2))


if __name__ == "__main__":
    main()
