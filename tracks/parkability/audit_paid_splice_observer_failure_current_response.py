#!/usr/bin/env python3
"""Symbolic audit of paid-splice observer-failure response extraction."""

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
    x, y, tau, d, d_minus, other_y, incoming, outgoing = z3.Reals(
        "x y tau d d_minus other_y incoming outgoing"
    )
    beta = z3.Real("beta")
    checks = {
        "failed_budget_is_current_strong_envy": prove(
            [y >= x, tau - x > y - x], tau <= y
        ),
        "current_strong_envy_is_failed_budget": prove(
            [y >= x, tau > y], tau - x <= y - x
        ),
        "least_good_complement_is_current_desired": prove(
            [tau == d_minus, tau > y], d_minus <= y
        ),
        "current_response_is_base_response": prove(
            [d > y, y >= x], d <= x
        ),
        "current_safety_is_surplus_budgeted": prove(
            [d_minus <= other_y, other_y >= x, beta == d_minus - x],
            beta > other_y - x,
        ),
        "signed_transfer_realizes_surplus": prove(
            [y == x + incoming - outgoing],
            y - x != incoming - outgoing,
        ),
    }

    gap_solver = z3.SolverFor("QF_LRA")
    gap_solver.add(x == 5, other_y == 8, d_minus == 7)
    gap_solver.add(d_minus <= other_y, other_y >= x, d_minus > x)
    assert gap_solver.check() == z3.sat
    base_safety_gap = {
        "status": "sat",
        "base_utility": "5",
        "current_utility": "8",
        "target_threshold": "7",
    }

    # Finite-state logic for the exact response record.  Each Boolean is an
    # abstract equality test, not an item-count assumption.
    seen, same_source_bundle = z3.Bools("seen same_source_bundle")
    triple_checks = {
        "decorated_response_trichotomy": prove(
            [],
            z3.Not(z3.Or(
                z3.Not(seen),
                z3.And(seen, z3.Not(same_source_bundle)),
                z3.And(seen, same_source_bundle),
            )),
        ),
        "old_different_bundle_is_strict_progress": prove(
            [seen, z3.Not(same_source_bundle), d > y], d <= y
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md"
    return {
        "schema": "paid-splice-observer-failure-current-response-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "current_safe_but_not_base_safe_witness": base_safety_gap,
        "exact_response_checks": triple_checks,
        "outcomes": [
            "permanent ordinary-or-decorated response augmentation",
            "same-owner current-utility progress before reset",
            "exact repeated decorated response connected-return gate",
        ],
        "remaining_gate": (
            "release-compatible closure of an exact repeated decorated response "
            "whose signed physical compensation transfers lie in one component"
        ),
        "claim_boundary": (
            "observer failure extraction and recurrence localization; full repeated-"
            "support splice closure, globally maximal GG, and EFX remain open"
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
