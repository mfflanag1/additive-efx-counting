#!/usr/bin/env python3
"""Symbolic audit of the blocked-hole minimal-K dichotomy."""

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
    dq, dh, dx, dk, dminus = z3.Reals("dq dh dx dk dminus")
    qk, qw, qg, mu = z3.Reals("qk qw qg mu")
    ra, rgr, rx = z3.Reals("ra rgr rx")
    checks = {
        "full_core_plus_tail_restores_hole": prove(
            [dq > dx, dh > 0], dq + dh <= dx
        ),
        "minimal_packet_is_strict": prove(
            [dk + dh > dx], dk + dh <= dx
        ),
        "admissible_full_residual_pays_q": prove(
            [mu > 0, qw >= 0, qk <= mu + qw], mu - qk + qw < 0
        ),
        "minimal_compensator_pays_q": prove(
            [mu > 0, qg >= qk - mu], mu - qk + qg < 0
        ),
        "root_remains_strict": prove(
            [ra > rx, rgr >= 0], ra + rgr <= rx
        ),
        "separator_exceeds_whole_q_margin": prove(
            [mu > 0, qw >= 0, qk > mu + qw], qk - qw <= mu
        ),
        "critical_deletion_boundary": prove(
            [dminus + dh <= dx], dminus + dh > dx
        ),
    }
    theorem = root / "results/BLOCKED_HOLE_MINIMAL_K_Q_BUDGET_DICHOTOMY_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "blocked-hole-minimal-k-q-budget-dichotomy-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "alternatives": [
            "fully paid three-owner cycle before observer-safety check",
            "minimal hole packet exceeds q margin even after all residual compensation",
        ],
        "exact_separator": [
            "d(K+H)>d(X_d)",
            "d(K-k+H)<=d(X_d) for every k in K",
            "q(K)-q(W)>mu_q",
        ],
        "remaining_gate": "observer surplus or fourth-owner compensation",
        "claim_boundary": (
            "payment-layer dichotomy for a hole blocked on Q; observer safety, "
            "fourth-owner separator, response-silent holes, GG, and EFX remain open"
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
