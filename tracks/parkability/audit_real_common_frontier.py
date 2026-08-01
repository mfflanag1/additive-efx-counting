#!/usr/bin/env python3
"""Audit the first unrestricted-real common-favorite frontier profile."""

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


SCHEMA = "real-common-favorite-4x9-frontier-audit-v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_path: Path) -> dict:
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != "generic-partition-lra-result-v1"
        or source.get("status") != "MASTER_UNKNOWN"
        or source.get("domain") != "strictly positive reals normalized per row"
        or source.get("favorite_pattern") != [0, 0, 0, 0]
        or source.get("require_distinct_item_values") is not True
        or len(source.get("trace", [])) != 1
    ):
        raise AssertionError("the real common-favorite source changed scope")
    values = tuple(tuple(row) for row in source["trace"][0]["values"])
    core.validate_values(values, expected_n=4, expected_m=9, lower=1)
    if any(
        len(set(row)) != 9
        or any(row[0] <= row[good] for good in range(1, 9))
        for row in values
    ):
        raise AssertionError("the frontier matrix lacks the claimed strict cell")

    labeled_shape_counts: Counter[tuple[int, ...]] = Counter()
    examples: dict[tuple[int, ...], tuple[int, ...]] = {}
    singleton_owner_counts: Counter[int] = Counter()
    singleton_owner_slacks: dict[int, list[int]] = {
        agent: [] for agent in range(4)
    }
    for assignment in itertools.product(range(4), repeat=9):
        if independent.is_complete_efx0(values, assignment):
            shape = tuple(sorted(Counter(assignment).values(), reverse=True))
            labeled_shape_counts[shape] += 1
            examples.setdefault(shape, assignment)
            owner = assignment[0]
            if assignment.count(owner) == 1:
                bundles = tuple(
                    tuple(
                        good
                        for good, assigned in enumerate(assignment)
                        if assigned == agent
                    )
                    for agent in range(4)
                )
                threshold = max(
                    sum(values[owner][good] for good in bundles[agent])
                    - min(values[owner][good] for good in bundles[agent])
                    for agent in range(4)
                    if agent != owner
                )
                singleton_owner_counts[owner] += 1
                singleton_owner_slacks[owner].append(
                    values[owner][0] - threshold
                )

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
    complete_efx_count = sum(labeled_shape_counts.values())
    if sum(singleton_owner_counts.values()) != complete_efx_count:
        raise AssertionError("not every literal EFX allocation isolates good 0")
    if set(singleton_owner_counts) != set(range(4)):
        raise AssertionError("not every agent can own the common favorite")
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
    if sum(
        record["threshold_passing_allocations"]
        for record in residual_selection.values()
    ) != complete_efx_count:
        raise AssertionError("singleton reduction census disagrees with literals")
    return {
        "schema": SCHEMA,
        "status": "REAL_FRONTIER_AUDIT_PASSED",
        "claim": (
            "The first unrestricted-real common-favorite countermodel to "
            "the cap-13 pool still admits complete EFX allocations."
        ),
        "source_path": str(source_path.resolve()),
        "source_sha256": file_sha256(source_path),
        "values": [list(row) for row in values],
        "literal_labeled_allocation_census": {
            "complete_efx_count": complete_efx_count,
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(labeled_shape_counts.items())
            },
            "example_assignments": {
                "+".join(map(str, shape)): list(examples[shape])
                for shape in sorted(examples)
            },
            "common_favorite_singleton_owner_counts": {
                str(agent): singleton_owner_counts[agent]
                for agent in range(4)
            },
            "singleton_threshold_slack_ranges": {
                str(agent): {
                    "minimum": min(singleton_owner_slacks[agent]),
                    "maximum": max(singleton_owner_slacks[agent]),
                }
                for agent in range(4)
            },
        },
        "unlabeled_partition_census": {
            "all_nonempty_partitions": len(universe),
            "supported_partitions": len(supported),
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(partition_shape_counts.items())
            },
            "singleton_good_counts": {
                str(good): count
                for good, count in sorted(singleton_good_counts.items())
            },
        },
        "singleton_reduction_census": residual_selection,
        "interpretation": (
            "This is a countermodel only to the frozen 446-partition pool, "
            "not to EFX existence. Every literal EFX allocation isolates "
            "the common favorite, and every agent can be its owner."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("results/efx49_common_favorite_real_sparse_session1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
