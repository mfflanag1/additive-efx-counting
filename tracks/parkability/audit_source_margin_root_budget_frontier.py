#!/usr/bin/env python3
"""Symbolic audit of the source-margin global two-row frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated_conclusion) -> str:
    solver = z3.Solver()
    solver.add(*assumptions, negated_conclusion)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    rp, xr, rc, rb = z3.Reals("rp xr rc rb")
    cr, gr, br, cr2, hr, gr2 = z3.Reals("cr gr br cr2 hr gr2")
    sigma = rp - rb + rc - xr
    paid = [sigma >= 0]
    checks = {
        "root_surplus_identity": prove([rp - rb + rc >= xr], sigma < 0),
        "return_extracted_good_root_change": prove(
            paid + [cr <= sigma], rp - rb + rc - cr < xr
        ),
        "add_unused_pool_good_root_change": prove(
            paid + [gr <= sigma], rp - rb + rc - gr < xr
        ),
        "return_swap_root_change": prove(
            paid + [br >= cr2], rp - rb + rc + br - cr2 < xr
        ),
        "cross_swap_root_change": prove(
            paid + [hr >= gr2], rp - rb + rc + hr - gr2 < xr
        ),
    }

    theorem = root / "results/SOURCE_MARGIN_ROOT_BUDGET_FRONTIER_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "source-margin-root-budget-frontier-audit-v2",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "frontier_certificates": [
            "every extracted boundary good exceeds root slack",
            "every unused pool good exceeds root slack",
            "root-affordable returned-good swap has aligned source order",
            "root-affordable cross-cut swap has aligned source order",
        ],
        "remaining_operation": "third-owner surplus-budgeted connected fork",
        "claim_boundary": (
            "symbolic audit of exchange identities for the cap-free global "
            "two-row selector; it does not force the third-owner fork or GG closure"
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
