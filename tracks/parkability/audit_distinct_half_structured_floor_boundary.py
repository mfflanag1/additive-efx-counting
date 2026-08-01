#!/usr/bin/env python3
"""Audit a boundary to the bottom-aware high-pair EFX upgrade."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .analyze_distinct_half_floor_exchange import efx_violations
    from .audit_distinct_half_normal_form_boundaries import audit_branch
    from .decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
        supported_efx_states,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from analyze_distinct_half_floor_exchange import efx_violations
    from audit_distinct_half_normal_form_boundaries import audit_branch
    from decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
        supported_efx_states,
    )


SCHEMA = "distinct-half-structured-floor-boundary-audit-v1"
FAVORITE = 0
VALUES = (
    (82, 75, 74, 47, 27, 63, 36, 22, 53),
    (72, 43, 40, 42, 20, 47, 44, 1, 56),
    (20, 7, 10, 19, 16, 17, 12, 5, 11),
    (53, 40, 17, 30, 34, 19, 50, 3, 35),
)


def structured(values, allocation):
    host = next(
        agent for agent, bundle in enumerate(allocation) if len(bundle) == 3
    )
    favorite_owner = next(
        agent for agent, bundle in enumerate(allocation) if FAVORITE in bundle
    )
    if host == favorite_owner or len(allocation[favorite_owner]) != 2:
        return False
    pair_owners = tuple(
        agent
        for agent in range(4)
        if agent not in (host, favorite_owner)
    )
    if any(
        any(2 * values[agent][good] <= values[agent][FAVORITE]
            for good in allocation[agent])
        for agent in pair_owners
    ):
        return False
    partner = next(
        good for good in allocation[favorite_owner] if good != FAVORITE
    )
    least, second_least = sorted(
        range(1, 9),
        key=lambda good: values[host][good],
    )[:2]
    return (
        partner == least
        or (
            partner == second_least
            and any(
                least in allocation[agent]
                for agent in pair_owners
            )
        )
    )


def audit():
    branch = audit_branch(VALUES)
    universe = favorite_pair_balanced_universe()
    structured_count = 0
    structured_efx_count = 0
    example = None
    for partition in universe:
        for matching in itertools.permutations(range(4)):
            allocation = tuple(
                partition[matching[agent]]
                for agent in range(4)
            )
            if not structured(VALUES, allocation):
                continue
            structured_count += 1
            violations = efx_violations(VALUES, partition, matching)
            if not violations:
                structured_efx_count += 1
            elif example is None:
                example = {
                    "bundles_by_owner": [
                        list(bundle) for bundle in allocation
                    ],
                    "violations": violations,
                }
    supported = supported_efx_states(VALUES, universe)
    literal_count = independent.count_complete_efx0(VALUES)
    if (
        structured_count != 728
        or structured_efx_count != 0
        or len(supported) != 306
        or literal_count != 1364
        or example is None
    ):
        raise AssertionError("structured-floor boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_STRUCTURED_FLOOR_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "branch_audit": branch,
        "favorite_pair_partition_count": len(universe),
        "structured_owner_floor_allocation_count": structured_count,
        "structured_efx_allocation_count": structured_efx_count,
        "favorite_pair_balanced_efx_partition_count": len(supported),
        "literal_complete_efx_allocation_count": literal_count,
        "example_non_efx_structured_allocation": example,
        "interpretation": (
            "The analytic density-floor construction is guaranteed and "
            "has many witnesses on this strict branch-valid profile, but "
            "none of those bottom-aware high-pair allocations is EFX. "
            "The profile itself still has complete balanced EFX."
        ),
        "limitation": (
            "This refutes only the direct EFX strengthening of the analytic "
            "owner-floor construction, not EFX existence."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
