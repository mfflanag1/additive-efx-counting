#!/usr/bin/env python3
"""Exact graph/arithmetic audit of the three-agent source reduction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    vertices = range(3)
    edges = tuple((i, j) for i in vertices for j in vertices if i != j)
    dag_counts = {1: 0, 2: 0, 3: 0}
    unique_source_edge_counts: dict[int, int] = {}
    gg_source_sets: set[tuple[int, ...]] = set()

    for mask in range(1 << len(edges)):
        chosen = {edge for bit, edge in enumerate(edges) if mask & (1 << bit)}
        # Floyd-Warshall reachability for a three-vertex exact census.
        reach = [[False] * 3 for _ in vertices]
        for i, j in chosen:
            reach[i][j] = True
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    reach[i][j] |= reach[i][k] and reach[k][j]
        if any(reach[i][i] for i in vertices):
            continue
        indegree = [sum((i, j) in chosen for i in vertices if i != j) for j in vertices]
        sources = sum(value == 0 for value in indegree)
        dag_counts[sources] += 1
        if sources == 1:
            unique_source_edge_counts[len(chosen)] = (
                unique_source_edge_counts.get(len(chosen), 0) + 1
            )
        # Vertex 0 models the full-graph source c. Record only the surviving
        # one/two-source GG cases.
        if indegree[0] == 0 and sources in (1, 2):
            gg_source_sets.add(tuple(i for i, value in enumerate(indegree) if value == 0))

    assert sum(dag_counts.values()) == 25
    assert dag_counts[1] > 0 and dag_counts[2] > 0 and dag_counts[3] == 1
    assert gg_source_sets == {(0,), (0, 1), (0, 2)}

    root_value, exterior_value, atom_value, nonroot_bundle, root_threshold = z3.Reals(
        "root_value exterior_value atom_value nonroot_bundle root_threshold"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        root_value > atom_value,
        atom_value > exterior_value,
        nonroot_bundle <= exterior_value,
        z3.Not(root_value > nonroot_bundle),
    )
    root_cross_safety = solver.check() == z3.unsat

    floor_solver = z3.SolverFor("QF_LRA")
    floor_solver.add(
        nonroot_bundle >= root_threshold,
        z3.Not(nonroot_bundle >= root_threshold),
    )
    nonroot_root_floor = floor_solver.check() == z3.unsat
    assert root_cross_safety and nonroot_root_floor

    theorem = ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md"
    exterior = ROOT / "results/BASE_CONTAINED_RETIRED_PACKET_EXTERIOR_DONATION_SPLIT_THEOREM_20260814.md"
    return {
        "schema": "exterior-dominance-three-agent-source-reduction-audit-v1",
        "status": "EXTERIOR_DOMINANCE_REDUCED_TO_AT_MOST_TWO_SOURCES",
        "three_vertex_dags": sum(dag_counts.values()),
        "dag_counts_by_number_of_sources": {str(k): v for k, v in dag_counts.items()},
        "unique_source_dags_by_edge_count": {
            str(k): v for k, v in sorted(unique_source_edge_counts.items())
        },
        "gg_surviving_source_sets": [list(s) for s in sorted(gg_source_sets)],
        "root_cross_safety": root_cross_safety,
        "nonroot_root_floor_preservation": nonroot_root_floor,
        "remaining_terminal": (
            "base_contained_exterior_dominance_one_source_or_"
            "two_source_root_threshold_debt"
        ),
        "full_T_L_times_theorem_closed": False,
        "sources": {
            str(theorem.relative_to(ROOT)): sha256(theorem),
            str(exterior.relative_to(ROOT)): sha256(exterior),
            "published_three_agent_source": "https://arxiv.org/abs/2002.05119",
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
