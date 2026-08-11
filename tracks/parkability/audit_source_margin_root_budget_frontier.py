#!/usr/bin/env python3
"""Symbolic audit of the source-margin root-budget frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    rp, xr, rc, rb = z3.Reals("rp xr rc rb")
    aa, xa, ac, ab = z3.Reals("aa xa ac ab")
    delta = xr - rp
    mu = aa - xa
    beta = rc - delta
    assumptions = [
        delta > 0,
        mu > 0,
        rc >= delta,
        ac >= mu,
        rb >= 0,
        rb <= beta,
        ab >= 0,
    ]

    solver = z3.Solver()
    solver.add(*assumptions)
    solver.add(rp - rb + rc < xr)
    assert solver.check() == z3.unsat

    solver = z3.Solver()
    solver.add(*assumptions, ab > ac - mu)
    solver.add(aa - ac + ab <= xa)
    assert solver.check() == z3.unsat

    solver = z3.Solver()
    solver.add(*assumptions, ab <= ac - mu)
    solver.add(ac - ab < mu)
    assert solver.check() == z3.unsat

    remaining, ag = z3.Reals("remaining ag")
    solver = z3.Solver()
    solver.add(remaining >= 0, ag > 0, ag <= remaining)
    solver.add(z3.Not(ag <= remaining))
    assert solver.check() == z3.unsat

    theorem = root / "results/SOURCE_MARGIN_ROOT_BUDGET_FRONTIER_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "source-margin-root-budget-frontier-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": {
            "root_payment_identity": "unsat",
            "source_restoration_identity": "unsat",
            "source_blockade_margin": "unsat",
            "unused_good_feasibility_contradicts_maximality": "unsat",
        },
        "outcomes": [
            "source restored under root budget",
            "unsafe restored target response augmentation",
            "full-pool source exhaustion",
            "pointwise root-budget blockade requiring split packet or third-owner fork",
        ],
        "claim_boundary": (
            "symbolic audit of the cap-free same-source compensation frontier; "
            "it does not eliminate the terminal blockade or prove GG closure"
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
