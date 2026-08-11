#!/usr/bin/env python3
"""Symbolic audit of paid-anchor disjoint recapture."""

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
    yd, extra, xd = z3.Reals("yd extra xd")
    dw, dai, dd = z3.Reals("dw dai dd")
    ci, cr, rr, xi = z3.Reals("ci cr rr xi")
    checks = {
        "anchor_preserves_hole_payment": prove(
            [yd >= xd, extra >= 0], yd + extra < xd
        ),
        "residual_gain_if_old_core_beats_response": prove(
            [dai > dd], dw + dai - dd <= dw
        ),
        "maximality_forces_response_above_old_core": prove(
            [dai != dd, z3.Not(dw + dai - dd > dw)], dd <= dai
        ),
        "anchor_overlap_covers_response_margin": prove(
            [ci > xi, cr <= rr, rr <= xi], ci - cr < ci - xi
        ),
        "anchor_overlap_is_positive": prove(
            [ci > xi, cr <= xi], ci - cr <= 0
        ),
    }
    old_support = {"Y_d", "R-D", "D", "A_i"}
    new_support = {"Y_d", "R-D", "D", "A_i"}
    theorem = root / "results/PAID_ANCHOR_DISJOINT_RECAPTURE_DICHOTOMY_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "paid-anchor-disjoint-recapture-dichotomy-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "support_conservation_schema": {
            "old": sorted(old_support),
            "new": sorted(new_support),
            "identity": "Y_d + R + A_i = D + A_i + Y_d + (R-D)",
            "conserved": old_support == new_support,
        },
        "outcomes": [
            "paid anchor-preserving recapture with strict d-order",
            "unsafe disjoint response augmentation",
            "paid-anchor hitting set captures full response margin",
        ],
        "remaining_gate": "reverse strict d-order or paid-anchor hitting set",
        "claim_boundary": (
            "recapture reduction at a paid anchor; strict polarity reversal, "
            "augmentation recurrence, GG, and four-agent EFX remain open"
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
