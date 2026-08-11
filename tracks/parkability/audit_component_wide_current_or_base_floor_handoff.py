#!/usr/bin/env python3
"""Symbolic audit of current/base floors in component-wide compensation."""

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
    d, y, x, omega, omega_star = z3.Reals("d y x omega omega_star")
    mu_cur = d - y
    delta = y - x
    mu_base = d - x
    checks = {
        "base_margin_decomposition": prove(
            [mu_cur == d - y, delta == y - x, mu_base == d - x],
            mu_base != mu_cur + delta,
        ),
        "current_branch_strictly_improves_current": prove(
            [omega > -mu_cur], d + omega <= y
        ),
        "middle_branch_strictly_pays_base": prove(
            [omega > -mu_base, omega <= -mu_cur], d + omega <= x
        ),
        "base_failure_separates_every_partition": prove(
            [omega <= omega_star, omega_star <= -mu_base],
            -omega < mu_base,
        ),
        "interval_trichotomy": prove(
            [d > y, y >= x],
            z3.Not(z3.Or(
                omega > -mu_cur,
                z3.And(omega > -mu_base, omega <= -mu_cur),
                omega <= -mu_base,
            )),
        ),
        "middle_interval_spends_realized_surplus": prove(
            [d > y, y > x, omega > -mu_base, omega <= -mu_cur],
            delta <= 0,
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/COMPONENT_WIDE_CURRENT_OR_BASE_FLOOR_HANDOFF_LEMMA_20260811.md"
    return {
        "schema": "component-wide-current-or-base-floor-handoff-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "outcomes": [
            "strict current-source component bridge",
            "strict base-paid priority-valid component bridge",
            "exact base-margin separator",
        ],
        "remaining_gate": (
            "sacrificed-source direct safety, outside-component recruitment, or "
            "response-core replacement after the base separator"
        ),
        "claim_boundary": (
            "two-floor component selector; final safety, full repeated-support GG, "
            "globally maximal countermodel, and EFX remain open"
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
