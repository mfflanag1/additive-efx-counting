#!/usr/bin/env python3
"""Decide the fixed-root dual-mode payment lemma in the length-three atom."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import atomic_json, bundles, integerize_model, subset_sum
    from .run_length_three_global_lex_atomic_cegar import BASE_BUNDLES, structural_solver
except ImportError:
    from run_alternating_global_lex_cegar import atomic_json, bundles, integerize_model, subset_sum
    from run_length_three_global_lex_atomic_cegar import BASE_BUNDLES, structural_solver


SCHEMA = "length-three-dual-mode-atom-v1"
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
P, R, Q, S = range(4)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def efx_failures(values, owner):
    assigned = bundles(owner)
    own = tuple(subset_sum(values, agent, assigned[agent]) for agent in range(4))
    return tuple(
        own[observer]
        < subset_sum(
            values,
            observer,
            tuple(good for good in assigned[target] if good != removed),
        )
        for observer in range(4)
        for target in range(4)
        for removed in assigned[target]
    )


def owner_for(payment, mode):
    owner = [None] * len(GOODS)
    owner[0] = P
    owner[6] = P
    owner[4] = Q
    if mode == "r":
        owner[5] = S
        for good in payment:
            owner[good] = R
    else:
        owner[5] = R
        for good in payment:
            owner[good] = S
    return tuple(owner)


def run(mode):
    solver, values, own = structural_solver(R, mode)
    residual = (1, 2, 3)
    candidates = []
    for size in range(1, len(residual) + 1):
        for payment in itertools.combinations(residual, size):
            for payment_mode, recipient in (("r", R), ("s", S)):
                owner = owner_for(payment, payment_mode)
                candidates.append((payment_mode, payment, owner))
                solver.add(
                    z3.Or(
                        subset_sum(values, recipient, payment) < own[recipient],
                        *efx_failures(values, owner),
                    )
                )
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "structural_mode": mode,
        "candidate_count": len(candidates),
        "status": "FIXED_ROOT_DUAL_MODE_FORCED" if checked == z3.unsat else str(checked).upper(),
        "values": None,
        "candidate_allocations": [
            {
                "mode": payment_mode,
                "payment": [GOODS[good] for good in payment],
                "owner_by_good": list(owner),
            }
            for payment_mode, payment, owner in candidates
        ],
        "claim_boundary": {
            "unsat": "the fixed-root dual-mode disjunction in the seven-good structural atom only",
            "sat": "an exact motif countermodel to that fixed-root disjunction, not to EFX",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parents[2])),
            "script_sha256": sha256(Path(__file__).resolve()),
            "z3_version": z3.get_version_string(),
        },
    }
    if checked == z3.sat:
        result["values"] = [list(row) for row in integerize_model(solver.model(), values)]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("exact", "selected"), default="selected")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.mode)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "structural_mode", "candidate_count")}, indent=2))


if __name__ == "__main__":
    main()
