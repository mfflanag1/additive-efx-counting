#!/usr/bin/env python3
"""Classify the rank-three sacrificed-hole gate missed by rank-four extraction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = ("r", "q", "c", "s")
TARGETS = (*OWNERS, "charity")
ANCHOR = ("r", "q")
SACRIFICED = "c"
PRIORITY = ("q", "s", "c")
ALLOWED = tuple(
    (source, target)
    for source in OWNERS
    for target in TARGETS
    if target == "charity" or source != target
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_key(matching: tuple[tuple[str, str], ...]) -> tuple:
    represented = {source for source, _ in matching}
    target_index = {target: index for index, target in enumerate(TARGETS)}
    physical_tie = tuple(
        -target_index.get(dict(matching).get(source), len(TARGETS))
        for source in OWNERS
    )
    return (
        len(matching),
        *(int(source in represented) for source in PRIORITY),
        physical_tie,
    )


def selected_matching(edges: frozenset[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    candidates = []
    for size in range(1, 5):
        for chosen in itertools.combinations(edges, size):
            sources = [source for source, _ in chosen]
            targets = [target for _, target in chosen]
            if ANCHOR not in chosen:
                continue
            if len(set(sources)) != size or len(set(targets)) != size:
                continue
            candidates.append(tuple(sorted(chosen)))
    assert candidates
    return max(candidates, key=matching_key)


def owner_cycle_free(edges: frozenset[tuple[str, str]]) -> bool:
    adjacency = {owner: set() for owner in OWNERS}
    for source, target in edges:
        if target in adjacency:
            adjacency[source].add(target)

    def cyclic_from(start: str, node: str, seen: set[str]) -> bool:
        for child in adjacency[node]:
            if child == start:
                return True
            if child not in seen and cyclic_from(start, child, seen | {child}):
                return True
        return False

    return not any(cyclic_from(owner, owner, {owner}) for owner in OWNERS)


def physically_connected(edges: frozenset[tuple[str, str]]) -> bool:
    vertices = set(TARGETS)
    adjacency = {vertex: set() for vertex in vertices}
    for source, target in edges:
        adjacency[source].add(target)
        adjacency[target].add(source)
    seen, stack = set(), ["r"]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adjacency[node] - seen)
    return vertices <= seen


def realize_minimal_graph(edges: frozenset[tuple[str, str]]) -> dict:
    # Each target is a singleton atom.  Its EFX threshold after deleting its
    # least good is zero, so every target is common-safe.  Edge values 2 and
    # nonedge values 1/2 exactly realize the desired-response graph above a
    # unit base/current floor.  This is a positive rational graph witness,
    # not a full globally maximal GG countermodel.
    valuations = {
        source: {
            f"atom:{target}": ("2" if (source, target) in edges else "1/2")
            for target in TARGETS
        }
        for source in OWNERS
    }
    desired = {
        (source, target)
        for source in OWNERS
        for target in TARGETS
        if source != target and valuations[source][f"atom:{target}"] == "2"
    }
    assert desired == set(edges)
    return {
        "base_floor_each_source": "1",
        "singleton_target_threshold_each_observer": "0",
        "valuations": valuations,
        "exact_desired_response_edges": [list(edge) for edge in sorted(desired)],
        "positive_rational": True,
        "full_GG_countermodel": False,
    }


def run(root: Path) -> dict:
    optional = tuple(edge for edge in ALLOWED if edge != ANCHOR)
    survivors = []
    for mask in range(1 << len(optional)):
        edges = frozenset(
            {ANCHOR}
            | {optional[index] for index in range(len(optional)) if mask & (1 << index)}
        )
        matching = selected_matching(edges)
        represented = {source for source, _ in matching}
        if len(matching) != 3 or represented != {"r", "q", "s"}:
            continue
        if (SACRIFICED, "q") not in edges:
            continue
        if not owner_cycle_free(edges) or not physically_connected(edges):
            continue
        matched_targets = {target for _, target in matching}
        holes = sorted(set(TARGETS) - matched_targets)
        assert len(holes) == 2
        survivors.append(
            {
                "edges": [list(edge) for edge in sorted(edges)],
                "selected_matching": [list(edge) for edge in matching],
                "holes": holes,
                "edge_count": len(edges),
            }
        )

    assert survivors
    minimum = min(item["edge_count"] for item in survivors)
    minimal = [item for item in survivors if item["edge_count"] == minimum]
    edge_histogram = Counter(item["edge_count"] for item in survivors)
    hole_histogram = Counter(tuple(item["holes"]) for item in survivors)
    matching_histogram = Counter(
        tuple(tuple(edge) for edge in item["selected_matching"])
        for item in survivors
    )
    witness_edges = frozenset(tuple(edge) for edge in minimal[0]["edges"])
    witness = dict(minimal[0])
    witness["rational_response_realization"] = realize_minimal_graph(witness_edges)

    theorem = root / "results/RANK_THREE_EXACT_REPEAT_CLOSURE_GATE_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "rank-three-exact-repeat-gate-v1",
        "status": "RANK_THREE_TWO_HOLE_OBSTRUCTION_EXISTS",
        "response_graphs_checked": 1 << len(optional),
        "survivor_count": len(survivors),
        "minimum_edge_count": minimum,
        "minimal_survivor_count": len(minimal),
        "minimal_survivors": minimal,
        "survivor_edge_count_histogram": {
            str(key): value for key, value in sorted(edge_histogram.items())
        },
        "survivor_hole_pair_histogram": {
            ",".join(key): value for key, value in sorted(hole_histogram.items())
        },
        "survivor_selected_matching_histogram": {
            ";".join(f"{source}->{target}" for source, target in key): value
            for key, value in sorted(matching_histogram.items())
        },
        "witness": witness,
        "checks": {
            "anchor_forced": ANCHOR in witness_edges,
            "selected_rank_is_three": len(witness["selected_matching"]) == 3,
            "sacrificed_owner_unrepresented": all(
                edge[0] != SACRIFICED for edge in witness["selected_matching"]
            ),
            "sacrificed_owner_is_root_facing": [SACRIFICED, "q"] in witness["edges"],
            "two_target_holes_remain": len(witness["holes"]) == 2,
            "all_owner_charity_graph_connected": physically_connected(witness_edges),
            "available_owner_response_graph_cycle_free": owner_cycle_free(witness_edges),
            "positive_rational_response_realization": witness[
                "rational_response_realization"
            ]["positive_rational"],
        },
        "claim_boundary": (
            "exact exhaustive graph-level refutation of the implication from "
            "full physical owner coverage plus anchor-constrained priority to a "
            "rank-four Hamiltonian response state; not a full-premise GG or EFX "
            "countermodel"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "response_graphs_checked", "survivor_count",
        "minimum_edge_count", "minimal_survivor_count"
    )}, indent=2))


if __name__ == "__main__":
    main()
