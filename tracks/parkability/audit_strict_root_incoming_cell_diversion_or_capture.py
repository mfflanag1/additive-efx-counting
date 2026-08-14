#!/usr/bin/env python3
"""Independent finite-graph/QF_LRA audit of incoming-cell diversion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "j")
SUPPLIERS = (*OWNERS, "charity")


def possible_edges():
    return tuple(
        (supplier, recipient)
        for supplier in SUPPLIERS
        for recipient in OWNERS
        if supplier != recipient
    )


def graph_audit():
    universe = possible_edges()
    records = []
    checked_graphs = 0
    for supplier in ("q", "d", "j", "charity"):
        incoming = (supplier, "r")
        for recipient in ("q", "d", "j"):
            other = tuple(edge for edge in universe if edge != incoming)
            recorded_size_three = False
            for size in range(4):
                for subset in itertools.combinations(other, size):
                    before = set(subset) | {incoming}
                    after = before - {incoming}
                    if supplier != recipient:
                        after.add((supplier, recipient))
                    assert len(before) <= 4
                    assert len(after) <= len(before)
                    checked_graphs += 1
                    if size == 0 or (size == 3 and not recorded_size_three):
                        records.append({
                            "supplier": supplier,
                            "recipient": recipient,
                            "before": [list(edge) for edge in sorted(before)],
                            "after": [list(edge) for edge in sorted(after)],
                            "before_count": len(before),
                            "after_count": len(after),
                        })
                        if size == 3:
                            recorded_size_three = True
    assert checked_graphs > 1000
    return checked_graphs, records


def algebra_audit():
    current, base, cell, final = z3.Reals("current base cell final")
    margin = current - base
    solver = z3.SolverFor("QF_LRA")
    solver.add(current > base, final == current - cell,
               cell < margin, final <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(current > base, final == current - cell,
               final > base, cell >= margin)
    reverse = solver.check() == z3.unsat

    old_j, gain, new_j = z3.Reals("old_j gain new_j")
    solver = z3.SolverFor("QF_LRA")
    solver.add(gain > 0, new_j == old_j + gain, new_j <= old_j)
    recipient_strict = solver.check() == z3.unsat
    assert forward and reverse and recipient_strict
    return forward and reverse, recipient_strict


def run(root: Path):
    checked_graphs, records = graph_audit()
    root_equivalence, recipient_strict = algebra_audit()
    script = Path(__file__).resolve()
    theorem = root / "results" / (
        "STRICT_ROOT_INCOMING_CELL_DIVERSION_OR_CAPTURE_LEMMA_20260814.md"
    )
    return {
        "schema": "strict-root-incoming-cell-diversion-or-capture-v1",
        "status": "NONINCREASING_EDGE_PROBE_OR_CELL_CAPTURE",
        "checked_graph_count": checked_graphs,
        "maximum_before_edges": 4,
        "maximum_after_edges": 4,
        "edge_count_never_increases": True,
        "root_payment_equivalence": root_equivalence,
        "recipient_strict": recipient_strict,
        "boundary_records": records,
        "claim_boundary": (
            "cap-free incoming-cell topology/payment theorem; simultaneous "
            "capture and root-origin recurrence remain open"
        ),
        "provenance": {
            "z3": z3.get_version_string(),
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
        "status": result["status"],
        "checked_graphs": result["checked_graph_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
