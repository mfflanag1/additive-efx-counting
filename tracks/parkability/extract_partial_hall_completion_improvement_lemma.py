#!/usr/bin/env python3
"""Extract a small completion-or-improvement lemma from the best Hall cell."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import eligible_constraints
    from .partial_hall_factored_master import adjacency_constraints
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import eligible_constraints
    from partial_hall_factored_master import adjacency_constraints


SCHEMA = "partial-hall-completion-improvement-lemma-v1"


def bundle(mask, goods=9):
    return tuple(good for good in range(goods) if mask & (1 << good))


def comparison_key(expression):
    return expression.sexpr()


def comparison_record(expression):
    return expression.sexpr()


def holds(expression, variables, integer_values):
    substitutions = [
        (variables[agent][good], z3.RealVal(integer_values[agent][good]))
        for agent in range(4)
        for good in range(9)
    ]
    return z3.is_true(z3.simplify(z3.substitute(expression, *substitutions)))


def solve(base_constraints, supports, outcome, timeout_ms=30000):
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*base_constraints)
    solver.add(*supports)
    solver.add(z3.Not(outcome))
    return solver.check(), solver


def run(seed, output, smt2_output):
    document = json.loads(seed.read_text())
    integer_values = document["values"]
    variables = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    floater = 8
    completion_direct = ((6, 7), (1, 2, 3), (0, 4, 8), (5,))
    direct_matching = (0, 1, 2, 3)
    completion_transfer = ((6, 7), (1, 3, 8), (0, 2, 4), (5,))
    transfer_matching = (0, 2, 1, 3)
    rival = ((6, 7), (1, 8), (0, 3, 4), (5,))
    rival_floater = 2

    positivity = [entry > 0 for row in variables for entry in row]
    normalizations = [z3.Sum(*row) == 1 for row in variables]
    base_eligibility = list(eligible_constraints(variables, base, floater))
    base_constraints = positivity + normalizations + base_eligibility

    direct_constraints = [
        constraint
        for agent, assigned_bundle in enumerate(direct_matching)
        for constraint in adjacency_constraints(
            variables[agent], completion_direct, assigned_bundle
        )
    ]
    transfer_constraints = [
        constraint
        for agent, assigned_bundle in enumerate(transfer_matching)
        for constraint in adjacency_constraints(
            variables[agent], completion_transfer, assigned_bundle
        )
    ]
    rival_constraints = list(
        eligible_constraints(variables, rival, rival_floater)
    )
    base_score = z3.Sum(
        *(z3.Sum(*(variables[agent][good] for good in base[agent])) for agent in range(4))
    )
    rival_score = z3.Sum(
        *(z3.Sum(*(variables[agent][good] for good in rival[agent])) for agent in range(4))
    )
    outcomes = {
        "direct_completion": z3.And(*direct_constraints),
        "transfer_completion": z3.And(*transfer_constraints),
        "eligible_strict_improvement": z3.And(
            *rival_constraints, rival_score > base_score
        ),
    }
    outcome = z3.Or(*outcomes.values())

    candidate_supports = {}
    for expression in direct_constraints + transfer_constraints + rival_constraints:
        if holds(expression, variables, integer_values):
            candidate_supports.setdefault(comparison_key(expression), expression)
    supports = list(candidate_supports.values())
    initial_result, _ = solve(base_constraints, supports, outcome)
    if initial_result != z3.unsat:
        raise RuntimeError(f"full seed support does not prove trichotomy: {initial_result}")

    index = 0
    while index < len(supports):
        trial = supports[:index] + supports[index + 1 :]
        result, _ = solve(base_constraints, trial, outcome)
        if result == z3.unsat:
            supports = trial
        else:
            index += 1

    final_result, final_solver = solve(base_constraints, supports, outcome)
    if smt2_output is not None:
        smt2_output.write_text(final_solver.to_smt2())

    artifact = {
        "schema": SCHEMA,
        "status": "PROVED" if final_result == z3.unsat else str(final_result).upper(),
        "meaning": (
            "Under positive normalized additive valuations, base eligibility, "
            "and the listed support comparisons, at least one listed complete "
            "EFX matching or an eligible strict potential improvement exists."
        ),
        "seed_path": str(seed),
        "seed_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
        "base": {"bundles": [list(part) for part in base], "floater": floater},
        "outcomes": {
            "direct_completion": {
                "bundles": [list(part) for part in completion_direct],
                "matching": list(direct_matching),
            },
            "transfer_completion": {
                "bundles": [list(part) for part in completion_transfer],
                "matching": list(transfer_matching),
            },
            "eligible_strict_improvement": {
                "bundles": [list(part) for part in rival],
                "floater": rival_floater,
            },
        },
        "seed_false_direct_comparisons": [
            comparison_record(item)
            for item in direct_constraints
            if not holds(item, variables, integer_values)
        ],
        "seed_false_transfer_comparisons": [
            comparison_record(item)
            for item in transfer_constraints
            if not holds(item, variables, integer_values)
        ],
        "candidate_support_count": len(candidate_supports),
        "deletion_irreducible_support_count": len(supports),
        "deletion_irreducible_supports": [
            comparison_record(item) for item in supports
        ],
        "solver_verdict": str(final_result),
    }
    if smt2_output is not None:
        artifact["smt2_path"] = str(smt2_output)
        artifact["smt2_sha256"] = hashlib.sha256(smt2_output.read_bytes()).hexdigest()
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path)
    args = parser.parse_args()
    artifact = run(args.seed, args.output, args.smt2_output)
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
