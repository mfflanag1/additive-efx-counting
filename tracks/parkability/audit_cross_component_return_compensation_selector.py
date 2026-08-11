#!/usr/bin/env python3
"""Symbolic audit of the cross-component return-compensation selector."""

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
    d, ys, sj, sl, yh, bh, hj, hl, omega, omega_star = z3.Reals(
        "d ys sj sl yh bh hj hl omega omega_star"
    )
    mu = d - ys
    sigma = yh - bh
    checks = {
        "observer_floor_equivalence": prove(
            [sigma == yh - bh, hl <= sigma + hj],
            yh + hj - hl < bh,
        ),
        "source_response_equivalence": prove(
            [mu == d - ys, omega == sl - sj, omega > -mu],
            d - sj + sl <= ys,
        ),
        "uncompensated_bridge_specialization": prove(
            [mu > 0, sl == 0, sj < mu], d - sj + sl <= ys
        ),
        "global_maximum_failure_separates_every_pair": prove(
            [omega <= omega_star, omega_star <= -mu, omega == sl - sj],
            sj - sl < mu,
        ),
        "successful_pair_beats_failure_boundary": prove(
            [omega == sl - sj, omega > -mu], sj - sl >= mu
        ),
    }

    # J=D and L=empty always satisfy debt removal and the h-budget when the
    # required floor is no larger than the current paid bundle.
    tau_empty, xh = z3.Reals("tau_empty xh")
    feasibility = {
        "selector_family_nonempty": prove(
            [tau_empty == 0, xh >= 0, yh >= bh, hj >= 0, hl == 0],
            z3.Or(tau_empty > xh, hl > yh - bh + hj),
        )
    }

    script = Path(__file__).resolve()
    theorem = root / "results/CROSS_COMPONENT_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "cross-component-return-compensation-selector-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "feasibility_checks": feasibility,
        "outcomes": [
            "paid two-edge physical component bridge",
            "exact direct-return separator requiring a multi-donor or priority handoff",
        ],
        "remaining_gate": (
            "terminate the multi-donor chain or prove a priority-valid base-floor handoff"
        ),
        "claim_boundary": (
            "two-owner bridge payment selector; observer safety, multi-donor closure, "
            "globally maximal GG, and EFX remain open"
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
