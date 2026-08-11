#!/usr/bin/env python3
"""Symbolic and finite-set audit of paid-anchor support reset."""

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


def powerset(values):
    values = tuple(values)
    for mask in range(1 << len(values)):
        yield frozenset(values[index] for index in range(len(values)) if mask & (1 << index))


def run(root: Path) -> dict:
    eta, vk = z3.Reals("eta vk")
    checks = {
        "reset_trichotomy_exhaustive": prove(
            [eta >= 0, vk >= 0],
            z3.Not(z3.Or(vk == 0, z3.And(vk > 0, vk <= eta), vk > eta)),
        ),
        "paid_branch_preserves_payment": prove(
            [eta >= 0, vk <= eta], eta - vk < 0
        ),
        "captured_branch_exhausts_margin": prove(
            [eta >= 0, vk > eta], vk <= eta
        ),
    }

    universe = frozenset(range(6))
    cases = 0
    violations = []
    for consumed in powerset(universe):
        live = universe - consumed
        for overlap in powerset(live):
            cases += 1
            updated = consumed | overlap
            if not (consumed <= updated <= universe and universe - updated == live - overlap):
                violations.append((sorted(consumed), sorted(overlap)))

    theorem = root / "results/UNIVERSAL_PAID_ANCHOR_SUPPORT_RESET_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "universal-paid-anchor-support-reset-audit-v1",
        "status": "ALL_FORCED" if not violations else "FAILED",
        "symbolic_checks": checks,
        "finite_set_audit": {
            "universe_size": len(universe),
            "cases": cases,
            "violations": violations,
        },
        "outcomes": [
            "preserved paid anchor",
            "strict consumed-support growth with hole paid",
            "captured hole-payment margin",
        ],
        "remaining_gate": "sacrificed-owner continuation after captured margin",
        "claim_boundary": (
            "paid-anchor reset monotonicity; released-core component, captured-margin "
            "termination, anchor changes, GG, and EFX remain open"
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
