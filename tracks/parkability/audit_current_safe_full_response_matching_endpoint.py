#!/usr/bin/env python3
"""Symbolic audit of the current-safe full-response endpoint."""

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
    x, y, own, tau, margin, debt, delta = z3.Reals(
        "x y own tau margin debt delta"
    )
    checks = {
        "current_safe_current_desired_is_efx": prove(
            [own > y, tau <= y], own < tau
        ),
        "paid_current_desired_pareto_dominates_base": prove(
            [y >= x, own > y], own <= x
        ),
        "margin_budget_is_efx_comparison": prove(
            [margin == own - x, debt == tau - x, margin >= debt], own < tau
        ),
        "efx_comparison_is_margin_budget": prove(
            [margin == own - x, debt == tau - x, own >= tau], margin < debt
        ),
        "current_safety_bounds_base_debt": prove(
            [tau <= y, delta == y - x], tau - x > delta
        ),
        "current_desire_margin_exceeds_current_surplus": prove(
            [own > y, margin == own - x, delta == y - x], margin <= delta
        ),
        "failed_budget_is_mixed_separator": prove(
            [margin == own - x, debt == tau - x, tau > own], debt <= margin
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/CURRENT_SAFE_FULL_RESPONSE_MATCHING_ENDPOINT_LEMMA_20260811.md"
    return {
        "schema": "current-safe-full-response-matching-endpoint-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "full_current_matching_endpoint": (
            "four disjoint current-safe current-desired cores form a partial EFX "
            "Pareto improvement"
        ),
        "exact_remaining_separator": (
            "an old assigned core margin is below a current-safe target debt"
        ),
        "remaining_gate": (
            "target-distinct replacement of every underfunded old edge by a "
            "current response, or a release-compatible alternating component"
        ),
        "claim_boundary": (
            "full current-response endpoint and mixed-row separator only; the "
            "universal repeated-support theorem and EFX remain open"
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
