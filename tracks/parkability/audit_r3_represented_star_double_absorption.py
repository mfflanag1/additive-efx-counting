#!/usr/bin/env python3
"""Audit the signed-edge identity for R3 represented-star absorption."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
CYCLE = {"r": "q", "q": "s", "s": "r"}  # response source -> target
REPRESENTED = frozenset(CYCLE)


def predecessor(owner):
    return next(source for source, target in CYCLE.items() if target == owner)


def records():
    output = []
    initial = {(target, source) for source, target in CYCLE.items()}
    for common_source in sorted(REPRESENTED):
        targets = tuple(sorted(REPRESENTED - {common_source}))
        for first_residual_used in (False, True):
            for second_residual_used in (False, True):
                residual_used = dict(zip(
                    targets, (first_residual_used, second_residual_used), strict=True
                ))
                destinations = {supplier: {recipient} for supplier, recipient in initial}
                # Complete and move each target's entire incoming matching
                # packet to the common star source.  Optional retained residual
                # parts have the target itself as supplier.
                for target in targets:
                    incoming_supplier = CYCLE[target]
                    destinations[incoming_supplier].discard(target)
                    destinations[incoming_supplier].add(common_source)
                    if residual_used[target]:
                        destinations.setdefault(target, set()).add(common_source)
                owner_edges = {
                    (supplier, recipient)
                    for supplier, recipients in destinations.items()
                    for recipient in recipients if supplier != recipient
                }
                expected = {
                    (supplier, common_source)
                    for supplier in REPRESENTED - {common_source}
                }
                assert owner_edges == expected
                # Parking charity at either depleted target adds only one edge.
                for charity_target in targets:
                    final_edges = owner_edges | {("charity", charity_target)}
                    assert len(final_edges) == 3
                    output.append({
                        "common_source": common_source,
                        "targets": list(targets),
                        "residual_used": residual_used,
                        "charity_target": charity_target,
                        "initial_owner_edges": sorted([list(edge) for edge in initial]),
                        "final_edges": sorted([list(edge) for edge in final_edges]),
                        "owner_edge_count": len(owner_edges),
                        "total_edge_count": len(final_edges),
                    })
    return output


def run(root: Path):
    rows = records()
    assert len(rows) == 24
    assert {row["common_source"] for row in rows} == {"r", "q", "s"}
    assert all(row["owner_edge_count"] == 2 for row in rows)
    assert all(row["total_edge_count"] == 3 for row in rows)
    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_REPRESENTED_STAR_DOUBLE_ABSORPTION_LEMMA_20260814.md"
    return {
        "schema": "r3-represented-star-double-absorption-audit-v1",
        "status": "EXACT_TWO_OWNER_EDGE_DOUBLE_ABSORPTION",
        "records_checked": len(rows),
        "records": rows,
        "monotone_continuation": (
            "every later response by the common source into either depleted "
            "target moves a nonempty residual subset along one of the same two "
            "supplier-to-source pairs; no new edge is created and the residual "
            "union strictly shrinks"
        ),
        "terminal_response_boundary": (
            "after exhausting common-source responses into the two represented "
            "targets, a non-EFX state has a different response source or a "
            "common-source response into d"
        ),
        "claim_boundary": (
            "signed conservation/edge identity and finite monotone termination; "
            "observer-response conversion after a different source appears remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "records_checked": result["records_checked"]
    }, indent=2))


if __name__ == "__main__":
    main()
