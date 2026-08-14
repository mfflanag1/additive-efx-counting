#!/usr/bin/env python3
"""Exhaustive audit of net base-transfer cuts and closed support unions."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


VERTICES = ("r", "q", "s", "d", "charity")
GOODS = tuple(range(4))


def cut_is_closed(base, final, subset):
    return all((base[g] in subset) == (final[g] in subset) for g in GOODS)


def aggregate_goods(assignment, subset):
    return frozenset(g for g in GOODS if assignment[g] in subset)


def net_edges(base, final):
    return {
        frozenset((base[g], final[g]))
        for g in GOODS if base[g] != final[g]
    }


def components(edges):
    remaining = set(VERTICES)
    rows = []
    while remaining:
        component = {next(iter(remaining))}
        while True:
            enlarged = component | {
                vertex
                for edge in edges if edge & component
                for vertex in edge
            }
            if enlarged == component:
                break
            component = enlarged
        rows.append(frozenset(component))
        remaining -= component
    return rows


def exhaustive_cut_audit():
    assignments = tuple(itertools.product(VERTICES, repeat=len(GOODS)))
    proper_subsets = tuple(
        frozenset(subset)
        for size in range(1, len(VERTICES))
        for subset in itertools.combinations(VERTICES, size)
    )
    pair_count = 0
    cut_count = 0
    disconnected_count = 0
    for base in assignments:
        for final in assignments:
            pair_count += 1
            edges = net_edges(base, final)
            comps = components(edges)
            if len(comps) > 1:
                disconnected_count += 1
            for subset in proper_subsets:
                cut_count += 1
                no_crossing = not any(
                    bool(edge & subset) and bool(edge - subset) for edge in edges
                )
                same_union = (
                    aggregate_goods(base, subset)
                    == aggregate_goods(final, subset)
                )
                closed = cut_is_closed(base, final, subset)
                assert no_crossing == closed == same_union
            for component in comps:
                assert (
                    aggregate_goods(base, component)
                    == aggregate_goods(final, component)
                )
    return {
        "assignment_count": len(assignments),
        "base_final_pair_count": pair_count,
        "proper_cut_checks": cut_count,
        "disconnected_pair_count": disconnected_count,
    }


def counterexample():
    # Goods follow the Y-relative path c->r->s->q->d.
    current = ("charity", "r", "s", "q")
    final = ("r", "s", "q", "d")
    base = ("s", "q", "r", "charity")
    current_edges = {
        frozenset((current[g], final[g])) for g in GOODS
    }
    assert len(current_edges) == 4
    assert len(components(current_edges)) == 1
    assert all(base[g] != final[g] for g in GOODS)
    base_edges = net_edges(base, final)
    base_components = set(components(base_edges))
    expected = {
        frozenset(("r", "q", "s")),
        frozenset(("d", "charity")),
    }
    assert base_components == expected
    return {
        "base": list(base),
        "current": list(current),
        "final": list(final),
        "current_component_count": 1,
        "net_base_components": [sorted(row) for row in sorted(
            base_components, key=lambda row: sorted(row)
        )],
        "whole_return_packet_count": 0,
    }


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "BRANCH_TREE_BASE_CANCELLATION_OR_CLOSED_UNION_LEMMA_20260814.md"
    census = exhaustive_cut_audit()
    witness = counterexample()
    return {
        "schema": "branch-tree-base-cancellation-closed-union-v1",
        "status": "CLOSED_UNION_EQUIVALENCE_EXHAUSTED",
        "owner_plus_charity_count": len(VERTICES),
        "good_count": len(GOODS),
        "census": census,
        "whole_return_shortcut_counterexample": witness,
        "checks": [
            "no net edge crosses K iff base/final membership agrees goodwise",
            "goodwise membership agreement iff aggregate physical unions agree",
            "every net connected component preserves its exact base-good union",
            "connected Y-tree can have disconnected X-net graph with no whole return",
        ],
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "finite exhaustive audit of the cap-free set identity and exact "
            "counterexample; response rank, outsider safety, PI, and EFX are "
            "not inferred"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "census": result["census"],
        "counterexample_components": result[
            "whole_return_shortcut_counterexample"
        ]["net_base_components"],
    }, indent=2))


if __name__ == "__main__":
    main()
