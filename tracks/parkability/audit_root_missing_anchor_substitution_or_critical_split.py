#!/usr/bin/env python3
"""Audit anchor substitution on the six root-missing source maps."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))
NONROOT = (1, 2, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def survivor_maps():
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        if len(set(mapping)) != 3 or 0 in set(mapping):
            continue
        duplicate = next(source for source in NONROOT if mapping.count(source) == 2)
        if mapping[0] != duplicate:
            continue
        yield mapping, duplicate


def substitution_edges(mapping, anchor_supplier):
    duplicate = mapping[0]
    predecessor = next(target for target in NONROOT if mapping[target] == duplicate)
    edges = {("charity", "0")}
    if anchor_supplier != duplicate:
        edges.add((str(anchor_supplier), str(duplicate)))
    for target in NONROOT:
        if target == predecessor:
            continue
        if target != mapping[target]:
            edges.add((str(target), str(mapping[target])))
    return predecessor, edges


def run(root: Path = ROOT) -> dict[str, object]:
    maps = list(survivor_maps())
    assert len(maps) == 6
    histogram = Counter()
    aligned = Counter()
    witnesses = []
    for anchor_supplier in NONROOT:
        for mapping, duplicate in maps:
            predecessor, edges = substitution_edges(mapping, anchor_supplier)
            histogram[len(edges)] += 1
            aligned[duplicate == anchor_supplier] += 1
            witnesses.append({
                "anchor_supplier": anchor_supplier,
                "mapping": list(mapping),
                "duplicate_source": duplicate,
                "omitted_predecessor": predecessor,
                "supplier_aligned": duplicate == anchor_supplier,
                "edge_count": len(edges),
            })

    yr, p, base, anchor = z3.Reals("yr p base anchor")
    root = z3.SolverFor("QF_LRA")
    root.add(yr > 0, p > 0, anchor > 0, yr + anchor > base)
    root.add(yr + p <= base)
    root.add(z3.Not(anchor > base - yr - p))

    h, mu = z3.Reals("h mu")
    source = z3.SolverFor("QF_LRA")
    source.add(mu > 0, h >= 0)
    source.add(z3.Not((h < mu) == ((mu - h) > 0)))

    theorem = root_path = Path(__file__).resolve().parents[2] / "results/ROOT_MISSING_ANCHOR_SUBSTITUTION_OR_CRITICAL_SPLIT_LEMMA_20260814.md"
    parent = root_path.parent / "LIQUIDATED_ROOT_THREE_SOURCE_PHYSICAL_COMPRESSION_FRONTIER_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Supplier-aligned partial-anchor split" in text
    assert "Supplier-misaligned boundary" in text

    return {
        "schema": "root-missing-anchor-substitution-critical-split-audit-v1",
        "status": "CONDITIONAL_SIX_MAP_ROOT_WALL_SPLIT_FRONTIER",
        "survivor_map_count": len(maps),
        "labelled_anchor_map_count": len(witnesses),
        "substitution_edge_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "supplier_alignment_histogram": {
            "aligned": aligned[True], "misaligned": aligned[False]
        },
        "all_substitutions_at_most_four_edges": all(
            witness["edge_count"] <= 4 for witness in witnesses
        ),
        "root_threshold_nonempty_under_wall": root.check() == z3.unsat,
        "source_split_identity": source.check() == z3.unsat,
        "packet_size_bound_used": False,
        "pure_cell_lift_proved": False,
        "accumulated_fan_application_proved": False,
        "observer_safety_proved": False,
        "misaligned_wall_closed": False,
        "fixed_u_theorem_proved": False,
        "survivor_mappings": [list(mapping) for mapping, _ in maps],
        "provenance": {
            str(path.relative_to(root_path.parents[1])): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "conditional on the unproved pure-cell lift, anchor substitution "
            "gives a four-edge probe for all six maps; "
            "root release is the only payment wall, and only the supplier-"
            "aligned third admits the partial-anchor critical-split frontier"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
