#!/usr/bin/env python3
"""Exact EFX census of the endpoint-6 root-fixed no-go profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .audit_allocated_e_paid_strengthening_counterprofile import complete_efx
from .run_allocated_e_allocation_atom_cegar import complete_menu
from .run_allocated_e_endpoint6_root_fixed_completion_cegar import support_edges
from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE


ROOT = Path(__file__).resolve().parents[2]


def key(goods):
    return "+".join(sorted(goods)) or "empty"


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }
    current_root = frozenset(SUPPORT_STATE["r"])
    root_counts = Counter()
    edge_counts = Counter()
    distance_counts = Counter()
    witnesses = []
    menu = complete_menu()
    for allocation in menu:
        if not complete_efx(values, allocation):
            continue
        root = frozenset(allocation["r"])
        edges = support_edges(allocation)
        root_counts[key(root)] += 1
        edge_counts[len(edges)] += 1
        distance = len(root ^ current_root)
        distance_counts[distance] += 1
        if len(witnesses) < 100:
            witnesses.append({
                "allocation": allocation,
                "edges": [list(edge) for edge in sorted(edges)],
                "root_removed": sorted(current_root - root),
                "root_added": sorted(root - current_root),
                "root_symmetric_difference": distance,
            })
    efx_count = sum(root_counts.values())
    assert efx_count > 0
    assert root_counts.get(key(current_root), 0) == 0
    result = {
        "schema": "endpoint6-root-fixed-countermodel-efx-census-v1",
        "status": "CENSUS_COMPLETE",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "allocation_menu_count": len(menu),
        "efx_allocation_count": efx_count,
        "current_root_bundle": sorted(current_root),
        "current_root_efx_count": 0,
        "minimum_root_symmetric_difference": min(distance_counts),
        "root_symmetric_difference_counts": dict(sorted(distance_counts.items())),
        "support_edge_counts": dict(sorted(edge_counts.items())),
        "root_bundle_counts": dict(root_counts.most_common()),
        "first_witnesses": witnesses,
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact census inside the 93,480-member bounded atom menu. It "
            "describes necessary anchor movement for this profile only."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps({
        "status": result["status"],
        "menu": result["allocation_menu_count"],
        "efx": result["efx_allocation_count"],
        "minimum_root_symmetric_difference": result["minimum_root_symmetric_difference"],
        "root_bundle_count": len(result["root_bundle_counts"]),
    }, indent=2))


if __name__ == "__main__":
    main()
