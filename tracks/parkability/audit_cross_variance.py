#!/usr/bin/env python3
"""Test a heterogeneous cross-variance potential for complete EFX."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

import numpy as np

try:
    from . import core, independent
    from .fast_count import FastParkability
except ImportError:
    import core
    import independent
    from fast_count import FastParkability


def assignment_from_index(index: int, n: int, m: int) -> tuple[int, ...]:
    return tuple((index // (n**good)) % n for good in range(m))


def exact_cross_variance(
    values: tuple[tuple[int, ...], ...],
    assignment: tuple[int, ...],
) -> Fraction:
    n = len(values)
    row_totals = tuple(sum(row) for row in values)
    result = Fraction()
    for observer, row in enumerate(values):
        loads = [Fraction() for _ in range(n)]
        for good, owner in enumerate(assignment):
            loads[owner] += Fraction(row[good], row_totals[observer])
        result += sum((load - Fraction(1, n)) ** 2 for load in loads)
    return result


def minimum_cross_variance_allocations(
    values: tuple[tuple[int, ...], ...],
    counter: FastParkability,
) -> tuple[Fraction, list[tuple[int, ...]]]:
    n = len(values)
    m = len(values[0])
    bits = counter.bits
    normalized = np.asarray(
        [
            [Fraction(value, sum(row)) for value in row]
            for row in values
        ],
        dtype=np.float64,
    )
    subset_totals = normalized @ bits.T
    potential = np.zeros(len(counter.complete_masks), dtype=np.float64)
    for observer in range(n):
        loads = subset_totals[observer, counter.complete_masks]
        potential += ((loads - 1.0 / n) ** 2).sum(axis=1)
    minimum = float(potential.min())
    tolerance = max(1e-12, abs(minimum) * 1e-10)
    candidates = np.flatnonzero(potential <= minimum + tolerance)
    exact = [
        (
            exact_cross_variance(
                values,
                assignment_from_index(int(index), n, m),
            ),
            assignment_from_index(int(index), n, m),
        )
        for index in candidates
    ]
    exact_minimum = min(score for score, _ in exact)
    return (
        exact_minimum,
        [assignment for score, assignment in exact if score == exact_minimum],
    )


def audit_instance(
    values: tuple[tuple[int, ...], ...],
    counter: FastParkability | None = None,
) -> dict:
    n = len(values)
    m = len(values[0])
    if counter is None:
        counter = FastParkability(n, m)
    minimum, assignments = minimum_cross_variance_allocations(values, counter)
    efx = [
        assignment
        for assignment in assignments
        if independent.is_complete_efx0(values, assignment)
    ]
    return {
        "cross_variance_minimum": f"{minimum.numerator}/{minimum.denominator}",
        "minimizer_count": len(assignments),
        "efx_minimizer_count": len(efx),
        "minimizer_sample": [list(item) for item in assignments[:10]],
        "efx_minimizer_sample": [list(item) for item in efx[:10]],
    }


def run_random(
    n: int,
    m: int,
    samples: int,
    maximum: int,
    seed: int,
) -> dict:
    counter = FastParkability(n, m)
    rng = random.Random(seed)
    for index in range(samples):
        values = tuple(
            tuple(rng.randint(1, maximum) for _ in range(m))
            for _ in range(n)
        )
        audit = audit_instance(values, counter)
        if audit["efx_minimizer_count"] == 0:
            return {
                "status": "COUNTEREXAMPLE",
                "n": n,
                "m": m,
                "instances_checked": index + 1,
                "maximum": maximum,
                "seed": seed,
                "values": [list(row) for row in values],
                **audit,
            }
    return {
        "status": "NO_COUNTEREXAMPLE",
        "n": n,
        "m": m,
        "instances_checked": samples,
        "maximum": maximum,
        "seed": seed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--n", type=int)
    parser.add_argument("--m", type=int)
    parser.add_argument("--samples", type=int)
    parser.add_argument("--maximum", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.instance is not None:
        raw = json.loads(args.instance.read_text())
        values = core.validate_values(raw["values"], lower=1)
        result = {
            "status": "AUDITED",
            "n": len(values),
            "m": len(values[0]),
            "values": [list(row) for row in values],
            **audit_instance(values),
        }
    else:
        if args.n is None or args.m is None or args.samples is None:
            parser.error("random mode requires --n, --m, and --samples")
        result = run_random(
            args.n,
            args.m,
            args.samples,
            args.maximum,
            args.seed,
        )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
