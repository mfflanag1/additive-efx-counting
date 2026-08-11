#!/usr/bin/env python3
"""Symbolic audit of the canonical q-budget split in the bottom-tail splice."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    ra, rgr, rx = z3.Reals("ra rgr rx")
    qk, qg, qw, mu = z3.Reals("qk qg qw mu")
    checks = {
        "root_payment_automatic": prove(
            [ra > rx, rgr >= 0], ra + rgr <= rx
        ),
        "root_surplus_identity_positive": prove(
            [ra > rx, rgr >= 0], (ra - rx) + rgr <= 0
        ),
        "q_payment_equivalence_forward": prove(
            [mu > 0, qg >= qk - mu], mu - qk + qg < 0
        ),
        "q_payment_equivalence_reverse": prove(
            [mu > 0, mu - qk + qg >= 0], qg < qk - mu
        ),
        "full_residual_suffices_when_admissible": prove(
            [mu > 0, qw >= 0, qk <= mu + qw], qw < qk - mu
        ),
        "compensation_impossible_when_inadmissible": prove(
            [mu > 0, qw >= 0, qg >= 0, qg <= qw, qk > mu + qw],
            qg >= qk - mu,
        ),
        "inadmissible_packet_captures_margin": prove(
            [mu > 0, qw >= 0, qk > mu + qw], qk <= mu
        ),
    }
    theorem = root / "results/BOTTOM_TAIL_Q_BUDGET_CANONICAL_SPLIT_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "bottom-tail-q-budget-canonical-split-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "canonical_split": (
            "choose inclusion-minimal G_q subset W with q(G_q) >= q(K)-mu_q; "
            "set G_r=W-G_q"
        ),
        "exact_admissibility": "q(K) <= mu_q + q(W)",
        "exact_failure": "q(K)-q(W) > mu_q",
        "remaining_gate": "hole-safe admissible K and observer-surplus budgets",
        "claim_boundary": (
            "root payment and q compensation are exact; hole-safe K existence, "
            "observer safety, fourth-owner separation, GG, and four-agent EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
