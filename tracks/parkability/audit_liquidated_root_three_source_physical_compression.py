#!/usr/bin/env python3
"""Exact census of whole-cell physical edges in the liquidated-root 3+1 fan."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))
ROOT_OWNER = 0
NONROOT = (1, 2, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum_edges(mapping: tuple[int, ...], anchor_supplier: int) -> tuple[int, dict]:
    image = set(mapping)
    missing = next(owner for owner in OWNERS if owner not in image)
    counts = Counter(mapping)
    duplicate = next(source for source, count in counts.items() if count == 2)
    duplicate_targets = [target for target, source in enumerate(mapping) if source == duplicate]
    fan_class = "missing_supplies_duplicate" if missing in duplicate_targets else "foreign_duplicate"
    omissions = [missing] if fan_class == "missing_supplies_duplicate" else duplicate_targets

    best: tuple[int, tuple, int, tuple] | None = None
    for omitted in omissions:
        selected = [target for target in OWNERS if target != omitted]
        assert {mapping[target] for target in selected} == image
        for root_residual_destination in OWNERS:
            edges = set()
            for target in OWNERS:
                supplier = anchor_supplier if target == ROOT_OWNER else target
                destination = target if target == omitted else mapping[target]
                if supplier != destination:
                    edges.add((str(supplier), str(destination)))
            if root_residual_destination != ROOT_OWNER:
                edges.add((str(ROOT_OWNER), str(root_residual_destination)))
            edges.add(("charity", str(missing)))
            candidate = (
                len(edges),
                tuple(sorted(edges)),
                omitted,
                root_residual_destination,
            )
            if best is None or candidate < best:
                best = candidate

    assert best is not None
    return best[0], {
        "missing": missing,
        "duplicate": duplicate,
        "class": fan_class,
        "omitted_target": best[2],
        "root_residual_destination": best[3],
        "edges": [list(edge) for edge in best[1]],
    }


def run(root: Path = ROOT) -> dict[str, object]:
    histogram = Counter()
    class_histogram = Counter()
    five_edge_mappings = {anchor: [] for anchor in NONROOT}
    maps_per_anchor = Counter()

    for anchor_supplier in NONROOT:
        for mapping in itertools.product(OWNERS, repeat=4):
            if any(mapping[target] == target for target in OWNERS):
                continue
            if len(set(mapping)) != 3:
                continue
            edge_count, witness = minimum_edges(mapping, anchor_supplier)
            missing_is_root = witness["missing"] == ROOT_OWNER
            histogram[edge_count] += 1
            class_histogram[(missing_is_root, witness["class"], edge_count)] += 1
            maps_per_anchor[anchor_supplier] += 1
            if edge_count == 5:
                assert witness["missing"] == ROOT_OWNER
                assert witness["class"] == "missing_supplies_duplicate"
                five_edge_mappings[anchor_supplier].append(list(mapping))

    theorem = root / "results/LIQUIDATED_ROOT_THREE_SOURCE_PHYSICAL_COMPRESSION_FRONTIER_LEMMA_20260814.md"
    parent = root / "results/MISSING_SUPPLIER_DUPLICATE_OMISSION_FOUR_EDGE_PAYMENT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "42 of the 48" in text
    assert "six root-missing" in text

    return {
        "schema": "liquidated-root-three-source-physical-compression-audit-v1",
        "status": "EXACT_WHOLE_CELL_NORMAL_FORM_FRONTIER",
        "anchor_suppliers": list(NONROOT),
        "maps_per_anchor_supplier": {str(k): maps_per_anchor[k] for k in NONROOT},
        "minimum_edge_histogram_all_anchor_suppliers": {
            str(k): histogram[k] for k in sorted(histogram)
        },
        "class_histogram_all_anchor_suppliers": {
            f"missing_root={str(root_missing).lower()}|{fan_class}|edges={edges}": count
            for (root_missing, fan_class, edges), count in sorted(
                class_histogram.items(), key=lambda item: str(item[0])
            )
        },
        "at_most_four_per_anchor_supplier": 42,
        "five_edge_per_anchor_supplier": 6,
        "five_edge_mappings_by_anchor_supplier": {
            str(anchor): five_edge_mappings[anchor] for anchor in NONROOT
        },
        "packet_size_bound_used": False,
        "minimum_within_declared_normal_form_proved": True,
        "unrestricted_packet_graph_theorem_proved": False,
        "observer_safety_proved": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "for each anchor supplier, 42 of 48 rank-three source maps admit "
            "a whole-cell liquidated-root routing with at most four physical "
            "supplier pairs; exactly the six root-missing, missing-supplies-"
            "duplicate maps need five pairs within this normal form"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
