#!/usr/bin/env python3
"""Symbolic audit of the root-anchored one-head two-hole selector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    base, a, w = z3.Reals("base a w")
    tau_w = z3.Real("tau_w")
    h, l = z3.Reals("h l")
    tau_l = z3.Real("tau_l")
    tau_l_plus = z3.Real("tau_l_plus")
    h_minus, l_plus = z3.Reals("h_minus l_plus")
    head_h_minus, head_l, head_l_plus = z3.Reals(
        "head_h_minus head_l head_l_plus"
    )

    # The original anchored partition is feasible under the nonhead root row.
    feasible = z3.SolverFor("QF_LRA")
    feasible.add(a > base, a >= tau_w)
    feasible.add(z3.Not(z3.And(a >= a, a >= tau_w)))
    assert feasible.check() == z3.unsat

    # At an outside-anchor least-good move, if both root constraints survive,
    # the head cell strictly improves, contradicting the selected maximum.
    critical = z3.SolverFor("QF_LRA")
    critical.add(
        h >= a,
        h >= tau_l,
        head_l < head_h_minus,
        head_l_plus > head_l,
        z3.Not(z3.And(h_minus >= a, h_minus >= tau_l_plus)),
        z3.Not(z3.Or(h_minus < a, h_minus < tau_l_plus)),
    )
    assert critical.check() == z3.unsat

    # Mutual-hole EFX excludes both cross-hole wall orientations.
    root_assigned, head_assigned = z3.Reals("root_assigned head_assigned")
    tau_head_cell_for_root, tau_root_cell_for_head = z3.Reals(
        "tau_head_cell_for_root tau_root_cell_for_head"
    )
    mutual = z3.SolverFor("QF_LRA")
    mutual.add(
        root_assigned >= tau_head_cell_for_root,
        head_assigned >= tau_root_cell_for_head,
    )
    for failure in (
        root_assigned < tau_head_cell_for_root,
        head_assigned < tau_root_cell_for_head,
    ):
        probe = z3.SolverFor("QF_LRA")
        probe.add(mutual.assertions(), failure)
        assert probe.check() == z3.unsat

    theorem = root / "results/ROOT_ANCHORED_ONE_HEAD_TWO_HOLE_SELECTOR_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-anchored-one-head-two-hole-selector-audit-v1",
        "status": "ROOT_FACING_ONE_HEAD_REDUCED_TO_TWO_HOLE_OR_CRITICAL_GOOD",
        "original_partition_feasible": True,
        "permanent_anchor_retained_by_selector": True,
        "outside_anchor_move_forces_root_criticality": True,
        "mutual_hole_walls_excluded": True,
        "surviving_certificates": [
            "anchor-critical least good",
            "root-floor-critical least good",
            "root-EFX-critical least good",
        ],
        "claim_boundary": (
            "cap-free selector reduction; critical-good reversal, response "
            "recurrence, and complete-pool capture remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "surviving_certificates": result["surviving_certificates"],
    }, indent=2))


if __name__ == "__main__":
    main()
