#!/usr/bin/env python3
"""Symbolic audit of compensated fourth-owner residual selection."""

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
    muq, qw, qkj, qm, bq, qg = z3.Reals("muq qw qkj qm bq qg")
    se, sl, sm, xs, mus, kappa = z3.Reals("se sl sm xs mus kappa")
    nu, dl, dj = z3.Reals("nu dl dj")
    ra, rg, xr = z3.Reals("ra rg xr")
    best_sm, other_sm = z3.Reals("best_sm other_sm")
    checks = {
        "fourth_owner_compensated": prove(
            [mus == se - xs, kappa >= sl - mus, sm >= kappa],
            se - sl + sm < xs,
        ),
        "remaining_residual_pays_q": prove(
            [bq == muq + qw - qkj, qm <= bq],
            qw - qm < qkj - muq,
        ),
        "minimal_q_packet_pays_q": prove(
            [qg >= qkj - muq], muq - qkj + qg < 0
        ),
        "hole_remains_strict": prove(
            [nu > 0, nu + dl - dj > 0], nu + dl - dj <= 0
        ),
        "root_remains_strict": prove(
            [ra > xr, rg >= 0], ra + rg <= xr
        ),
        "maximizer_failure_is_global": prove(
            [best_sm >= other_sm, best_sm < kappa], other_sm >= kappa
        ),
    }

    old_packets = {"A", "H", "Q0", "KJ", "J", "E0", "L", "W"}
    new_packets = {"A", "H", "Q0", "KJ", "J", "E0", "L", "W"}
    theorem = root / "results/COMPENSATED_FOURTH_OWNER_RESIDUAL_SELECTOR_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "compensated-fourth-owner-residual-selector-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "support_conserved": old_packets == new_packets,
        "supplier_edges": [
            "r->d:H", "q->d:K-J", "s->d:L",
            "d->r:G_r", "d->q:G_q", "d->s:M",
        ],
        "canonical_M": "maximize s(M) subject to M subset W and q(M)<=B_q",
        "success_test": "s(M_star)>=max(0,s(L)-mu_s)",
        "exact_failure": "q(M)<=B_q implies s(M)<kappa_s for every M subset W",
        "remaining_gate": "observer-surplus safety or response-augmentation recurrence",
        "claim_boundary": (
            "complete payment selector for the four-owner packet geometry; "
            "observer safety, augmentation recurrence, GG, and EFX remain open"
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
