#!/usr/bin/env python3
"""Independent graph audit of PI-free support drainage."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "PI_FREE_DESIRED_CORE_SUPPORT_DRAINAGE_LEMMA_20260813.md"
OWNERS = tuple(range(4))


def reaches_outside(vertices, edges, start):
    outside = set(OWNERS) - set(vertices)
    queue = deque((start,))
    reached = {start}
    while queue:
        source = queue.popleft()
        for tail, head in edges:
            if tail != source:
                continue
            if head in outside:
                return True
            if head not in reached:
                reached.add(head)
                queue.append(head)
    return False


def no_closed_subset(vertices, edges):
    vertices = tuple(vertices)
    for size in range(1, len(vertices) + 1):
        for subset in itertools.combinations(vertices, size):
            subset = set(subset)
            if not any(tail in subset and head not in subset for tail, head in edges):
                return False
    return True


def audit():
    records = 0
    positive = 0
    for size in range(1, 4):
        for vertices in itertools.combinations(OWNERS, size):
            possible = tuple((tail, head) for tail in vertices for head in OWNERS)
            for mask in range(1 << len(possible)):
                edges = {
                    edge for index, edge in enumerate(possible)
                    if mask & (1 << index)
                }
                closed_free = no_closed_subset(vertices, edges)
                reachability = all(
                    reaches_outside(vertices, edges, vertex) for vertex in vertices
                )
                assert closed_free == reachability
                if closed_free:
                    positive += 1
                    # One shortest-path successor per vertex produces a forest
                    # with at most |R| edges and all paths leaving R.
                    selected = {}
                    outside = set(OWNERS) - set(vertices)
                    for start in vertices:
                        queue = deque((start,))
                        predecessor = {start: None}
                        exit_edge = None
                        while queue and exit_edge is None:
                            tail = queue.popleft()
                            for edge_tail, head in edges:
                                if edge_tail != tail:
                                    continue
                                if head in outside:
                                    exit_edge = (tail, head)
                                    break
                                if head not in predecessor:
                                    predecessor[head] = tail
                                    queue.append(head)
                        assert exit_edge is not None
                        tail, head = exit_edge
                        selected[tail] = head
                        while predecessor[tail] is not None:
                            parent = predecessor[tail]
                            selected[parent] = tail
                            tail = parent
                    assert len(selected) <= len(vertices)
                    assert all(
                        reaches_outside(vertices, set(selected.items()), vertex)
                        for vertex in vertices
                    )
                records += 1

    return {
        "schema": "pi-free-desired-core-support-drainage-audit-v1",
        "status": "NO_CLOSED_SUBSET_IFF_OUTSIDE_DRAINAGE_VERIFIED",
        "graph_records": records,
        "positive_drainage_records": positive,
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free graph consequence. Payment, physical-supplier edge "
            "compression, observer safety, and final EFX remain open."
        ),
    }


def main():
    output = ROOT / "results" / "pi_free_desired_core_support_drainage_audit.json"
    result = audit()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "records": result["graph_records"],
        "positive": result["positive_drainage_records"],
    }, indent=2))


if __name__ == "__main__":
    main()
