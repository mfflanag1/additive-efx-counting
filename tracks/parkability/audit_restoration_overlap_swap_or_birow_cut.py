#!/usr/bin/env python3
"""Exact arithmetic audit for the restoration-overlap swap lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict[str, object]:
    x, delta, sp, sm, u, mu, topup, slack = z3.Reals(
        "x delta sp sm u mu topup slack"
    )
    v, j, root_new, recipient_margin = z3.Reals(
        "v j root_new recipient_margin"
    )
    premises = [
        delta > 0,
        sp == sm + delta,
        u - mu > 0,
        slack == topup - (u - mu),
        slack >= 0,
        j > 0,
        root_new == x - j + v,
        recipient_margin == slack - v,
    ]
    root_margin = prove(premises, root_new - x == v - j)
    recipient_identity = prove(premises, recipient_margin == slack - v)
    feasible_if = prove(
        premises + [v <= slack, v >= j],
        recipient_margin >= 0,
    )
    root_weak_if = prove(
        premises + [v <= slack, v >= j],
        root_new >= x,
    )
    crossing_packet_too_expensive = prove(
        premises + [z3.Implies(v <= slack, v < j), v >= j],
        v > slack,
    )
    assert all([
        root_margin,
        recipient_identity,
        feasible_if,
        root_weak_if,
        crossing_packet_too_expensive,
    ])

    theorem = repo / "results/RESTORATION_OVERLAP_SWAP_OR_BIROW_CUT_LEMMA_20260814.md"
    base = repo / "results/NONDEGENERATE_ROOT_EQUALITY_BASE_RESTORATION_LEMMA_20260814.md"
    strict = repo / "results/STRICT_ROOT_OVERPAYMENT_SACRIFICE_OR_EQUALITY_HALL_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "restoration-overlap-swap-or-birow-cut-audit-v1",
        "status": "PURE_OVERLAP_REDUCED_TO_STRICT_ROOT_OR_BIROW_CUT",
        "root_margin_identity": root_margin,
        "recipient_margin_identity": recipient_identity,
        "recipient_floor_under_swap": feasible_if,
        "root_floor_under_swap": root_weak_if,
        "proper_root_crossing_too_expensive_in_surviving_cut": (
            crossing_packet_too_expensive
        ),
        "remaining_root_branches": [
            "root_payment_deficiency",
            "supplier_mode_incompatibility",
            "restoration_overlap_birow_cut",
        ],
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "base_restoration_dependency": str(base.relative_to(repo)),
            "base_restoration_dependency_sha256": sha256(base),
            "strict_root_dependency": str(strict.relative_to(repo)),
            "strict_root_dependency_sha256": sha256(strict),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "remaining_root_branches": result["remaining_root_branches"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
