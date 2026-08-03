#!/usr/bin/env python3
"""Prove literal threshold expansions and audit an exported master."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_threshold_hall_local_gradient import (
        eligible as nested_eligible,
        threshold as nested_threshold,
    )
    from .run_minimum_slot_orbit_cegar import (
        eligible,
        theta_upper_bound,
        threshold_terms,
    )
except ImportError:
    from anneal import atomic_json
    from decide_threshold_hall_local_gradient import (
        eligible as nested_eligible,
        threshold as nested_threshold,
    )
    from run_minimum_slot_orbit_cegar import (
        eligible,
        theta_upper_bound,
        threshold_terms,
    )


SCHEMA = "minimum-slot-literal-threshold-expansion-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equivalent(left, right):
    solver = z3.SolverFor("QF_LRA")
    solver.add(z3.Xor(left, right))
    return solver.check() == z3.unsat


def ite_count(assertions):
    count = 0
    seen = set()
    stack = list(assertions)
    while stack:
        expression = stack.pop()
        key = expression.hash()
        if key in seen:
            continue
        seen.add(key)
        if z3.is_app_of(expression, z3.Z3_OP_ITE):
            count += 1
        stack.extend(expression.children())
    return count


def run(source, output):
    row = [z3.Real(f"x_{good}") for good in range(9)]
    bound = z3.Real("bound")
    threshold_checks = []
    for bundle in ((0,), (0, 1), (0, 1, 2)):
        nested = nested_threshold(row, bundle)
        terms = threshold_terms(row, bundle)
        threshold_checks.append(
            {
                "bundle_size": len(bundle),
                "upper_bound_equivalent": equivalent(
                    bound >= nested,
                    z3.And(*(bound >= term for term in terms)),
                ),
                "strict_failure_equivalent": equivalent(
                    bound < nested,
                    z3.Or(*(bound < term for term in terms)),
                ),
            }
        )

    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    theta_checks = []
    for bundles in (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0,), (1, 2), (3, 4), (5, 6, 7)),
    ):
        nested = z3.Sum(
            *(nested_threshold(values[owner], bundles[owner]) for owner in range(4))
        )
        theta_checks.append(
            {
                "shape": [len(bundle) for bundle in bundles],
                "upper_bound_equivalent": equivalent(
                    nested <= bound,
                    theta_upper_bound(values, bundles, bound),
                ),
            }
        )

    base = ((0, 1), (2, 3), (4, 5), (6, 7))
    eligibility_equivalent = equivalent(
        nested_eligible(values, base, 8),
        eligible(values, base, 8),
    )
    solver = z3.Solver()
    solver.from_file(str(source))
    source_ite_count = ite_count(solver.assertions())
    checks = {
        "threshold_equivalences": all(
            record["upper_bound_equivalent"]
            and record["strict_failure_equivalent"]
            for record in threshold_checks
        ),
        "theta_equivalences": all(
            record["upper_bound_equivalent"] for record in theta_checks
        ),
        "eligibility_equivalent": eligibility_equivalent,
        "source_has_zero_ites": source_ite_count == 0,
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "LITERAL_THRESHOLD_EXPANSION_PROVED"
            if all(checks.values())
            else "LITERAL_THRESHOLD_EXPANSION_MISMATCH"
        ),
        "meaning": (
            "Symbolic QF_LRA equivalence checks prove the leave-one-good-out "
            "expansions used for threshold upper bounds, strict failures, "
            "eligibility, and threshold-potential bounds."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "source_assertion_count": len(solver.assertions()),
        "source_ite_count": source_ite_count,
        "threshold_checks": threshold_checks,
        "theta_checks": theta_checks,
        "checks": checks,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
