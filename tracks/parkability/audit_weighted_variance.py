#!/usr/bin/env python3
"""Test whether an EFX partition is supported by weighted row variances."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from . import core
except ImportError:
    import core


def canonical_partition_of_assignment(
    assignment: tuple[int, ...],
    n: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(
        tuple(good for good, owner in enumerate(assignment) if owner == agent)
        for agent in range(n)
    ))


def variance_vector(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> tuple[Fraction, ...]:
    result = []
    for row in values:
        total = sum(row)
        loads = [
            Fraction(sum(row[good] for good in bundle), total)
            for bundle in partition
        ]
        result.append(sum(load * load for load in loads))
    return tuple(result)


def rational(value: Fraction) -> z3.RatNumRef:
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def supporting_weights(
    candidate: tuple[Fraction, ...],
    universe: list[tuple[Fraction, ...]],
) -> tuple[Fraction, ...] | None:
    weights = [z3.Real(f"weight_{agent}") for agent in range(len(candidate))]
    solver = z3.SolverFor("QF_LRA")
    solver.add(*(weight > 0 for weight in weights))
    solver.add(z3.Sum(*weights) == 1)
    for alternative in universe:
        solver.add(
            z3.Sum(*(
                weights[agent] * rational(candidate[agent])
                for agent in range(len(candidate))
            ))
            <=
            z3.Sum(*(
                weights[agent] * rational(alternative[agent])
                for agent in range(len(candidate))
            ))
        )
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    return tuple(
        Fraction(
            model.eval(weight).numerator_as_long(),
            model.eval(weight).denominator_as_long(),
        )
        for weight in weights
    )


def audit(values: tuple[tuple[int, ...], ...]) -> dict:
    n = len(values)
    m = len(values[0])
    partitions = list(core.iter_unlabeled_nonempty_partitions(n, m))
    vectors = [variance_vector(values, partition) for partition in partitions]
    position = {partition: index for index, partition in enumerate(partitions)}
    efx_partitions = sorted({
        canonical_partition_of_assignment(assignment, n)
        for assignment in core.iter_efx0_assignments(values)
    })
    supported = []
    for partition in efx_partitions:
        weights = supporting_weights(vectors[position[partition]], vectors)
        if weights is not None:
            supported.append({
                "partition": [list(bundle) for bundle in partition],
                "weights": [
                    f"{weight.numerator}/{weight.denominator}"
                    for weight in weights
                ],
            })
    return {
        "n": n,
        "m": m,
        "partition_count": len(partitions),
        "efx_partition_count": len(efx_partitions),
        "supported_efx_partition_count": len(supported),
        "supported_sample": supported[:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = json.loads(args.instance.read_text())
    values = core.validate_values(raw["values"], lower=1)
    result = {
        "status": "AUDITED",
        "values": [list(row) for row in values],
        **audit(values),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
