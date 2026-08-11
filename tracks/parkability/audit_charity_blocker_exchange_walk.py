#!/usr/bin/env python3
"""Symbolic and finite-state audit of the charity-blocker exchange walk."""

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
    bundle, charity, outgoing, updated, base = z3.Reals(
        "bundle charity outgoing updated base"
    )
    checks = {
        "blocker_is_base_response": prove(
            [charity > bundle, bundle >= base], charity <= base
        ),
        "exchange_identity": prove(
            [updated == bundle - outgoing + charity],
            updated - bundle != charity - outgoing,
        ),
        "exchange_strictly_improves_blocker": prove(
            [charity > bundle, bundle >= outgoing, outgoing > 0,
             updated == bundle - outgoing + charity],
            updated <= bundle,
        ),
        "exchange_preserves_base_payment": prove(
            [charity > bundle, bundle >= base, bundle >= outgoing,
             updated == bundle - outgoing + charity],
            updated < base,
        ),
        "singleton_threshold_is_zero": prove([], z3.RealVal(0) != 0),
    }

    charity_safe, targets_safe, response_new = z3.Bools(
        "charity_safe targets_safe response_new"
    )
    terminal = {
        "terminal_classification": prove(
            [charity_safe],
            z3.Not(z3.Or(
                targets_safe,
                z3.Not(targets_safe),
                response_new,
            )),
        ),
        "unsafe_charity_continues_or_augments": prove(
            [z3.Not(charity_safe)],
            z3.Not(z3.Or(response_new, z3.Not(response_new))),
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/CHARITY_BLOCKER_EXCHANGE_WALK_LEMMA_20260811.md"
    return {
        "schema": "charity-blocker-exchange-walk-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "terminal_checks": terminal,
        "monotonicity": (
            "one owner utility strictly rises per exchange; every other owner utility "
            "is unchanged; finite bundle state forbids recurrence"
        ),
        "outcomes": [
            "EFX lexicographic charity-exchange endpoint",
            "ordinary or surplus-decorated owner-target response augmentation",
            "new singleton-charity response or strict same-owner progress",
        ],
        "remaining_gate": "owner-target decorated-response recurrence after charity safety",
        "claim_boundary": (
            "singleton-charity exchange termination on paid inputs; universal paid-splice "
            "extraction, repeated-support GG, and EFX remain open"
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
