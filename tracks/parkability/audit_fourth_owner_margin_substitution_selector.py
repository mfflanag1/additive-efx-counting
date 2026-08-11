#!/usr/bin/env python3
"""Symbolic audit of fourth-owner margin substitution."""

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
    qk, qj, qw, muq, theta = z3.Reals("qk qj qw muq theta")
    de, dj, dl, nu = z3.Reals("de dj dl nu")
    se, sl, xs, mus = z3.Reals("se sl xs mus")
    ra, rg, xr = z3.Reals("ra rg xr")
    other_j, other_l = z3.Reals("other_j other_l")
    checks = {
        "q_cover_family_nonempty": prove(
            [muq > 0, qw >= 0, theta == qk - muq - qw, theta > 0],
            qk < theta,
        ),
        "returned_J_makes_remaining_K_admissible": prove(
            [theta == qk - muq - qw, qj >= theta],
            qk - qj > muq + qw,
        ),
        "hole_payment_after_substitution": prove(
            [nu > 0, nu + dl - dj > 0], nu - dj + dl <= 0
        ),
        "fourth_owner_weak_payment": prove(
            [mus == se - xs, sl <= mus], se - sl < xs
        ),
        "root_strict_payment": prove(
            [ra > xr, rg >= 0], ra + rg <= xr
        ),
        "extremal_failure_is_global": prove(
            [dj <= other_j, dl >= other_l, dj - dl >= nu],
            other_j - other_l < nu,
        ),
    }
    theorem = root / "results/FOURTH_OWNER_MARGIN_SUBSTITUTION_SELECTOR_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "fourth-owner-margin-substitution-selector-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "selectors": {
            "J_star": "minimize d(J) subject to q(J)>=theta_q",
            "L_star": "maximize d(L) subject to s(L)<=mu_s",
        },
        "success_test": "nu_d + d(L_star) - d(J_star) > 0",
        "exact_failure": "d(J)-d(L)>=nu_d for every q-sufficient J and s-affordable L",
        "remaining_operation": "compensate fourth owner or augment response relation",
        "claim_boundary": (
            "exact uncompensated fourth-owner selector; compensated donor, "
            "observer safety, response-silent fourth owner, GG, and EFX remain open"
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
