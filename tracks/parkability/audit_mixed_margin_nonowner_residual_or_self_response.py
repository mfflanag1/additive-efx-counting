#!/usr/bin/env python3
"""Symbolic audit of the nonowner residual-or-self-response dichotomy."""

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
    x, assigned, incoming, residual, tau, current = z3.Reals(
        "x assigned incoming residual tau current"
    )
    checks = {
        "released_residual_payment_covers_debt": prove(
            [assigned + residual >= tau], assigned + residual < tau
        ),
        "failed_residual_forces_incoming_core_order": prove(
            [current == incoming + residual, assigned + residual < tau, tau <= current],
            incoming <= assigned,
        ),
        "incoming_core_becomes_base_response": prove(
            [assigned > x, incoming > assigned], incoming <= x
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/MIXED_MARGIN_NONOWNER_RESIDUAL_OR_SELF_RESPONSE_LEMMA_20260811.md"
    return {
        "schema": "mixed-margin-nonowner-residual-or-self-response-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "outcomes": [
            "released own residual pays decorated debt",
            "unsafe enlarged target gives current-response augmentation",
            "old incoming core gives self-response PI, support growth, or augmentation",
        ],
        "excluded_roles": ["decorated target owner", "decorated source"],
        "remaining_gate": "decorated-target-owner complement-return selector",
        "claim_boundary": (
            "nonowner debt only; target-owner payment, mixed-margin closure, and "
            "EFX remain open"
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
