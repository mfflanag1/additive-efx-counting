#!/usr/bin/env python3
"""Exact audit of strict root overpayment sacrifice/equality Hall."""

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


def run(repo: Path) -> dict:
    x, delta, total, transferred, compensation, new_root, price = z3.Reals(
        "x delta total transferred compensation new_root price"
    )
    premises = [
        total == x + delta,
        new_root == total - transferred + compensation,
        transferred > delta,
        price == transferred - delta,
    ]
    margin_identity = prove(
        premises,
        new_root - x == compensation - price,
    )
    strict_equivalence = prove(
        premises,
        (new_root > x) == (compensation > price),
    )
    equality_equivalence = prove(
        premises,
        (new_root == x) == (compensation == price),
    )
    assert margin_identity and strict_equivalence and equality_equivalence

    theorem = repo / "results/STRICT_ROOT_OVERPAYMENT_SACRIFICE_OR_EQUALITY_HALL_LEMMA_20260814.md"
    hall = repo / "results/TWO_CREDITOR_RETIRED_PACKET_SPLIT_OR_HALL_CUT_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "strict-root-overpayment-sacrifice-or-equality-hall-audit-v1",
        "status": "JOINT_HALL_REDUCED_TO_ROOT_DEFICIENCY_OR_EXACT_EQUALITY",
        "root_margin_identity": margin_identity,
        "strict_root_overpayment_equivalence": strict_equivalence,
        "exact_root_payment_equivalence": equality_equivalence,
        "remaining_root_branches": [
            "root_payment_family_empty",
            "all_surviving_root_payments_exact",
        ],
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free strict-root priority sacrifice; exact equality Hall "
            "and full theorem remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "hall_theorem": str(hall.relative_to(repo)),
            "hall_theorem_sha256": sha256(hall),
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

