#!/usr/bin/env python3
"""Symbolic audit of the third-owner root-replacement fork."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.Solver()
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    rr, rc, rg, rk, xr = z3.Reals("rr rc rg rk xr")
    bd, bk, bg, xb = z3.Reals("bd bk bg xb")
    aa, ac, ab, xa = z3.Reals("aa ac ab xa")
    delta = xr - (rr - rc)
    mu = bd - xb
    checks = {
        "root_payment_equivalence": prove(
            [rk - rg >= delta], rr - rc - rg + rk < xr
        ),
        "donor_weak_payment_equivalence": prove(
            [mu > 0, bk - bg <= mu], bd - bk + bg < xb
        ),
        "donor_equality_is_accepted": prove(
            [mu > 0, bk - bg == mu], bd - bk + bg != xb
        ),
        "captured_source_restoration": prove(
            [aa > xa, ab >= 0], aa - ac + ab + ac <= xa
        ),
        "full_core_is_root_best": prove(
            [rk <= z3.Real("rd"), rg >= 0, z3.Real("rd") < delta],
            rk - rg >= delta,
        ),
    }

    theorem = root / "results/THIRD_OWNER_ROOT_REPLACEMENT_FORK_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "third-owner-root-replacement-fork-audit-v2",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "alternatives": [
            "aggregate root concentration",
            "surplus-budgeted fork or response augmentation",
            "exact donor-margin blockade",
        ],
        "claim_boundary": (
            "symbolic packet-selector theorem; GG does not yet rule out the "
            "root-concentration or donor-margin certificates"
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
