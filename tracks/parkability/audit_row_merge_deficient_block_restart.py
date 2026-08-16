#!/usr/bin/env python3
"""Audit a generic-wall refutation of deficient-block partial restart."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        graph,
        matching_count,
        minimal_hall_witnesses,
        transfer_distance,
    )
    from .decide_row_merge_partial_entry_radius import (
        deficient_block_partitions,
        delete_good,
        global_wall_isolation,
        partial_partitions,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        graph,
        matching_count,
        minimal_hall_witnesses,
        transfer_distance,
    )
    from decide_row_merge_partial_entry_radius import (
        deficient_block_partitions,
        delete_good,
        global_wall_isolation,
        partial_partitions,
    )


SCHEMA = "row-merge-deficient-block-restart-refutation-audit-v1"


def run(source_path: Path, output_path: Path) -> dict:
    if output_path.exists():
        raise ValueError("output path must be new")
    source = json.loads(source_path.read_text())
    if source.get("status") != "DEFICIENT_BLOCK_RESTART_REFUTATION_WITNESS":
        raise ValueError("a deficient-block restart witness is required")
    n = source["n"]
    m = source["m"]
    wall = core.validate_values(
        source["wall_values"], expected_n=n, expected_m=m, lower=1
    )
    post = core.validate_values(
        source["post_wall_values"], expected_n=n, expected_m=m, lower=1
    )
    partition = tuple(tuple(bundle) for bundle in source["wall_partition"])
    moving = source["moving_agent"]
    moving_bundle = source["moving_bundle_index"]
    perturbed_good = source["perturbed_good"]
    critical_good = source["critical_good"]
    witness_agents = tuple(source["minimal_hall_witness_agents"])
    block_indices = tuple(source["deficient_block_bundle_indices"])
    witness_size = len(witness_agents)
    if witness_agents != tuple(range(witness_size)) or block_indices != tuple(
        range(witness_size)
    ):
        raise ValueError("the audit expects the canonical deficient block")
    u = partition[moving_bundle]
    w = tuple(good for good in partition[1] if good != critical_good)
    if (
        sum(wall[moving][good] for good in u)
        != sum(wall[moving][good] for good in w)
        or post[moving][perturbed_good] <= wall[moving][perturbed_good]
        or any(
            post[agent][good] != wall[agent][good]
            for agent in range(n)
            for good in range(m)
            if (agent, good) != (moving, perturbed_good)
        )
    ):
        raise AssertionError("the designated wall perturbation is invalid")
    isolation_failures = global_wall_isolation(wall, post, u, w)
    if isolation_failures:
        raise AssertionError("the witness crosses an additional subset-sum wall")

    wall_graph = graph(wall, partition)
    post_graph = graph(post, partition)
    changed = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(n)
        for bundle in range(n)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if (
        any(not wall_graph[agent][agent] for agent in range(n))
        or changed != ((moving, moving_bundle, True, False),)
    ):
        raise AssertionError("the wall EFX allocation or single-edge loss failed")
    witnesses = minimal_hall_witnesses(post_graph)
    expected_witness = (witness_agents, tuple(range(1, witness_size)))
    if expected_witness not in witnesses:
        raise AssertionError("the designated minimal Hall witness is absent")

    block_goods = tuple(
        good for bundle in partition[:witness_size] for good in bundle
    )
    block_candidate_count = 0
    block_allocation_count = 0
    per_deleted_good = {}
    for deleted_good in block_goods:
        support_count = 0
        allocation_count = 0
        candidates = deficient_block_partitions(
            partition, witness_size, deleted_good
        )
        block_candidate_count += len(candidates)
        for candidate in candidates:
            count = matching_count(graph(post, candidate))
            support_count += bool(count)
            allocation_count += count
        block_allocation_count += allocation_count
        per_deleted_good[str(deleted_good)] = {
            "candidate_partition_count": len(candidates),
            "supporting_partition_count": support_count,
            "supporting_allocation_count": allocation_count,
        }
    if block_candidate_count != 150 or block_allocation_count != 0:
        raise AssertionError("the deficient-block restart census failed")

    global_support_count = 0
    global_allocation_count = 0
    global_histogram = Counter()
    nearest = None
    literal_counts = independent.count_removed_good_efx0_bases(post)
    per_good_global_counts = []
    for deleted_good in range(m):
        origin = delete_good(partition, deleted_good)
        good_allocation_count = 0
        for candidate in partial_partitions(m, deleted_good):
            count = matching_count(graph(post, candidate))
            if not count:
                continue
            distance = transfer_distance(origin, candidate)
            global_support_count += 1
            global_allocation_count += count
            good_allocation_count += count
            global_histogram[distance] += 1
            record = (distance, deleted_good, candidate)
            if nearest is None or record < nearest:
                nearest = record
        per_good_global_counts.append(good_allocation_count)
    if tuple(per_good_global_counts) != literal_counts or nearest is None:
        raise AssertionError("the independent global partial-EFX census failed")

    complete_partition_count = 0
    complete_allocation_count = 0
    for candidate in core.iter_unlabeled_nonempty_partitions(n, m):
        count = matching_count(graph(post, candidate))
        if count:
            complete_partition_count += 1
            complete_allocation_count += count
    if complete_allocation_count != independent.count_complete_efx0(post):
        raise AssertionError("the independent complete-EFX census failed")

    result = {
        "schema": SCHEMA,
        "status": "DEFICIENT_BLOCK_RESTART_REFUTATION_AUDITED",
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "n": n,
        "m": m,
        "generic_single_wall_verified": True,
        "wall_feasibility_graph": [list(row) for row in wall_graph],
        "post_feasibility_graph": [list(row) for row in post_graph],
        "changed_original_partition_edges": [list(item) for item in changed],
        "minimal_hall_witnesses": [
            {"agents": list(agents), "neighbors": list(neighbors)}
            for agents, neighbors in witnesses
        ],
        "deficient_block_bundle_indices": list(block_indices),
        "deficient_block_deleted_goods": list(block_goods),
        "deficient_block_candidate_partition_count": block_candidate_count,
        "deficient_block_supporting_allocation_count": 0,
        "deficient_block_census_by_deleted_good": per_deleted_good,
        "global_partial_efx_partition_count": global_support_count,
        "global_partial_efx_allocation_count": global_allocation_count,
        "global_partial_efx_allocation_count_by_deleted_good": list(
            literal_counts
        ),
        "global_partial_efx_transfer_distance_histogram": {
            str(distance): global_histogram[distance]
            for distance in sorted(global_histogram)
        },
        "nearest_global_partial_efx_transfer_distance": nearest[0],
        "nearest_global_partial_efx_deleted_good": nearest[1],
        "nearest_global_partial_efx_partition": [
            list(bundle) for bundle in nearest[2]
        ],
        "complete_efx_supporting_partition_count": complete_partition_count,
        "complete_efx_allocation_count": complete_allocation_count,
        "claim": (
            "All 150 one-good deletions and arbitrary repartitions confined "
            "to the deficient block fail, while complete EFX allocations exist."
        ),
        "claim_boundary": (
            "This refutes deficient-block partial restart in one generic "
            "seven-good Hall-size-three cell. It does not refute a global "
            "partial restart or complete EFX continuation."
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
