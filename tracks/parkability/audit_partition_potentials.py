#!/usr/bin/env python3
"""Audit canonical threshold potentials over unlabeled bundle partitions."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import core
except ImportError:
    import core


def bundle_statistics(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> tuple[
    tuple[tuple[Fraction, ...], ...],
    tuple[tuple[Fraction, ...], ...],
]:
    totals = []
    thresholds = []
    for row in values:
        denominator = sum(row)
        row_totals = []
        row_thresholds = []
        for bundle in partition:
            total = Fraction(sum(row[good] for good in bundle), denominator)
            minimum = Fraction(min(row[good] for good in bundle), denominator)
            row_totals.append(total)
            row_thresholds.append(total - minimum)
        totals.append(tuple(row_totals))
        thresholds.append(tuple(row_thresholds))
    return tuple(totals), tuple(thresholds)


def admits_efx_matching(
    totals: tuple[tuple[Fraction, ...], ...],
    thresholds: tuple[tuple[Fraction, ...], ...],
) -> bool:
    n = len(totals)
    feasible = [
        [
            all(
                own_bundle == target
                or totals[agent][own_bundle] >= thresholds[agent][target]
                for target in range(n)
            )
            for own_bundle in range(n)
        ]
        for agent in range(n)
    ]
    return any(
        all(feasible[agent][matching[agent]] for agent in range(n))
        for matching in itertools.permutations(range(n))
    )


def potential_keys(
    totals: tuple[tuple[Fraction, ...], ...],
    thresholds: tuple[tuple[Fraction, ...], ...],
) -> dict[str, object]:
    n = len(totals)
    flat_thresholds = tuple(
        sorted(
            (value for row in thresholds for value in row),
            reverse=True,
        )
    )
    row_maxima = tuple(sorted((max(row) for row in thresholds), reverse=True))
    return {
        "threshold_lex": flat_thresholds,
        "row_max_lex": row_maxima,
        "sum_row_max": sum(row_maxima, Fraction()),
        "sum_threshold_squares": sum(
            (value * value for row in thresholds for value in row),
            Fraction(),
        ),
        "sum_thresholds": sum(
            (value for row in thresholds for value in row),
            Fraction(),
        ),
        "threshold_range_squares": sum(
            (
                (value - sum(row, Fraction()) / n) ** 2
                for row in thresholds
                for value in row
            ),
            Fraction(),
        ),
    }


def audit(values: tuple[tuple[int, ...], ...]) -> dict:
    n = len(values)
    m = len(values[0])
    records = []
    for partition in core.iter_unlabeled_nonempty_partitions(n, m):
        totals, thresholds = bundle_statistics(values, partition)
        records.append({
            "partition": partition,
            "admits_efx_matching": admits_efx_matching(totals, thresholds),
            "keys": potential_keys(totals, thresholds),
        })
    names = tuple(records[0]["keys"])
    results = {}
    for name in names:
        minimum = min(record["keys"][name] for record in records)
        minimizers = [
            record for record in records if record["keys"][name] == minimum
        ]
        successful = [
            record for record in minimizers if record["admits_efx_matching"]
        ]
        results[name] = {
            "minimizer_count": len(minimizers),
            "efx_minimizer_count": len(successful),
            "minimizer_sample": [
                [list(bundle) for bundle in record["partition"]]
                for record in minimizers[:5]
            ],
            "efx_minimizer_sample": [
                [list(bundle) for bundle in record["partition"]]
                for record in successful[:5]
            ],
        }
    return {
        "n": n,
        "m": m,
        "partition_count": len(records),
        "efx_partition_count": sum(
            record["admits_efx_matching"] for record in records
        ),
        "potentials": results,
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
