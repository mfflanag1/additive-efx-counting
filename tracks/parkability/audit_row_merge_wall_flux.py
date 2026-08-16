#!/usr/bin/env python3
"""Audit allocation-count flux at exact row-interpolation walls."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_row_merge_interpolation import (
        bundles_from_assignment,
        fixed_agents_are_efx,
        moving_agent_interval,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from audit_row_merge_interpolation import (
        bundles_from_assignment,
        fixed_agents_are_efx,
        moving_agent_interval,
    )


SCHEMA = "row-merge-wall-flux-audit-v1"


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def allocation_sign(assignment: tuple[int, ...], n: int) -> int:
    bundles = bundles_from_assignment(assignment, n)
    masks = tuple(sum(1 << good for good in bundle) for bundle in bundles)
    ordered = sorted(range(n), key=lambda agent: masks[agent])
    positions = {agent: position for position, agent in enumerate(ordered)}
    return permutation_sign(tuple(positions[agent] for agent in range(n)))


def fraction_record(value: Fraction) -> dict[str, int | str | float]:
    return {
        "exact": str(value),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def assignment_record(assignment: tuple[int, ...], n: int) -> dict:
    bundles = bundles_from_assignment(assignment, n)
    return {
        "assignment": list(assignment),
        "bundles": [list(bundle) for bundle in bundles],
    }


def audit_path(values, moving: int, base: int) -> dict:
    n = len(values)
    m = len(values[0])
    intervals = []
    for assignment in itertools.product(range(n), repeat=m):
        bundles = bundles_from_assignment(assignment, n)
        if not fixed_agents_are_efx(values, bundles, moving):
            continue
        interval = moving_agent_interval(values, bundles, moving, base)
        if interval is None:
            continue
        intervals.append((*interval, allocation_sign(assignment, n), assignment))

    walls = sorted(
        {
            endpoint
            for lower, upper, _sign, _assignment in intervals
            for endpoint in (lower, upper)
            if 0 < endpoint < 1
        }
    )
    events = []
    for wall in walls:
        left = [
            sign
            for lower, upper, sign, _assignment in intervals
            if lower < wall <= upper
        ]
        right = [
            sign
            for lower, upper, sign, _assignment in intervals
            if lower <= wall < upper
        ]
        disappearing = [
            sign
            for lower, upper, sign, _assignment in intervals
            if lower < wall == upper
        ]
        appearing = [
            sign
            for lower, upper, sign, _assignment in intervals
            if lower == wall < upper
        ]
        low_side_allocations = None
        if min(len(left), len(right)) <= n:
            low_side_allocations = {
                "left": [
                    assignment_record(assignment, n)
                    for lower, upper, _sign, assignment in intervals
                    if lower < wall <= upper
                ],
                "right": [
                    assignment_record(assignment, n)
                    for lower, upper, _sign, assignment in intervals
                    if lower <= wall < upper
                ],
            }
        events.append(
            {
                "wall": fraction_record(wall),
                "left_count": len(left),
                "right_count": len(right),
                "count_delta": len(right) - len(left),
                "count_parity_preserved": len(left) % 2 == len(right) % 2,
                "count_mod_n_preserved": len(left) % n == len(right) % n,
                "left_signed_count": sum(left),
                "right_signed_count": sum(right),
                "signed_count_preserved": sum(left) == sum(right),
                "disappearing_count": len(disappearing),
                "appearing_count": len(appearing),
                "disappearing_signed_count": sum(disappearing),
                "appearing_signed_count": sum(appearing),
                "low_side_allocations": low_side_allocations,
            }
        )

    return {
        "moving_agent": moving,
        "base_agent": base,
        "supporting_interval_count": len(intervals),
        "interior_wall_count": len(events),
        "count_parity_preserved_at_every_wall": all(
            event["count_parity_preserved"] for event in events
        ),
        "count_mod_n_preserved_at_every_wall": all(
            event["count_mod_n_preserved"] for event in events
        ),
        "canonical_partition_signed_count_preserved_at_every_wall": all(
            event["signed_count_preserved"] for event in events
        ),
        "events": events,
    }


def run(source_path: Path, output_path: Path, moving: int | None, base: int | None):
    source = json.loads(source_path.read_text())
    values = core.validate_values(source["values"], lower=1)
    n = len(values)
    if (moving is None) != (base is None):
        raise ValueError("--moving and --base must be supplied together")
    pairs = (
        [(moving, base)]
        if moving is not None
        else [
            (candidate_moving, candidate_base)
            for candidate_moving in range(n)
            for candidate_base in range(n)
            if candidate_moving != candidate_base
        ]
    )
    paths = [audit_path(values, candidate_moving, candidate_base) for candidate_moving, candidate_base in pairs]
    result = {
        "schema": SCHEMA,
        "source": str(source_path),
        "n": n,
        "m": len(values[0]),
        "path_count": len(paths),
        "count_parity_invariant": all(
            path["count_parity_preserved_at_every_wall"] for path in paths
        ),
        "count_mod_n_invariant": all(
            path["count_mod_n_preserved_at_every_wall"] for path in paths
        ),
        "canonical_partition_signed_count_invariant": all(
            path["canonical_partition_signed_count_preserved_at_every_wall"]
            for path in paths
        ),
        "paths": paths,
        "claim_boundary": (
            "This exactly audits three candidate wall-flux invariants on the "
            "specified finite profile. Failure refutes the corresponding "
            "candidate; survival is not a general theorem."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--moving", type=int)
    parser.add_argument("--base", type=int)
    args = parser.parse_args()
    run(args.source, args.output, args.moving, args.base)


if __name__ == "__main__":
    main()
