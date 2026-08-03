#!/usr/bin/env python3
"""Audit the rank-one local-six refutation and radius-two successor."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
        local_favorite_pair_conversions,
        transfer_distance,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
        local_favorite_pair_conversions,
        transfer_distance,
    )


SCHEMA = "common-favorite-rank1-local6-boundary-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def singleton_support(values):
    return tuple(
        ((FAVORITE,),) + partition
        for partition in residual_partitions()
        if matching_rank(
            feasible_graph(values, ((FAVORITE,),) + partition)
        )
        == N
    )


def validate_profile(values):
    if (
        any(row[FAVORITE] <= max(row[1:]) for row in values)
        or not threshold_passes(values, 0, RESIDUAL)
        or resident_graph(values) != ((True, False, False),) * 3
    ):
        raise AssertionError("profile left the rank-one mixed cell")


def reconstruct_pool(trace, add_per_iteration=256):
    pool = []
    pool_set = set()
    supported_sequence = []
    for expected_iteration, record in enumerate(trace, 1):
        values = tuple(tuple(row) for row in record["values"])
        validate_profile(values)
        if (
            record["iteration"] != expected_iteration
            or record["singleton_pool_size_before"] != len(pool)
            or any(
                matching_rank(feasible_graph(values, partition)) == N
                for partition in pool
            )
        ):
            raise AssertionError("CEGAR trace ordering changed")
        survivors = [
            partition
            for partition in (
                ((FAVORITE,),) + item for item in residual_partitions()
            )
            if canonical(partition) not in pool_set
            and matching_rank(feasible_graph(values, partition)) == N
        ]
        if len(survivors) != record[
            "supported_unpooled_singleton_partition_count"
        ]:
            raise AssertionError("CEGAR singleton census changed")
        supported_sequence.append(len(survivors))
        for partition in survivors[:add_per_iteration]:
            pool.append(partition)
            pool_set.add(canonical(partition))
    return pool, supported_sequence


def audit_local6(path):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema")
        != "common-favorite-rank1-triple-conversion-cpsat-v1"
        or payload.get("status") != "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
        or payload.get("upper") != 20
        or payload.get("conversion_scope") != "first"
        or payload.get("values") is None
    ):
        raise ValueError("local-six source metadata changed")
    values = core.validate_values(
        payload["values"],
        expected_n=4,
        expected_m=9,
        lower=1,
        upper=20,
    )
    validate_profile(values)
    pool, sequence = reconstruct_pool(payload["cegar_trace"])
    if len(pool) != payload["singleton_obstruction_pool_size"] or len(pool) != 256:
        raise AssertionError("local-six source pool changed")
    if singleton_support(values):
        raise AssertionError("local-six boundary gained singleton EFX")

    conversions = local_favorite_pair_conversions(RESIDUAL)
    conversion_ranks = [
        matching_rank(feasible_graph(values, partition))
        for partition in conversions
    ]
    if conversion_ranks != [3, 3, 3, 3, 2, 3]:
        raise AssertionError("local-six conversion ranks changed")
    source = ((FAVORITE,),) + RESIDUAL
    support = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(4, 9)
        if matching_rank(feasible_graph(values, partition)) == N
    )
    shape_count = Counter(
        "".join(map(str, sorted(map(len, partition), reverse=True)))
        for partition in support
    )
    distance_count = Counter(transfer_distance(source, partition) for partition in support)
    literal_count = independent.count_complete_efx0(values)
    if (
        len(support) != 366
        or shape_count != Counter({"3222": 366})
        or distance_count != Counter({2: 15, 3: 80, 4: 179, 5: 92})
        or literal_count != 1259
    ):
        raise AssertionError("local-six support census changed")
    proto = Path(payload["proto"])
    if not proto.is_file() or sha256(proto) != payload["proto_sha256"]:
        raise AssertionError("local-six CP-SAT proto changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "values": [list(row) for row in values],
        "resident_graph": [list(row) for row in resident_graph(values)],
        "reconstructed_cegar_pool_size": len(pool),
        "supported_singleton_count_sequence": sequence,
        "favorite_singleton_supporting_partition_count": 0,
        "local_conversion_ranks": conversion_ranks,
        "local_conversion_supporting_partition_count": 0,
        "all_supporting_partition_count": len(support),
        "supporting_partition_count_by_shape": dict(sorted(shape_count.items())),
        "supporting_partition_transfer_distance_histogram": {
            str(key): value for key, value in sorted(distance_count.items())
        },
        "minimum_transfer_distance_to_efx_partition": min(distance_count),
        "nearest_efx_partition_count": distance_count[min(distance_count)],
        "complete_efx_allocation_count": literal_count,
        "proto_sha256": payload["proto_sha256"],
    }


def audit_radius2(path):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema")
        != "common-favorite-rank1-triple-conversion-cpsat-v1"
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "UNKNOWN"
        or payload.get("upper") != 20
        or payload.get("conversion_scope") != "radius2"
        or payload.get("blocked_partition_count") != 63
        or payload.get("values") is not None
    ):
        raise ValueError("radius-two source metadata changed")
    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    if len(neighborhood) != 63:
        raise AssertionError("radius-two neighborhood changed")
    pool, sequence = reconstruct_pool(payload["cegar_trace"])
    trace_values = tuple(tuple(row) for row in payload["cegar_trace"][0]["values"])
    if (
        len(pool) != 256
        or len(pool) != payload["singleton_obstruction_pool_size"]
        or any(
            matching_rank(feasible_graph(trace_values, partition)) == N
            for partition in neighborhood
        )
    ):
        raise AssertionError("radius-two boundary changed")
    proto = Path(payload["proto"])
    if not proto.is_file() or sha256(proto) != payload["proto_sha256"]:
        raise AssertionError("radius-two CP-SAT proto changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "blocked_balanced_partition_count": len(neighborhood),
        "reconstructed_cegar_pool_size": len(pool),
        "supported_singleton_count_sequence": sequence,
        "solver_status": payload["solver_status"],
        "solver_wall_seconds": payload["solver_wall_seconds"],
        "proto_sha256": payload["proto_sha256"],
    }


def run(local6_path, radius2_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    result = {
        "schema": SCHEMA,
        "status": "RANK1_LOCAL6_REFUTED_RADIUS2_OPEN",
        "n": 4,
        "m": 9,
        "domain": "positive additive valuations",
        "strict_common_favorite": FAVORITE,
        "local_six_boundary": audit_local6(local6_path),
        "radius_two_boundary": audit_radius2(radius2_path),
        "claim": (
            "Even with no favorite-singleton EFX partition, a threshold-safe "
            "rank-one 3+3+2 state can block all six one-good transfers. Its "
            "nearest EFX repair may require two transfers."
        ),
        "claim_boundary": (
            "The exact local-six matrix is not an EFX counterexample; it has "
            "366 balanced supporting partitions. The radius-two UNKNOWN "
            "endpoint neither proves nor refutes the successor implication."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local6", type=Path, required=True)
    parser.add_argument("--radius2", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.local6, args.radius2, args.output)


if __name__ == "__main__":
    main()
