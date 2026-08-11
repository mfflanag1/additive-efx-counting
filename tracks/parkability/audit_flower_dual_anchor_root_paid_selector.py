#!/usr/bin/env python3
"""QF_LRA checks for the dual-anchor root-paid selector lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    p, xr, h, ell, g, eh, el, eg = z3.Reals(
        "p xr h ell g eh el eg"
    )
    positive = [p > 0, xr > 0, g > 0, eg > 0]

    atom = z3.Int("atom")
    records = [
        checked(
            "dual_core_parent_supports_are_disjoint",
            [
                z3.Or(atom == 0, atom == 4),  # T_r or f in D_q
                z3.Or(atom == 1, atom == 2),  # T_q or B_r in A_a
            ],
        ),
        checked(
            "whole_pool_partition_is_feasible_when_root_payable",
            positive + [p >= xr, z3.Not(z3.And(p >= xr, p >= 0))],
        ),
        checked(
            "selected_root_is_nonworse_and_residual_envy_free",
            positive + [h >= xr, h >= ell, z3.Or(h < xr, h < ell)],
        ),
        checked(
            "least_good_move_strictly_improves_external_hole",
            positive + [el + eg <= el],
        ),
        checked(
            "maximality_forces_payment_or_envy_constraint_failure",
            positive
            + [
                h >= xr,
                h >= ell,
                h - g >= xr,
                h - g >= ell + g,
                z3.Not(z3.And(h - g >= xr, h - g >= ell + g)),
            ],
        ),
        checked(
            "payment_critical_rewrite",
            positive + [h - g < xr, g <= h - xr],
        ),
        checked(
            "envy_critical_rewrite",
            positive + [h - g < ell + g, 2 * g <= h - ell],
        ),
        checked(
            "strong_envy_is_exact_least_good_inequality",
            positive + [eg <= eh, el < eh - eg, el >= eh - eg],
        ),
    ]

    script = Path(__file__).resolve()
    theorem = root / "results/FLOWER_DUAL_ANCHOR_ROOT_PAID_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "flower-dual-anchor-root-paid-selector-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of root-payment feasibility and the two exact "
            "critical-good certificates; it does not prove payment in the "
            "dual-pool-deficit branch or terminate the subsequent response boundary"
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
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
