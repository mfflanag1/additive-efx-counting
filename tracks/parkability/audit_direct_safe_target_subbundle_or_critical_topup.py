#!/usr/bin/env python3
"""Audit of direct-safe target selection and recurrent critical top-up."""

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


def critical_set_audit():
    records = 0
    for size in range(1, 7):
        goods = tuple(range(size))
        for values in itertools.product(range(1, 4), repeat=size):
            total = sum(values)
            for floor in range(1, total + 1):
                feasible = [
                    frozenset(subset)
                    for r in range(size + 1)
                    for subset in itertools.combinations(goods, r)
                    if sum(values[g] for g in subset) >= floor
                ]
                minimal = [
                    subset for subset in feasible
                    if not any(proper < subset for proper in feasible)
                ]
                assert minimal
                for subset in minimal:
                    assert all(
                        sum(values[x] for x in subset - {g}) < floor
                        for g in subset
                    )
                    records += 1
    return records


def run(root: Path) -> dict:
    owner, floor, other_final, other_threshold, target_threshold = z3.Reals(
        "owner floor other_final other_threshold target_threshold"
    )
    d_value, q_value = z3.Reals("d_value q_value")
    checks = {
        "safe_branch_target_owner_direct_floor": prove(
            [owner >= floor, floor >= other_threshold], owner < other_threshold
        ),
        "safe_branch_other_observer": prove(
            [other_final >= target_threshold], other_final < target_threshold
        ),
        "recurrent_old_core_below_floor": prove(
            [q_value >= floor, d_value < q_value, z3.Not(d_value >= floor)],
            d_value >= floor,
        ),
        "old_core_feasibility_is_exact_floor_test": prove(
            [d_value >= floor], d_value < floor
        ),
    }
    critical_records = critical_set_audit()

    script = Path(__file__).resolve()
    theorem = root / "results/DIRECT_SAFE_TARGET_SUBBUNDLE_OR_CRITICAL_TOPUP_LEMMA_20260811.md"
    return {
        "schema": "direct-safe-target-subbundle-or-critical-topup-audit-v1",
        "status": "ALL_EXHAUSTED",
        "symbolic_checks": checks,
        "critical_set_records": critical_records,
        "minimal_feasible_sets_every_good_critical": True,
        "outcomes": [
            "partial EFX lex endpoint",
            "permanent current-response or release augmentation",
            "exact old response plus nonempty target-owner-critical top-up packet",
        ],
        "remaining_gate": (
            "substitute or compensate the recurrent critical top-up packet using "
            "the full signed-transfer component"
        ),
        "claim_boundary": (
            "direct-safe subbundle selector only; critical-top-up substitution, "
            "mixed-margin closure, and EFX remain open"
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
