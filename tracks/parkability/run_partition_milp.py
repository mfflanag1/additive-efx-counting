#!/usr/bin/env python3
"""Numerical robust-counterexample search over partition feasibility graphs."""

from __future__ import annotations

import argparse
import itertools
import json
import platform
import time
from pathlib import Path

from ortools.linear_solver import pywraplp

try:
    from . import core, independent
    from .run_lra_cegar import atomic_json, canonical_sha256
except ImportError:
    import core
    import independent
    from run_lra_cegar import atomic_json, canonical_sha256


SCHEMA = "partition-robust-milp-result-v1"


def run(
    *,
    n: int,
    m: int,
    favorite_pattern: tuple[int, ...],
    minimum_margin: float,
    time_limit_s: float,
    result_path: Path,
) -> dict:
    if (
        n < 2
        or m < n
        or len(favorite_pattern) != n
        or any(not 0 <= good < m for good in favorite_pattern)
        or minimum_margin <= 0
        or time_limit_s < 0
        or result_path.exists()
    ):
        raise ValueError("invalid pattern, margin, timeout, or result path")
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("OR-Tools SCIP backend is unavailable")
    solver.SetTimeLimit(round(time_limit_s * 1000))

    started = time.time()
    margin = solver.NumVar(minimum_margin, 1 / m, "margin")
    values = [
        [
            solver.NumVar(0, 1, f"value_{observer}_{good}")
            for good in range(m)
        ]
        for observer in range(n)
    ]
    for observer, row in enumerate(values):
        solver.Add(sum(row) == 1)
        for value in row:
            solver.Add(value >= margin)
        favorite = favorite_pattern[observer]
        for other in range(m):
            if other != favorite:
                solver.Add(row[favorite] - row[other] >= margin)

    comparison_variables: dict[tuple[int, int, int], pywraplp.Variable] = {}

    def comparison(observer: int, own_mask: int, remainder_mask: int):
        key = observer, own_mask, remainder_mask
        existing = comparison_variables.get(key)
        if existing is not None:
            return existing
        sign = solver.BoolVar(
            f"comparison_{observer}_{own_mask}_{remainder_mask}"
        )
        difference = sum(
            values[observer][good]
            for good in range(m)
            if own_mask & (1 << good)
        ) - sum(
            values[observer][good]
            for good in range(m)
            if remainder_mask & (1 << good)
        )
        solver.Add(difference >= margin - 2 * (1 - sign))
        solver.Add(difference <= -margin + 2 * sign)
        comparison_variables[key] = sign
        return sign

    partition_count = 0
    edge_count = 0
    matching_constraints = 0
    for partition in core.iter_unlabeled_nonempty_partitions(n, m):
        masks = [
            sum(1 << good for good in bundle)
            for bundle in partition
        ]
        feasible = []
        for observer in range(n):
            row = []
            for own_bundle in range(n):
                comparisons = []
                for target_bundle in range(n):
                    if target_bundle == own_bundle:
                        continue
                    for removed in partition[target_bundle]:
                        remainder = masks[target_bundle] ^ (1 << removed)
                        if remainder:
                            comparisons.append(
                                comparison(
                                    observer,
                                    masks[own_bundle],
                                    remainder,
                                )
                            )
                edge = solver.BoolVar(
                    f"edge_{partition_count}_{observer}_{own_bundle}"
                )
                for sign in comparisons:
                    solver.Add(edge <= sign)
                solver.Add(
                    edge
                    >= sum(comparisons) - (len(comparisons) - 1)
                )
                row.append(edge)
                edge_count += 1
            feasible.append(row)
        for matching in itertools.permutations(range(n)):
            solver.Add(
                sum(
                    feasible[observer][matching[observer]]
                    for observer in range(n)
                )
                <= n - 1
            )
            matching_constraints += 1
        partition_count += 1

    solver.Maximize(margin)
    build_seconds = time.time() - started
    solve_started = time.time()
    status_code = solver.Solve()
    solve_seconds = time.time() - solve_started
    status_names = {
        pywraplp.Solver.OPTIMAL: "OPTIMAL",
        pywraplp.Solver.FEASIBLE: "FEASIBLE",
        pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
        pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
        pywraplp.Solver.ABNORMAL: "ABNORMAL",
        pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
    }
    status = status_names.get(status_code, f"STATUS_{status_code}")
    extra = {}
    if status_code in {pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE}:
        scale = 10**12
        integer_values = tuple(
            tuple(max(1, round(value.solution_value() * scale)) for value in row)
            for row in values
        )
        exact_count = independent.count_complete_efx0(integer_values)
        extra = {
            "objective_margin": margin.solution_value(),
            "best_bound": solver.Objective().BestBound(),
            "rounded_integer_values": [list(row) for row in integer_values],
            "rounded_values_sha256": canonical_sha256(integer_values),
            "rounded_exact_complete_efx0_count": exact_count,
            "rounded_exact_parkable_triple_count": len(
                independent.enumerate_completion_first(integer_values)
            ),
        }
        if exact_count == 0:
            extra["audited_status"] = "ZERO_COMPLETE_EFX0"
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": "numerical robust search; not an exact proof certificate",
        "n": n,
        "m": m,
        "favorite_pattern": list(favorite_pattern),
        "minimum_margin": minimum_margin,
        "partition_count": partition_count,
        "comparison_variables": len(comparison_variables),
        "feasibility_edge_variables": edge_count,
        "matching_constraints": matching_constraints,
        "variables": solver.NumVariables(),
        "constraints": solver.NumConstraints(),
        "build_seconds": round(build_seconds, 6),
        "solve_seconds": round(solve_seconds, 6),
        "elapsed_seconds": round(time.time() - started, 6),
        "solver": solver.SolverVersion(),
        "environment": {"python": platform.python_version()},
        **extra,
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=8)
    parser.add_argument("--favorite-pattern", required=True)
    parser.add_argument("--minimum-margin", type=float, default=1e-7)
    parser.add_argument("--time-limit", type=float, default=3600)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    pattern = tuple(map(int, args.favorite_pattern.split(",")))
    run(
        n=args.n,
        m=args.m,
        favorite_pattern=pattern,
        minimum_margin=args.minimum_margin,
        time_limit_s=args.time_limit,
        result_path=args.result,
    )


if __name__ == "__main__":
    main()
