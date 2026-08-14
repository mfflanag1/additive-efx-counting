#!/usr/bin/env python3
"""Classify exact escape allocations from the fixed-U packet CEGAR."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


OWNERS = ("r", "q", "d", "s")


def holder_map(allocation):
    return {
        good: recipient
        for recipient, goods in allocation.items()
        for good in goods
    }


def graph_shape(edges):
    vertices = set()
    adjacency = collections.defaultdict(set)
    directed = collections.Counter(edges)
    for source, target in edges:
        vertices.update((source, target))
        adjacency[source].add(target)
        adjacency[target].add(source)
    components = []
    unseen = set(vertices)
    while unseen:
        seed = min(unseen)
        seen = set()
        stack = [seed]
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            stack.extend(adjacency[vertex] - seen)
        components.append(sorted(seen))
        unseen -= seen
    simple_edges = {(source, target) for source, target in edges}
    has_directed_two_cycle = any(
        (target, source) in simple_edges for source, target in simple_edges
        if source != target
    )
    return {
        "connected": len(components) <= 1,
        "components": components,
        "charity_participates": "charity" in vertices,
        "charity_donates": any(source == "charity" for source, _ in edges),
        "charity_receives": any(target == "charity" for _, target in edges),
        "has_parallel_supplier_edges": any(count > 1 for count in directed.values()),
        "has_directed_two_cycle": has_directed_two_cycle,
    }


def analyze(source: Path, iteration=None):
    payload = json.loads(source.read_text())
    if "base" in payload:
        base_allocation = payload["base"]
        goods = payload["goods"]
        records = [
            {"mode": record.get("mode"), "allocation": record.get("blocking_allocation")}
            for record in payload["iterations"]
        ]
    else:
        # The batch artifact is seeded by the discovery artifact, which is the
        # authoritative source for the shared atomization.
        seed_path = Path(payload["seed"])
        seed = json.loads(seed_path.read_text())
        if payload.get("edge_origin") == "support":
            base_allocation = seed["support_state"]
        else:
            base_allocation = seed["base"]
        goods = seed["goods"]
        selected_rounds = [
            round_record for round_record in payload["rounds"]
            if iteration is None or round_record.get("iteration") == iteration
        ]
        records = [
            {
                "iteration": round_record.get("iteration"),
                "mode": round_record.get("mode"),
                "reported_minimum": round_record.get("minimum_radius"),
                "allocation": allocation,
            }
            for round_record in selected_rounds
            for allocation in round_record.get("blocking_allocations", [])
        ]
    base = holder_map(base_allocation)
    radii = collections.Counter()
    charity_bundles = collections.Counter()
    moved_goods = collections.Counter()
    transfer_graphs = collections.Counter()
    edge_counts = collections.Counter()
    simple_transfer_graphs = collections.Counter()
    retained_base_goods = collections.Counter()
    charity_sources = collections.Counter()
    shape_counts = collections.Counter()

    mode_counts = collections.Counter()
    for record in records:
        allocation = record["allocation"]
        if allocation is None:
            continue
        mode_counts[record["mode"]] += 1
        holder = holder_map(allocation)
        moved = tuple(good for good in goods if holder[good] != base[good])
        radii[len(moved)] += 1
        charity_bundles[tuple(allocation["charity"])] += 1
        moved_goods.update(moved)
        transfer_graphs[tuple(sorted((base[good], holder[good]) for good in moved))] += 1
        simple_graph = tuple(sorted(set((base[good], holder[good]) for good in moved)))
        edge_counts[len(simple_graph)] += 1
        simple_transfer_graphs[simple_graph] += 1
        shape = graph_shape(tuple((base[good], holder[good]) for good in moved))
        shape_counts[tuple(sorted((key, json.dumps(value, sort_keys=True))
                                  for key, value in shape.items()))] += 1
        charity_sources[tuple(sorted(base[good] for good in allocation["charity"]))] += 1
        for owner in OWNERS:
            retained = tuple(sorted(set(base_allocation[owner]) & set(allocation[owner])))
            retained_base_goods[owner, retained] += 1

    def rows(counter, limit=None):
        values = counter.most_common(limit)
        return [{"key": list(key) if isinstance(key, tuple) else key, "count": count}
                for key, count in values]

    return {
        "schema": "fixed-u-full-packet-escape-analysis-v1",
        "source": str(source),
        "source_iteration": iteration,
        "source_status": payload["status"],
        "escape_count": sum(radii.values()),
        "mode_counts": dict(mode_counts),
        "move_radius_counts": dict(sorted(radii.items())),
        "packet_edge_counts": dict(sorted(edge_counts.items())),
        "moved_good_counts": dict(moved_goods.most_common()),
        "charity_bundles": rows(charity_bundles),
        "charity_source_multisets": rows(charity_sources),
        "transfer_graph_count": len(transfer_graphs),
        "simple_transfer_graph_count": len(simple_transfer_graphs),
        "top_simple_transfer_graphs": rows(simple_transfer_graphs, 50),
        "top_transfer_graphs": rows(transfer_graphs, 25),
        "graph_shape_counts": [
            {
                "shape": {key: json.loads(value) for key, value in shape},
                "count": count,
            }
            for shape, count in shape_counts.most_common()
        ],
        "retained_base_goods": [
            {"owner": owner, "goods": list(goods), "count": count}
            for (owner, goods), count in retained_base_goods.most_common()
        ],
        "claim_boundary": (
            "descriptive census of exact CEGAR escape allocations; frequencies do not "
            "prove that any listed transfer template is universally feasible"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iteration", type=int)
    args = parser.parse_args()
    result = analyze(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "escape_count": result["escape_count"],
        "move_radius_counts": result["move_radius_counts"],
        "transfer_graph_count": result["transfer_graph_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
