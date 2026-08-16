#!/usr/bin/env python3
"""Audit the failure of the fixed 3+3+2 one-transfer repair rule."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_common_favorite_mixed_hall_boundaries import audit_case
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        N,
        local_favorite_pair_conversions,
    )
except ImportError:
    from anneal import atomic_json
    from audit_common_favorite_mixed_hall_boundaries import audit_case
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        N,
        local_favorite_pair_conversions,
    )


SCHEMA = "common-favorite-mixed-hall-local6-boundary-audit-v1"


def run(source_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    source = json.loads(source_path.read_text())
    if (
        source.get("selected_residual_shape") != "332"
        or source.get("block_local_favorite_pair_conversions") is not True
        or source.get("local_favorite_pair_conversion_count") != 6
    ):
        raise ValueError("source is not the local-six boundary")
    case = audit_case(source_path)
    values = tuple(tuple(row) for row in case["values"])
    selected = tuple(
        tuple(bundle) for bundle in source["selected_residual_partition"]
    )
    conversions = local_favorite_pair_conversions(selected)
    supporting = [
        partition
        for partition in conversions
        if matching_rank(feasible_graph(values, partition)) == N
    ]
    if supporting or case["minimum_transfer_distance_to_efx_partition"] != 2:
        raise AssertionError("the fixed local-six boundary changed")
    result = {
        "schema": SCHEMA,
        "status": "FIXED_332_ONE_TRANSFER_RULE_EXACTLY_REFUTED",
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "values": case["values"],
        "selected_residual_partition": source["selected_residual_partition"],
        "local_favorite_pair_conversions": [
            [list(bundle) for bundle in partition] for partition in conversions
        ],
        "local_favorite_pair_conversion_count": 6,
        "local_favorite_pair_support_count": 0,
        "favorite_singleton_supporting_partition_count": 0,
        "all_supporting_partition_count": case["all_supporting_partition_count"],
        "supporting_partition_count_by_shape": case[
            "supporting_partition_count_by_shape"
        ],
        "minimum_transfer_distance_to_efx_partition": 2,
        "nearest_efx_partition_count": case["nearest_efx_partition_count"],
        "nearest_efx_partition_sample": case["nearest_efx_partition_sample"],
        "complete_efx_allocation_count": case["complete_efx_allocation_count"],
        "claim": (
            "A threshold-passing 3+3+2 residual partition can have deficient "
            "resident Hall rank while all six one-good transfers from a triple "
            "onto the common favorite remain EFX-obstructed."
        ),
        "claim_boundary": (
            "This refutes only the fixed-partition one-transfer repair rule. "
            "The profile still has complete balanced EFX allocations at "
            "transfer distance two."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
