#!/usr/bin/env python3
"""Audit paid-anchor consumption by the least-good wall response."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
    ai, ww, least, rr = z3.Reals("ai ww least rr")
    checks = {
        "least_good_complement_current_improvement": prove(
            [ai < ww - least], ww - least <= ai
        ),
        "empty_anchor_intersection_contradiction": prove(
            [ww - least > ai, rr <= ai, ww - least == rr], z3.BoolVal(True)
        ),
    }

    universe = frozenset(range(6))
    support_cases = 0
    violations = []
    for anchor in powerset(universe):
        if not anchor:
            continue
        residual = universe - anchor
        for g in universe:
            complement = universe - {g}
            if not (complement & anchor):
                # Set-theoretically this forces anchor={g} and B=R.
                support_cases += 1
                if anchor != frozenset({g}) or complement != residual:
                    violations.append((sorted(anchor), g))

    theorem = root / "results/PAID_ANCHOR_LEAST_GOOD_CONSUMPTION_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "paid-anchor-least-good-consumption-audit-v1",
        "status": "ALL_FORCED" if not violations else "FAILED",
        "symbolic_checks": checks,
        "finite_support_audit": {
            "universe_size": len(universe),
            "empty_intersection_cases": support_cases,
            "violations": violations,
        },
        "support_identity": "A_i + Y_d + R = (Y_d+R-g) + (A_i+g)",
        "outcomes": [
            "strict consumed paid-anchor support",
            "unsafe response augmentation",
        ],
        "remaining_gate": "connected restoration of consumed anchor support",
        "claim_boundary": (
            "anchor-driven wall conversion; restoration, unpaid sacrificed-owner "
            "continuation, unsafe recurrence, GG, and EFX remain open"
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
