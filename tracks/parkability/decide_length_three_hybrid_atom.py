#!/usr/bin/env python3
"""Falsify the hybrid r-tail/s-base escape family in the exact atom."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_length_three_dual_mode_split import (
        P,
        Q,
        R,
        S,
        efx_failures,
        make_cell,
        structural_solver,
    )
    from .run_alternating_global_lex_cegar import atomic_json, bundles, integerize_model, subset_sum
except ImportError:
    from decide_length_three_dual_mode_split import (
        P,
        Q,
        R,
        S,
        efx_failures,
        make_cell,
        structural_solver,
    )
    from run_alternating_global_lex_cegar import atomic_json, bundles, integerize_model, subset_sum


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_owners(cell, mode):
    fixed_agent = S if mode == "r_tail" else R
    payment_agent = R if mode == "r_tail" else S
    choices = (P, payment_agent, Q, None)
    free_goods = tuple(good for good in range(cell["m"]) if good != cell["y"])
    for assignment in itertools.product(choices, repeat=len(free_goods)):
        owner = [None] * cell["m"]
        owner[cell["y"]] = fixed_agent
        for good, agent in zip(free_goods, assignment):
            owner[good] = agent
        yield tuple(owner)


def run(timeout):
    cell = make_cell((1, 1, 1, 1))
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout * 1000)
    candidate_count = 0
    for mode in ("r_tail", "s_base"):
        for owner in candidate_owners(cell, mode):
            assigned = bundles(owner)
            p_value = subset_sum(values, P, assigned[P])
            q_value = subset_sum(values, Q, assigned[Q])
            blockers = [p_value <= own[P], q_value <= own[Q], *efx_failures(values, owner)]
            if mode == "s_base":
                blockers.append(subset_sum(values, S, assigned[S]) < own[S])
            solver.add(z3.Or(*blockers))
            candidate_count += 1
    checked = solver.check()
    root = Path(__file__).resolve().parents[2]
    dependencies = (
        root / "tracks/parkability/decide_length_three_dual_mode_split.py",
        root / "tracks/parkability/run_alternating_global_lex_cegar.py",
    )
    result = {
        "schema": "length-three-hybrid-atom-v1",
        "status": "HYBRID_ATOM_FORCED" if checked == z3.unsat else "SAT" if checked == z3.sat else "UNKNOWN",
        "solver_status": str(checked),
        "candidate_count": candidate_count,
        "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
        "values": None,
        "claim_boundary": {
            "unsat": "the hybrid escape family in the exact seven-good length-three atom only",
            "sat": "an exact atomic countermodel to the hybrid family, not necessarily to all EFX escapes",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "z3_version": z3.get_version_string(),
            "dependencies": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for path in dependencies
            ],
        },
    }
    if checked == z3.sat:
        result["values"] = [list(row) for row in integerize_model(solver.model(), values)]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "candidate_count", "reason_unknown")}, indent=2))


if __name__ == "__main__":
    main()
