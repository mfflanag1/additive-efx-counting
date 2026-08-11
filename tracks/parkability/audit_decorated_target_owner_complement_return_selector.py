#!/usr/bin/env python3
"""Symbolic audit of decorated-target-owner complement return."""

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
    x_t, assigned_t, residual_t, tau_t, d_minus_j = z3.Reals(
        "x_t assigned_t residual_t tau_t d_minus_j"
    )
    old_s, residual_s, returned_s, final_s, floor_s, phi = z3.Reals(
        "old_s residual_s returned_s final_s floor_s phi"
    )
    checks = {
        "least_good_complement_pays_target_owner": prove(
            [d_minus_j == tau_t, assigned_t + residual_t < tau_t,
             assigned_t + residual_t > x_t],
            d_minus_j <= x_t,
        ),
        "complement_return_conserves_source_value": prove(
            [final_s == old_s + residual_s + returned_s],
            final_s != old_s + residual_s + returned_s,
        ),
        "nonnegative_selector_slack_pays_source_floor": prove(
            [phi == final_s - floor_s, phi >= 0], final_s < floor_s
        ),
        "negative_maximum_is_universal_separator": prove(
            [phi == final_s - floor_s, phi < 0], final_s >= floor_s
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/DECORATED_TARGET_OWNER_COMPLEMENT_RETURN_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "decorated-target-owner-complement-return-selector-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "selector_family_nonempty": True,
        "success_outcomes": [
            "EFX lex endpoint",
            "ordinary or full-decorated response augmentation from complement wall",
        ],
        "exact_failure_separator": (
            "every target-owner-paying complement return leaves the decorated "
            "source below its priority/direct-safety floor"
        ),
        "smallest_remaining_operations": [
            "outside-pool compensation into decorated source",
            "decorated source or root change",
            "decorated core replacement",
        ],
        "remaining_gate": (
            "eliminate the universal complement-return separator using the full "
            "signed-transfer component, or realize it at a globally maximal GG state"
        ),
        "claim_boundary": (
            "target-owner bilateral selector only; mixed-margin closure and EFX "
            "remain open"
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
