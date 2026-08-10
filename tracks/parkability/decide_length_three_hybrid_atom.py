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
    )
    from .run_length_three_global_lex_atomic_cegar import structural_solver
    from .run_alternating_global_lex_cegar import atomic_json, bundles, integerize_model, subset_sum
except ImportError:
    from decide_length_three_dual_mode_split import (
        P,
        Q,
        R,
        S,
        efx_failures,
        make_cell,
    )
    from run_length_three_global_lex_atomic_cegar import structural_solver
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
    records = []
    total_candidates = 0
    for singleton_source in (P, R, Q):
        solver, values, own = structural_solver(singleton_source, "exact")
        solver.set(timeout=timeout * 1000)
        modes = ("r_tail", "s_base") if singleton_source == R else ("r_tail",)
        candidate_count = 0
        for mode in modes:
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
        record = {
            "singleton_source": ("p", "r", "q")[singleton_source],
            "modes": list(modes),
            "candidate_count": candidate_count,
            "solver_status": str(checked),
            "status": "FORCED" if checked == z3.unsat else "SAT" if checked == z3.sat else "UNKNOWN",
            "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
            "values": None,
        }
        if checked == z3.sat:
            record["values"] = [list(row) for row in integerize_model(solver.model(), values)]
        records.append(record)
        total_candidates += candidate_count
    all_forced = all(record["status"] == "FORCED" for record in records)
    root = Path(__file__).resolve().parents[2]
    dependencies = (
        root / "tracks/parkability/decide_length_three_dual_mode_split.py",
        root / "tracks/parkability/run_alternating_global_lex_cegar.py",
        root / "tracks/parkability/run_length_three_global_lex_atomic_cegar.py",
    )
    result = {
        "schema": "length-three-hybrid-atom-v1",
        "status": "ALL_SOURCE_ATOM_FORCED" if all_forced else "NOT_ALL_FORCED",
        "candidate_count": total_candidates,
        "records": records,
        "claim_boundary": {
            "forced": "the source-valid tail/hybrid family in each exact seven-good length-three source atom",
            "not_proved": "the arbitrary-packet all-source length-three theorem",
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
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "candidate_count")}, indent=2))


if __name__ == "__main__":
    main()
