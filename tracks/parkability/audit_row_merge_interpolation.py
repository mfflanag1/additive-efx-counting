#!/usr/bin/env python3
"""Audit EFX coverage while one valuation row separates from another."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
except ImportError:
    import core
    import independent
    from anneal import atomic_json


SCHEMA = "row-merge-interpolation-audit-v2"


def bundles_from_assignment(assignment, n):
    return tuple(
        tuple(good for good, owner in enumerate(assignment) if owner == agent)
        for agent in range(n)
    )


def fixed_agents_are_efx(values, bundles, moving):
    for observer, row in enumerate(values):
        if observer == moving:
            continue
        own = sum(row[good] for good in bundles[observer])
        for target, bundle in enumerate(bundles):
            if target == observer:
                continue
            for removed in bundle:
                if own < sum(row[good] for good in bundle if good != removed):
                    return False
    return True


def moving_agent_interval(values, bundles, moving, base):
    lower = Fraction(0)
    upper = Fraction(1)
    base_row = values[base]
    target_row = values[moving]
    own_bundle = bundles[moving]
    for target, bundle in enumerate(bundles):
        if target == moving:
            continue
        for removed in bundle:
            remainder = tuple(good for good in bundle if good != removed)
            intercept = sum(base_row[good] for good in own_bundle) - sum(
                base_row[good] for good in remainder
            )
            slope = sum(
                target_row[good] - base_row[good] for good in own_bundle
            ) - sum(
                target_row[good] - base_row[good] for good in remainder
            )
            if slope == 0:
                if intercept < 0:
                    return None
            elif slope > 0:
                lower = max(lower, Fraction(-intercept, slope))
            else:
                upper = min(upper, Fraction(-intercept, slope))
            if lower > upper:
                return None
    lower = max(lower, Fraction(0))
    upper = min(upper, Fraction(1))
    return (lower, upper) if lower <= upper else None


def fraction_record(value):
    return {
        "exact": str(value),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def interval_cover(intervals):
    frontier = Fraction(0)
    cover = []
    while frontier < 1:
        candidates = [
            item
            for item in intervals
            if item[0] <= frontier and item[1] > frontier
        ]
        if not candidates:
            break
        chosen = max(
            candidates,
            key=lambda item: (item[1], -item[0], item[2]),
        )
        cover.append(chosen)
        frontier = chosen[1]
    return frontier, cover


def cover_record(cover):
    return [
        {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
            "assignment": list(assignment),
        }
        for lower, upper, assignment in cover
    ]


def path_audit(values, moving, base):
    n = len(values)
    m = len(values[0])
    intervals = []
    for assignment in itertools.product(range(n), repeat=m):
        bundles = bundles_from_assignment(assignment, n)
        if not fixed_agents_are_efx(values, bundles, moving):
            continue
        interval = moving_agent_interval(values, bundles, moving, base)
        if interval is not None:
            intervals.append((*interval, assignment))
    intervals.sort(key=lambda item: (item[0], -item[1], item[2]))

    components = []
    for lower, upper, _assignment in intervals:
        if not components or lower > components[-1][1]:
            components.append([lower, upper])
        else:
            components[-1][1] = max(components[-1][1], upper)

    frontier, cover = interval_cover(intervals)
    by_partition = {}
    for lower, upper, assignment in intervals:
        bundles = bundles_from_assignment(assignment, n)
        partition = tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))
        by_partition.setdefault(partition, []).append((lower, upper, assignment))
    stable_partitions = []
    for partition, partition_intervals in sorted(by_partition.items()):
        partition_frontier, partition_cover = interval_cover(partition_intervals)
        if partition_frontier >= 1:
            stable_partitions.append((partition, partition_cover))
    stable_partition_record = None
    if stable_partitions:
        partition, partition_cover = min(
            stable_partitions,
            key=lambda item: (len(item[1]), item[0]),
        )
        stable_partition_record = {
            "partition": [list(bundle) for bundle in partition],
            "assignment_cover_size": len(partition_cover),
            "assignment_cover": cover_record(partition_cover),
        }

    return {
        "moving_agent": moving,
        "base_agent": base,
        "interpolated_row": (
            f"(1-t) row {base} + t row {moving}, for 0 <= t <= 1"
        ),
        "supporting_interval_count": len(intervals),
        "efx_allocation_count_at_zero": sum(
            lower <= 0 <= upper for lower, upper, _ in intervals
        ),
        "efx_allocation_count_at_one": sum(
            lower <= 1 <= upper for lower, upper, _ in intervals
        ),
        "union_component_count": len(components),
        "union_components": [
            {
                "lower": fraction_record(lower),
                "upper": fraction_record(upper),
            }
            for lower, upper in components
        ],
        "covers_unit_interval": frontier >= 1,
        "greedy_cover_size": len(cover),
        "greedy_cover": cover_record(cover),
        "right_frontier": fraction_record(frontier),
        "supporting_unlabeled_partition_count": len(by_partition),
        "full_path_partition_count": len(stable_partitions),
        "stable_partition": stable_partition_record,
    }


def run(source_path, result_path):
    if result_path.exists():
        raise ValueError("result path already exists")
    source = json.loads(source_path.read_text())
    values = core.validate_values(source["values"], lower=1)
    if len(values) != 4:
        raise ValueError("the row-merge audit currently requires four agents")
    direct_count = independent.count_complete_efx0(values)
    paths = [
        path_audit(values, moving, base)
        for moving in range(len(values))
        for base in range(len(values))
        if moving != base
    ]
    if any(path["efx_allocation_count_at_one"] != direct_count for path in paths):
        raise AssertionError("interpolation endpoint disagrees with direct EFX count")

    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_ORDERED_ROW_MERGES_COVERED"
            if all(path["covers_unit_interval"] for path in paths)
            else "ROW_MERGE_COVERAGE_GAP_FOUND"
        ),
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "n": len(values),
        "m": len(values[0]),
        "values": [list(row) for row in values],
        "complete_efx_allocation_count": direct_count,
        "ordered_row_merge_path_count": len(paths),
        "maximum_greedy_cover_size": max(
            path["greedy_cover_size"] for path in paths
        ),
        "all_ordered_row_merges_have_stable_partition": all(
            path["stable_partition"] is not None for path in paths
        ),
        "maximum_stable_partition_assignment_cover_size": max(
            (
                path["stable_partition"]["assignment_cover_size"]
                for path in paths
                if path["stable_partition"] is not None
            ),
            default=0,
        ),
        "paths": paths,
        "claim_boundary": (
            "This is an exact finite audit of the recorded source profile. "
            "Path coverage for this profile does not prove a row-merge "
            "continuation theorem for arbitrary additive instances."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.result)


if __name__ == "__main__":
    main()
