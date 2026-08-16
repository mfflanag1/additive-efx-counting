#!/usr/bin/env python3
"""Solver-free audit of a row merge with no stable partition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_row_merge_interpolation import path_audit
    from .audit_row_merge_single_wall_radius import graph, matching_count
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_row_merge_interpolation import path_audit
    from audit_row_merge_single_wall_radius import graph, matching_count


SCHEMA = "row-merge-no-stable-partition-audit-v1"


def partition_support(values):
    n = len(values)
    m = len(values[0])
    support = {}
    for partition in core.iter_unlabeled_nonempty_partitions(n, m):
        count = matching_count(graph(values, partition))
        if count:
            support[partition] = count
    return support


def partition_records(support):
    return [
        {
            "partition": [list(bundle) for bundle in partition],
            "supporting_matching_count": support[partition],
        }
        for partition in sorted(support)
    ]


def run(source_path: Path, output_path: Path) -> dict:
    if output_path.exists():
        raise ValueError("output path must be new")
    source = json.loads(source_path.read_text())
    if source.get("status") != "NO_STABLE_PARTITION_WITNESS":
        raise ValueError("a no-stable-partition witness is required")
    values = core.validate_values(
        source["values"],
        expected_n=source["n"],
        expected_m=source["m"],
        lower=1,
    )
    moving = source["moving_agent"]
    base = source["base_agent"]
    merged = [list(row) for row in values]
    merged[moving] = list(merged[base])
    target_support = partition_support(values)
    merged_support = partition_support(merged)
    shared = set(target_support) & set(merged_support)
    target_literal_count = independent.count_complete_efx0(values)
    merged_literal_count = independent.count_complete_efx0(merged)
    if (
        shared
        or sum(target_support.values()) != target_literal_count
        or sum(merged_support.values()) != merged_literal_count
    ):
        raise AssertionError("endpoint support census failed")

    interpolation = path_audit(values, moving, base)
    if (
        not interpolation["covers_unit_interval"]
        or interpolation["union_component_count"] != 1
        or interpolation["full_path_partition_count"] != 0
        or interpolation["stable_partition"] is not None
        or interpolation["efx_allocation_count_at_zero"] != merged_literal_count
        or interpolation["efx_allocation_count_at_one"] != target_literal_count
    ):
        raise AssertionError("exact interpolation audit failed")

    result = {
        "schema": SCHEMA,
        "status": "NO_STABLE_PARTITION_AUDITED",
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "n": len(values),
        "m": len(values[0]),
        "moving_agent": moving,
        "base_agent": base,
        "merged_endpoint_values": merged,
        "target_endpoint_partition_count": len(target_support),
        "target_endpoint_allocation_count": target_literal_count,
        "merged_endpoint_partition_count": len(merged_support),
        "merged_endpoint_allocation_count": merged_literal_count,
        "shared_endpoint_partition_count": 0,
        "target_endpoint_partitions": partition_records(target_support),
        "merged_endpoint_partitions": partition_records(merged_support),
        "path_supporting_interval_count": interpolation[
            "supporting_interval_count"
        ],
        "path_union_components": interpolation["union_components"],
        "path_greedy_cover_size": interpolation["greedy_cover_size"],
        "path_greedy_cover": interpolation["greedy_cover"],
        "full_path_partition_count": interpolation[
            "full_path_partition_count"
        ],
        "claim": (
            "No unlabeled partition supports EFX at both endpoints, while two "
            "exact allocation intervals cover the entire row merge."
        ),
        "claim_boundary": (
            "This refutes the fixed-partition row-merge conjecture. It does "
            "not refute row-merge continuation with changing partitions or "
            "complete additive EFX existence."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
