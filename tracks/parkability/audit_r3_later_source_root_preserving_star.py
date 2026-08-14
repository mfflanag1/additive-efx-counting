#!/usr/bin/env python3
"""Audit the R3 later-source root-preserving star edge/capture frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


CYCLE = {"r": "q", "q": "s", "s": "r"}
LATER_SOURCES = ("q", "s")


def edge_records():
    initial = {(target, source) for source, target in CYCLE.items()}
    rows = []
    for source in LATER_SOURCES:
        targets = {"r", *(set(CYCLE) - {source, "r"})}
        assert len(targets) == 2
        nonroot_target = next(target for target in targets if target != "r")
        for root_incoming in ("none", "partial", "whole"):
            for root_residual_used in (False, True):
                if root_incoming == "none" and not root_residual_used:
                    continue
                for other_residual_used in (False, True):
                    destinations = {supplier: {recipient} for supplier, recipient in initial}

                    # Root response: preserve every unused part of the incoming
                    # root packet.  A proper move therefore keeps the old edge.
                    root_supplier = CYCLE["r"]
                    if root_incoming == "whole":
                        destinations[root_supplier].discard("r")
                    if root_incoming != "none":
                        destinations[root_supplier].add(source)
                    if root_residual_used:
                        destinations.setdefault("r", set()).add(source)

                    # Other star target: complete its incoming packet, deleting
                    # the old matching destination before redirecting/returning.
                    other_supplier = CYCLE[nonroot_target]
                    destinations[other_supplier].discard(nonroot_target)
                    destinations[other_supplier].add(source)
                    if other_residual_used:
                        destinations.setdefault(nonroot_target, set()).add(source)

                    owner_edges = {
                        (supplier, recipient)
                        for supplier, recipients in destinations.items()
                        for recipient in recipients if supplier != recipient
                    }
                    assert len(owner_edges) <= 3
                    final_edges = owner_edges | {("charity", nonroot_target)}
                    assert len(final_edges) <= 4
                    rows.append({
                        "source": source,
                        "root_incoming": root_incoming,
                        "root_residual_used": root_residual_used,
                        "nonroot_target": nonroot_target,
                        "other_residual_used": other_residual_used,
                        "owner_edges": sorted([list(edge) for edge in owner_edges]),
                        "owner_edge_count": len(owner_edges),
                        "total_edge_count": len(final_edges),
                    })
    return rows


def capture_checks():
    anchor, retained, base = z3.Reals("anchor retained base")
    moved = anchor - retained
    assumptions = [anchor > base, retained >= 0, retained <= base]
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(moved >= anchor - base))
    margin_status = str(solver.check())
    assert margin_status == "unsat"

    positive = z3.SolverFor("QF_LRA")
    positive.add(*assumptions, z3.Not(moved > 0))
    positive_status = str(positive.check())
    assert positive_status == "unsat"
    return {
        "full_margin_capture_negation": margin_status,
        "strict_positive_capture_negation": positive_status,
    }


def run(root: Path):
    rows = edge_records()
    assert len(rows) == 20
    assert {row["source"] for row in rows} == set(LATER_SOURCES)
    checks = capture_checks()
    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_LATER_SOURCE_ROOT_PRESERVING_STAR_FRONTIER_LEMMA_20260814.md"
    return {
        "schema": "r3-later-source-root-preserving-star-audit-v1",
        "status": "FOUR_EDGE_OR_FULL_ROOT_MARGIN_CAPTURE",
        "edge_records_checked": len(rows),
        "edge_records": rows,
        "capture_checks": checks,
        "claim_boundary": (
            "exact edge frontier and root-margin dichotomy; conversion of full "
            "anchor capture into PI/full-owner extraction remains open"
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
        "status": result["status"], "checked": result["edge_records_checked"]
    }, indent=2))


if __name__ == "__main__":
    main()
