#!/usr/bin/env python3
"""Audit the unrestricted-real common-favorite balanced-only profile."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "real-common-favorite-balanced-boundary-audit-v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_path: Path) -> dict:
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != "generic-partition-lra-result-v1"
        or source.get("status") != "ZERO_SUPPORTED_PARTITIONS"
        or source.get("domain") != "strictly positive reals normalized per row"
        or source.get("favorite_pattern") != [0, 0, 0, 0]
        or source.get("partition_shape") != [6, 1, 1, 1]
        or source.get("require_distinct_item_values") is not True
    ):
        raise AssertionError("the balanced-boundary source changed scope")
    values = tuple(tuple(row) for row in source["values"])
    core.validate_values(values, expected_n=4, expected_m=9, lower=1)
    if any(
        len(set(row)) != 9
        or any(row[0] <= row[good] for good in range(1, 9))
        for row in values
    ):
        raise AssertionError("the matrix lacks a strict common favorite")

    labeled_shape_counts: Counter[tuple[int, ...]] = Counter()
    for assignment in itertools.product(range(4), repeat=9):
        if independent.is_complete_efx0(values, assignment):
            labeled_shape_counts[
                tuple(sorted(Counter(assignment).values(), reverse=True))
            ] += 1

    universe = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    supported = supported_partitions(values, universe)
    partition_shape_counts = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in supported
    )
    singleton_good_counts = Counter(
        good
        for partition in supported
        for good in range(9)
        if (good,) in partition
    )
    if (
        not supported
        or set(labeled_shape_counts) != {(3, 2, 2, 2)}
        or set(partition_shape_counts) != {(3, 2, 2, 2)}
        or singleton_good_counts
    ):
        raise AssertionError("the profile is not exclusively balanced EFX")

    residual_selection = {}
    for owner in range(4):
        remaining_agents = tuple(agent for agent in range(4) if agent != owner)
        residual_efx_count = 0
        passing_count = 0
        best_slack = None
        for owners in itertools.product(remaining_agents, repeat=8):
            bundles = {
                agent: tuple(
                    good
                    for good, assigned in zip(range(1, 9), owners)
                    if assigned == agent
                )
                for agent in remaining_agents
            }
            if any(
                sum(values[agent][good] for good in bundles[agent])
                < sum(values[agent][good] for good in bundles[other] if good != removed)
                for agent in remaining_agents
                for other in remaining_agents
                for removed in bundles[other]
            ):
                continue
            residual_efx_count += 1
            threshold = max(
                sum(values[owner][good] for good in bundles[agent])
                - min(values[owner][good] for good in bundles[agent])
                for agent in remaining_agents
            )
            slack = values[owner][0] - threshold
            best_slack = slack if best_slack is None else max(best_slack, slack)
            passing_count += slack >= 0
        residual_selection[str(owner)] = {
            "residual_efx_allocations": residual_efx_count,
            "threshold_passing_allocations": passing_count,
            "best_threshold_slack": best_slack,
        }
    if any(
        record["threshold_passing_allocations"]
        for record in residual_selection.values()
    ):
        raise AssertionError("the singleton reduction found a completion")

    return {
        "schema": SCHEMA,
        "status": "BALANCED_BOUNDARY_AUDIT_PASSED",
        "claim": (
            "This strict common-favorite profile has complete EFX "
            "allocations, but every one has shape (3,2,2,2)."
        ),
        "source_path": str(source_path.resolve()),
        "source_sha256": file_sha256(source_path),
        "values": [list(row) for row in values],
        "literal_labeled_allocation_census": {
            "complete_efx_count": sum(labeled_shape_counts.values()),
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(labeled_shape_counts.items())
            },
        },
        "unlabeled_partition_census": {
            "all_nonempty_partitions": len(universe),
            "supported_partitions": len(supported),
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(partition_shape_counts.items())
            },
            "singleton_good_counts": {},
        },
        "singleton_reduction_census": residual_selection,
        "interpretation": (
            "The singleton branch, including the residual-threshold "
            "(6,1,1,1) subfamily, cannot replace the balanced branch."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "results/efx49_common_favorite_real_shape6111_session1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
