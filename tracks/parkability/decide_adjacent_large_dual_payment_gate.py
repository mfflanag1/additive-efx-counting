#!/usr/bin/env python3
"""Decide failure of both mirrored adjacent-large payment conditions."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "adjacent-large-dual-payment-gate-v1"


def nonempty_subsets(goods):
    for size in range(1, len(goods) + 1):
        yield from itertools.combinations(goods, size)


def no_payment(values, own, recipient, active, reservoir):
    clauses = []
    for payment in nonempty_subsets(reservoir):
        below_threshold = tuple(
            subset_sum(values, recipient, payment)
            < subset_sum(
                values,
                recipient,
                tuple(good for good in active if good != removed),
            )
            for removed in active
        )
        unsafe = tuple(
            subset_sum(
                values,
                observer,
                tuple(good for good in payment if good != removed),
            )
            > own[observer]
            for observer in range(4)
            for removed in payment
        )
        clauses.append(z3.Or(*below_threshold, *unsafe))
    return clauses


def run(sizes, timeout_seconds):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    tr, br, tq, bq = cell["packets"]
    f = cell["floater"]
    d_p = tr + (f,)
    d_r = tq + (f,)
    w = br + tq + bq
    u = tr + br + bq
    solver.add(*no_payment(values, own, 1, d_p, w))
    solver.add(*no_payment(values, own, 0, d_r, u))
    solver.set(timeout=timeout_seconds * 1000)
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "status": str(checked),
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "constraints": {
            "first_failure": "no common-safe R subset B_r+X_q pays tau_r(T_r+f)",
            "second_failure": "no common-safe P subset X_r+B_q pays tau_p(T_q+f)",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
            "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
        },
        "claim_boundary": {
            "unsat": "exact dual-payment dichotomy only in this fixed packet-size cell",
            "sat": "exact fixed-cell counterexample to the dual-payment dichotomy, not to unrestricted escape or EFX existence",
            "unknown": "no mathematical decision",
        },
    }
    if checked == z3.sat:
        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = run(sizes, args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
