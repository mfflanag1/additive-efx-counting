#!/usr/bin/env python3
"""Classify nearest repairs of the q=4 nine-good row-merge boundary."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )
    from .core import iter_unlabeled_nonempty_partitions, validate_values
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )
    from core import iter_unlabeled_nonempty_partitions, validate_values


SCHEMA = "row-merge-q4-distance-three-exchange-analysis-v1"
N = 4
MATCHINGS = tuple(itertools.permutations(range(N)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def optimal_alignments(base, candidate):
    scored = tuple(
        (
            sum(
                len(set(base[index]) & set(candidate[order[index]]))
                for index in range(N)
            ),
            order,
        )
        for order in MATCHINGS
    )
    optimum = max(score for score, _order in scored)
    return tuple(order for score, order in scored if score == optimum)


def transfer_edges(base, candidate, alignment):
    destination = {
        good: base_index
        for base_index, candidate_index in enumerate(alignment)
        for good in candidate[candidate_index]
    }
    return tuple(
        (source, destination[good], good)
        for source, bundle in enumerate(base)
        for good in bundle
        if destination[good] != source
    )


def simple_chain_type(edges):
    vertices = {vertex for edge in edges for vertex in edge[:2]}
    indegree = {vertex: 0 for vertex in vertices}
    outdegree = {vertex: 0 for vertex in vertices}
    adjacency = {vertex: set() for vertex in vertices}
    for source, target, _good in edges:
        outdegree[source] += 1
        indegree[target] += 1
        adjacency[source].add(target)
        adjacency[target].add(source)
    if any(indegree[v] > 1 or outdegree[v] > 1 for v in vertices):
        return None
    seen = set()
    stack = [next(iter(vertices))]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    if seen != vertices:
        return None
    if len(vertices) == len(edges) and all(
        indegree[v] == outdegree[v] == 1 for v in vertices
    ):
        return "cycle"
    starts = [v for v in vertices if indegree[v] == 0 and outdegree[v] == 1]
    ends = [v for v in vertices if indegree[v] == 1 and outdegree[v] == 0]
    internal = [v for v in vertices if indegree[v] == outdegree[v] == 1]
    if (
        len(vertices) == len(edges) + 1
        and len(starts) == len(ends) == 1
        and len(internal) == len(edges) - 1
    ):
        return "path"
    return None


def exchange_chain_partitions(base, maximum_length):
    found = set()
    for length in range(1, maximum_length + 1):
        for vertices in itertools.permutations(range(N), length + 1):
            if len(set(vertices)) != len(vertices):
                continue
            edges = tuple(zip(vertices[:-1], vertices[1:]))
            for goods in itertools.product(*(base[source] for source, _ in edges)):
                if any(
                    len(base[source])
                    == sum(edge_source == source for edge_source, _ in edges)
                    for source in range(N)
                ):
                    continue
                moved = [list(bundle) for bundle in base]
                for (source, target), good in zip(edges, goods):
                    moved[source].remove(good)
                    moved[target].append(good)
                found.add(canonical(moved))
    for length in range(2, maximum_length + 1):
        for vertices in itertools.permutations(range(N), length):
            if vertices[0] != min(vertices):
                continue
            edges = tuple(
                (vertices[index], vertices[(index + 1) % length])
                for index in range(length)
            )
            for goods in itertools.product(*(base[source] for source, _ in edges)):
                moved = [list(bundle) for bundle in base]
                for (source, target), good in zip(edges, goods):
                    moved[source].remove(good)
                    moved[target].append(good)
                found.add(canonical(moved))
    return tuple(sorted(found))


def run(source_path: Path, output_path: Path) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != "row-merge-q4-small-step-radius-cegar-v1"
        or source.get("status") != "RADIUS_PIVOT_REFUTATION_FOUND"
        or source.get("m") != 9
        or source.get("radius") != 2
    ):
        raise ValueError("source is not the terminal q=4 nine-good boundary")
    validate_values(source["terminal_wall_values"], expected_n=N, lower=1)
    post = validate_values(
        source["terminal_post_wall_values"], expected_n=N, lower=1
    )
    base = tuple(tuple(bundle) for bundle in source["wall_partition"])
    if base != ((0, 1), (2, 3), (4, 5), (6, 7, 8)):
        raise AssertionError("the wall partition changed")

    nearest = []
    global_support_count = 0
    for candidate in iter_unlabeled_nonempty_partitions(N, 9):
        feasible = graph(post, candidate)
        count = matching_count(feasible)
        if not count:
            continue
        global_support_count += 1
        if transfer_distance(canonical(base), candidate) != 3:
            continue
        records = []
        for alignment in optimal_alignments(base, candidate):
            edges = transfer_edges(base, candidate, alignment)
            records.append(
                {
                    "alignment": list(alignment),
                    "edges": [
                        {"source": source, "target": target, "good": good}
                        for source, target, good in edges
                    ],
                    "simple_chain_type": simple_chain_type(edges),
                }
            )
        efx_matchings = [
            list(matching)
            for matching in MATCHINGS
            if all(feasible[agent][matching[agent]] for agent in range(N))
        ]
        nearest.append(
            {
                "partition": [list(bundle) for bundle in candidate],
                "matching_count": count,
                "efx_matchings": efx_matchings,
                "optimal_alignment_records": records,
                "has_simple_three_exchange_chain": any(
                    record["simple_chain_type"] in {"path", "cycle"}
                    for record in records
                ),
            }
        )

    menu = exchange_chain_partitions(base, 3)
    supporting_menu = []
    for candidate in menu:
        count = matching_count(graph(post, candidate))
        if count:
            supporting_menu.append(
                {
                    "partition": [list(bundle) for bundle in candidate],
                    "matching_count": count,
                    "distance": transfer_distance(canonical(base), candidate),
                }
            )
    if (
        global_support_count != 123
        or len(nearest) != 20
        or len(menu) != 515
        or len(supporting_menu) != 8
        or any(record["distance"] != 3 for record in supporting_menu)
    ):
        raise AssertionError("the nearest-repair classification changed")

    result = {
        "schema": SCHEMA,
        "status": "DISTANCE_THREE_EXCHANGE_MOTIF_CLASSIFIED",
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "n": N,
        "m": 9,
        "wall_partition": [list(bundle) for bundle in base],
        "global_supporting_partition_count": global_support_count,
        "nearest_transfer_distance": 3,
        "nearest_supporting_partition_count": len(nearest),
        "nearest_supporting_partitions": nearest,
        "simple_exchange_chain_maximum_length": 3,
        "simple_exchange_chain_partition_count": len(menu),
        "supporting_simple_exchange_chain_partition_count": len(supporting_menu),
        "supporting_simple_exchange_chain_partitions": supporting_menu,
        "interpretation": (
            "The first unbalanced q=4 boundary has a complete EFX repair "
            "generated by a simple three-good path or cycle. This identifies "
            "a compact successor menu but does not prove that the menu works "
            "for every wall profile."
        ),
        "claim_boundary": (
            "This is an exact classification of one fixed positive-additive "
            "profile, not a row-merge continuation theorem."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
