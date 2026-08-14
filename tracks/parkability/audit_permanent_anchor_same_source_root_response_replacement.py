#!/usr/bin/env python3
"""Audit same-source replacement at a permanent-anchor bilateral probe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


OWNERS = ("q", "d", "s")
F_Q_STATES = ("empty", "proper", "all")


def topology_audit():
    rows = []
    for source in OWNERS:
        for f_r in (False, True):
            for f_q_state in F_Q_STATES:
                if not f_r and f_q_state == "empty":
                    continue
                for d_nonempty in (False, True):
                    edges = {("charity", "r")}
                    if f_q_state != "all" or (source == "q" and d_nonempty):
                        edges.add(("q", "r"))
                    if f_r:
                        edges.add(("r", source))
                    if f_q_state != "empty" and source != "q":
                        edges.add(("q", source))
                    if d_nonempty and source != "q":
                        edges.add((source, "r"))

                    overflow = (
                        source != "q" and d_nonempty and f_r
                        and f_q_state == "proper"
                    )
                    assert (len(edges) == 5) == overflow

                    completed_edges = set(edges)
                    if overflow:
                        # Completing the anchor removes q->r while q->source
                        # is already active.
                        completed_edges.remove(("q", "r"))
                    assert len(completed_edges) <= 4
                    rows.append({
                        "source": source,
                        "f_r_nonempty": f_r,
                        "f_q_state": f_q_state,
                        "d_nonempty": d_nonempty,
                        "edge_count": len(edges),
                        "overflow": overflow,
                        "anchor_completed_edge_count": len(completed_edges),
                    })
    assert len(rows) == 30
    assert sum(row["overflow"] for row in rows) == 2
    assert max(row["anchor_completed_edge_count"] for row in rows) == 4
    return rows


def algebra_audit():
    bi_minus_d, h, d, f = z3.Reals("bi_minus_d h d f")
    current_i = bi_minus_d + h
    next_i = bi_minus_d + f
    premises = [bi_minus_d >= 0, h > d, f > current_i]

    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, f <= d)
    response_implies_admissible = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, next_i <= current_i)
    strict_source_progress = solver.check() == z3.unsat

    br, xr, packet, dr, pr = z3.Reals("br xr packet dr pr")
    delta = br - xr
    final_r = br - packet + dr + pr
    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, final_r > xr,
               packet - dr >= delta + pr)
    root_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, packet - dr < delta + pr,
               final_r <= xr)
    root_reverse = solver.check() == z3.unsat

    assert all((response_implies_admissible, strict_source_progress,
                root_forward, root_reverse))
    return {
        "response_implies_admissible": response_implies_admissible,
        "strict_same_source_progress": strict_source_progress,
        "root_payment_equivalence": root_forward and root_reverse,
    }


def run(root: Path):
    rows = topology_audit()
    checks = algebra_audit()
    script = Path(__file__).resolve()
    theorem = root / "results" / (
        "PERMANENT_ANCHOR_SAME_SOURCE_ROOT_RESPONSE_REPLACEMENT_LEMMA_20260814.md"
    )
    return {
        "schema": "permanent-anchor-same-source-root-response-replacement-v1",
        "status": "SAME_SOURCE_PROGRESS_OR_TYPED_ROOT_CAPTURE",
        "case_count": len(rows),
        "overflow_case_count": sum(row["overflow"] for row in rows),
        "maximum_repaired_edge_count": max(
            row["anchor_completed_edge_count"] for row in rows
        ),
        **checks,
        "cases": rows,
        "claim_boundary": (
            "same-source residual response closed to progress/capture; "
            "different-source and capture branches remain open"
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
        "overflow_cases": result["overflow_case_count"],
        "maximum_repaired_edges": result["maximum_repaired_edge_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
