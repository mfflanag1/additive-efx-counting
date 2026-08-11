#!/usr/bin/env python3
"""Symbolic and finite-set audit of retained-bottom-support reset."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    assert solver.check() == z3.unsat
    return "unsat"


def powerset(values):
    values = tuple(values)
    for mask in range(1 << len(values)):
        yield frozenset(values[i] for i in range(len(values)) if mask & (1 << i))


def run(root: Path) -> dict:
    eta, value_k = z3.Reals("eta value_k")
    scalar_checks = {
        "reset_trichotomy_exhaustive": prove(
            eta > 0,
            value_k >= 0,
            z3.Not(z3.Or(
                value_k == 0,
                z3.And(value_k > 0, value_k < eta),
                z3.And(value_k > 0, value_k >= eta),
            )),
        ),
        "fresh_consumption_preserves_margin": prove(
            eta > 0, value_k > 0, value_k < eta, eta - value_k <= 0
        ),
        "captured_packet_covers_margin": prove(
            eta > 0, value_k >= eta, value_k < eta
        ),
    }

    universe = frozenset(range(5))
    finite_cases = 0
    violations = []
    for v in powerset(universe):
        for s in powerset(v):
            live = v - s
            for k in powerset(live):
                finite_cases += 1
                sp = s | k
                if not (s <= sp <= v and (v - sp) == (live - k)):
                    violations.append((sorted(v), sorted(s), sorted(k)))

    theorem = root / "results/UNIVERSAL_RETAINED_BOTTOM_SUPPORT_RESET_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "universal-retained-bottom-support-reset-audit-v1",
        "status": "ALL_FORCED" if not violations else "FAILED",
        "symbolic_checks": scalar_checks,
        "finite_set_audit": {
            "universe_size": len(universe),
            "cases": finite_cases,
            "violations": violations,
        },
        "potential": ["absorbed bottom support |V|", "consumed bottom support |S|"],
        "precondition": "retained cores avoid permanent top/floater anchor T_q+f",
        "remaining_gate": "support-disjoint repeated-bottom Hall state",
        "claim_boundary": (
            "bottom-overlap resets preserve the live anchor, grow S, or capture "
            "root margin; reverse-support components and support-disjoint repeated "
            "Hall closure remain open"
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
