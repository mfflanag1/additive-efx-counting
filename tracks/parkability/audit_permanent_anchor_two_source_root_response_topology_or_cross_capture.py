#!/usr/bin/env python3
"""Audit two-source permanent-anchor response topology and cross capture."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


NONROOT = ("q", "d", "s")


def edge_set(pair, yr_holders, a_holders):
    edges = {("charity", "r")}
    for holder in yr_holders:
        if holder != "r":
            edges.add(("r", holder))
    for holder in a_holders:
        if holder != "q":
            edges.add(("q", holder))
    return edges


def topology_audit():
    rows = []
    for pair in itertools.combinations(NONROOT, 2):
        holders = ("r", *pair)
        presence = tuple(
            frozenset(holder for holder, bit in zip(holders, bits) if bit)
            for bits in itertools.product((0, 1), repeat=3)
            if any(bits)
        )
        for yr_holders, a_holders in itertools.product(presence, repeat=2):
            if any(source not in yr_holders | a_holders for source in pair):
                continue
            before = edge_set(pair, yr_holders, a_holders)
            returned_anchor_holders = a_holders - {"r"}
            after_return = edge_set(pair, yr_holders, returned_anchor_holders)
            cross = (
                set(pair) == {"d", "s"}
                and all(source in yr_holders and source in a_holders
                        for source in pair)
            )
            assert (len(after_return) > 4) == cross

            pure_repaired_max = None
            if cross:
                repaired_counts = []
                for pure_source in pair:
                    other = next(source for source in pair if source != pure_source)
                    for pure_supplier in ("r", "q"):
                        repaired = {("charity", "r")}
                        repaired.add((pure_supplier, pure_source))
                        repaired.add(("r", other))
                        repaired.add(("q", other))
                        repaired = {
                            edge for edge in repaired if edge[0] != edge[1]
                        }
                        repaired_counts.append(len(repaired))
                pure_repaired_max = max(repaired_counts)
                assert pure_repaired_max <= 4

            rows.append({
                "sources": list(pair),
                "yr_holders": sorted(yr_holders),
                "anchor_holders": sorted(a_holders),
                "initial_edge_count": len(before),
                "after_anchor_return_edge_count": len(after_return),
                "initial_four_edge_feasible": len(before) <= 4,
                "irreducible_cross": cross,
                "pure_cell_repaired_maximum": pure_repaired_max,
            })
    assert len(rows) == 96
    assert sum(row["initial_four_edge_feasible"] for row in rows) == 76
    assert sum(not row["initial_four_edge_feasible"] for row in rows) == 20
    assert sum(row["irreducible_cross"] for row in rows) == 4
    return rows


def algebra_audit():
    br, xr, moved, pr, final = z3.Reals("br xr moved pr final")
    delta = br - xr
    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, final == br - moved + pr,
               moved < delta + pr, final <= xr)
    root_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, final == br - moved + pr,
               final > xr, moved >= delta + pr)
    root_reverse = solver.check() == z3.unsat

    rpart, qpart, floor, full, margin = z3.Reals(
        "rpart qpart floor full margin"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(full == rpart + qpart, margin == full - floor,
               rpart <= floor, qpart < margin)
    q_capture = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(full == rpart + qpart, margin == full - floor,
               qpart <= floor, rpart < margin)
    r_capture = solver.check() == z3.unsat

    assert root_forward and root_reverse and q_capture and r_capture
    return {
        "root_payment_equivalence": root_forward and root_reverse,
        "two_supplier_capture": q_capture and r_capture,
    }


def run(root: Path):
    rows = topology_audit()
    checks = algebra_audit()
    script = Path(__file__).resolve()
    theorem = root / "results" / (
        "PERMANENT_ANCHOR_TWO_SOURCE_ROOT_RESPONSE_TOPOLOGY_OR_"
        "CROSS_CAPTURE_LEMMA_20260814.md"
    )
    return {
        "schema": "permanent-anchor-two-source-root-response-topology-v1",
        "status": "FOUR_EDGE_PAIR_OR_ROOT_OR_CROSS_CAPTURE",
        "case_count": len(rows),
        "initial_four_edge_case_count": sum(
            row["initial_four_edge_feasible"] for row in rows
        ),
        "initial_overflow_case_count": sum(
            not row["initial_four_edge_feasible"] for row in rows
        ),
        "irreducible_cross_case_count": sum(
            row["irreducible_cross"] for row in rows
        ),
        **checks,
        "cases": rows,
        "claim_boundary": (
            "cap-free two-source topology theorem conditional on common-state "
            "disjoint responses; cross-state transport/capture remain open"
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
        "cases": result["case_count"],
        "initial_four_edge_cases": result["initial_four_edge_case_count"],
        "initial_overflow_cases": result["initial_overflow_case_count"],
        "irreducible_cross_cases": result["irreducible_cross_case_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
