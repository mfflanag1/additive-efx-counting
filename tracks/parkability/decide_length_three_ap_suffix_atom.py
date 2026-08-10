#!/usr/bin/env python3
"""Falsify the forced a=p q-source suffix rotation in the exact atom."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import (
        ALL_OWNERS,
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        numeric_efx,
        subset_sum,
    )
    from .run_length_three_global_lex_atomic_cegar import BASE_OWNER, structural_solver
    from .decide_length_three_dual_mode_split import efx_failures
except ImportError:
    from run_alternating_global_lex_cegar import (
        ALL_OWNERS,
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        numeric_efx,
        subset_sum,
    )
    from run_length_three_global_lex_atomic_cegar import BASE_OWNER, structural_solver
    from decide_length_three_dual_mode_split import efx_failures


P, R, Q, S = range(4)
TR, BR, TQ, BQ, X, Y, FLOATER = range(7)
ORDER = (S, P, R, Q)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lex_improves(values, owner):
    base_bundles = bundles(BASE_OWNER)
    assigned = bundles(owner)
    base = tuple(sum(values[i][g] for g in base_bundles[i]) for i in range(4))
    new = tuple(sum(values[i][g] for g in assigned[i]) for i in range(4))
    for agent in ORDER:
        if new[agent] != base[agent]:
            return new[agent] > base[agent]
    return False


def minimum_escape(values):
    best = None
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner) or not lex_improves(values, owner):
            continue
        changed = sum(owner[g] != BASE_OWNER[g] for g in range(7))
        allocated = sum(entry is not None for entry in owner)
        key = (changed, -allocated, tuple(4 if entry is None else entry for entry in owner))
        if best is None or key < best[0]:
            assigned = bundles(owner)
            best = (
                key,
                {
                    "changed_good_count": changed,
                    "allocated_good_count": allocated,
                    "owner_by_good": list(owner),
                    "bundles": {
                        name: list(assigned[agent])
                        for agent, name in enumerate(("p", "r", "q", "s"))
                    },
                },
            )
    return None if best is None else best[1]


def run(timeout):
    solver, values, own = structural_solver(P, "exact")
    solver.set(timeout=timeout * 1000)
    cases = []
    residual = (BR, TQ, BQ)
    for size in range(1, len(residual) + 1):
        for boundary in itertools.combinations(residual, size):
            boundary_value = subset_sum(values, R, boundary)
            unanchored_residual = tuple(g for g in residual if g not in boundary) + (X,)
            for pivot, remainder in ((TR, FLOATER), (FLOATER, TR)):
                theta = values[R][pivot]
                suffix_owner = [None] * 7
                suffix_owner[X] = P
                suffix_owner[pivot] = P
                suffix_owner[remainder] = R
                suffix_owner[Y] = S
                for good in boundary:
                    suffix_owner[good] = Q
                condition = z3.And(
                    values[R][pivot] <= values[R][remainder],
                    desired_expression(values, own, Q, boundary),
                    boundary_value < theta,
                    subset_sum(values, R, unanchored_residual) < theta,
                    z3.Or(*efx_failures(values, tuple(suffix_owner))),
                )
                cases.append((boundary, pivot, tuple(suffix_owner), condition))
    solver.add(z3.Or(*(condition for _boundary, _pivot, _owner, condition in cases)))
    checked = solver.check()
    root = Path(__file__).resolve().parents[2]
    result = {
        "schema": "length-three-ap-suffix-atom-v1",
        "status": "SAT" if checked == z3.sat else "SUFFIX_FORCED" if checked == z3.unsat else "UNKNOWN",
        "solver_status": str(checked),
        "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
        "case_count": len(cases),
        "values": None,
        "claim_boundary": {
            "sat": "an exact atomic countermodel to the forced suffix rotation only",
            "unsat": "the forced suffix rotation under the scalar hypotheses in the exact a=p atom only",
            "not_decided": "the arbitrary-packet a=p escape theorem",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "dependencies": {
                str(path.relative_to(root)): sha256(path)
                for path in (
                    root / "tracks/parkability/run_alternating_global_lex_cegar.py",
                    root / "tracks/parkability/run_length_three_global_lex_atomic_cegar.py",
                    root / "tracks/parkability/decide_length_three_dual_mode_split.py",
                )
            },
            "z3_version": z3.get_version_string(),
        },
    }
    if checked == z3.sat:
        model = solver.model()
        integer_values = integerize_model(model, values)
        result["values"] = [list(row) for row in integer_values]
        for boundary, pivot, owner, condition in cases:
            if z3.is_true(model.eval(condition, model_completion=True)):
                result["boundary"] = list(boundary)
                result["pivot"] = pivot
                result["suffix_owner_by_good"] = list(owner)
                assigned = bundles(owner)
                result["suffix_efx_violations"] = [
                    {"observer": observer, "target": target}
                    for observer in range(4)
                    for target in range(4)
                    if sum(integer_values[observer][g] for g in assigned[observer])
                    < max(
                        (
                            sum(integer_values[observer][g] for g in assigned[target] if g != removed)
                            for removed in assigned[target]
                        ),
                        default=0,
                    )
                ]
                break
        result["minimum_lex_escape"] = minimum_escape(integer_values)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "case_count", "reason_unknown")}, indent=2))


if __name__ == "__main__":
    main()
