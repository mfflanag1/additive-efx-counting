#!/usr/bin/env python3
"""Decide the adjacent safe r/q repartition theorem in a fixed cell."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_adjacent_large_dual_payment_gate import nonempty_subsets
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        atomic_json,
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from decide_adjacent_large_dual_payment_gate import nonempty_subsets
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        atomic_json,
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "adjacent-large-safe-repartition-gate-v2"


def add_compatible_absence(solver, values, own, cell):
    _tr, br, _tq, bq = cell["packets"]
    families = (
        (1, 3, br),
        (3, 1, bq),
        (2, 1, bq),
        (0, 1, bq),
    )
    for source, target, incoming in families:
        target_bundle = cell["base_bundles"][target]
        for incoming_size in range(len(incoming) + 1):
            for incoming_subset in itertools.combinations(incoming, incoming_size):
                for release_size in range(len(target_bundle) + 1):
                    for release in itertools.combinations(target_bundle, release_size):
                        offer = tuple(
                            good for good in target_bundle if good not in release
                        ) + incoming_subset
                        for candidate in nonempty_subsets(offer):
                            solver.add(
                                z3.Not(
                                    desired_expression(values, own, source, candidate)
                                )
                            )


def common_safe_expression(values, own, bundle):
    return z3.And(
        *(
            subset_sum(
                values,
                observer,
                tuple(good for good in bundle if good != removed),
            )
            <= own[observer]
            for observer in range(4)
            for removed in bundle
        )
    )


def safe_rq_repartition_expression(values, own, r_bundle, q_bundle):
    q_pays = z3.And(
        *(
            subset_sum(values, 3, q_bundle)
            >= subset_sum(
                values,
                3,
                tuple(good for good in r_bundle if good != removed),
            )
            for removed in r_bundle
        )
    )
    return z3.And(
        desired_expression(values, own, 1, r_bundle),
        common_safe_expression(values, own, q_bundle),
        q_pays,
    )


def rq_repartitions(cell):
    pool = (
        cell["base_bundles"][1]
        + cell["base_bundles"][3]
        + (cell["floater"],)
    )
    for r_bundle in nonempty_subsets(pool):
        remainder = tuple(good for good in pool if good not in r_bundle)
        for q_bundle in nonempty_subsets(remainder):
            yield r_bundle, q_bundle


def add_no_safe_rq_repartition(solver, values, own, cell):
    """Exclude EFX allocations (x, R, y, Q) drawn from Xr+Xq+f."""
    for r_bundle, q_bundle in rq_repartitions(cell):
        solver.add(
            z3.Not(
                safe_rq_repartition_expression(
                    values, own, r_bundle, q_bundle
                )
            )
        )


def run(sizes, timeout_seconds):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    add_compatible_absence(solver, values, own, cell)
    add_no_safe_rq_repartition(solver, values, own, cell)
    solver.set(timeout=timeout_seconds * 1000)
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "status": str(checked),
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "premises": [
            "strict adjacent-large structural cell",
            "all four PI-compatible generalized families absent",
            (
                "no disjoint R,Q subset X_r+X_q+f with R desired by r, Q "
                "common-safe, and v_q(Q) at least tau_q(R)"
            ),
        ],
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
            "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
        },
        "claim_boundary": {
            "unsat": "fixed-cell safe-repartition theorem only",
            "sat": "fixed-cell counterexample to that theorem, not to unrestricted escape or EFX",
            "unknown": "no mathematical decision",
        },
    }
    if checked == z3.sat:
        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = run(sizes, args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
