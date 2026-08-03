#!/usr/bin/env python3
"""Audit the open radius-two mixed Hall decision boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_threshold_pass_hall import (
        M,
        N,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        M,
        N,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )


SCHEMA = "common-favorite-mixed-hall-radius2-gate-audit-v1"
SHAPE = "332"
RADIUS = 2
OWNER = 0
ADD_PER_ITERATION = 256


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_boundary(path, expected_upper, expected_cegar):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != "common-favorite-threshold-pass-hall-cpsat-v1"
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "UNKNOWN"
        or payload.get("upper") != expected_upper
        or payload.get("selected_residual_shape") != SHAPE
        or payload.get("block_local_transfer_radius") != RADIUS
        or payload.get("blocked_local_partition_count") != 63
        or payload.get("cegar_singletons", False) is not expected_cegar
    ):
        raise ValueError("radius-two decision boundary metadata changed")
    proto = Path(payload["proto"])
    if not proto.is_file() or sha256(proto) != payload["proto_sha256"]:
        raise AssertionError("radius-two CP-SAT proto changed")
    return payload


def canonical(partition):
    return tuple(sorted(tuple(bundle) for bundle in partition))


def audit_trace(payload):
    residual = tuple(residual_partitions())
    selected = SHAPES[SHAPE]
    neighborhood = balanced_transfer_neighborhood(selected, RADIUS)
    if len(neighborhood) != 63:
        raise AssertionError("radius-two neighborhood census changed")
    pool = []
    pool_set = set()
    for expected_iteration, record in enumerate(payload["cegar_trace"], 1):
        if (
            record["iteration"] != expected_iteration
            or record["singleton_pool_size_before"] != len(pool)
        ):
            raise AssertionError("CEGAR trace ordering changed")
        values = tuple(tuple(row) for row in record["values"])
        if (
            len(values) != N
            or any(len(row) != M or row[0] <= max(row[1:]) for row in values)
            or not threshold_passes(values, OWNER, selected)
        ):
            raise AssertionError("CEGAR trace model left the target cell")
        if any(
            matching_rank(feasible_graph(values, partition)) == N
            for partition in neighborhood
        ):
            raise AssertionError("CEGAR trace model supports a blocked repair")
        if any(
            matching_rank(feasible_graph(values, partition)) == N
            for partition in pool
        ):
            raise AssertionError("CEGAR trace model supports a pooled singleton")
        survivors = []
        for partition in residual:
            full_partition = ((0,),) + partition
            key = canonical(full_partition)
            if key in pool_set:
                continue
            if matching_rank(feasible_graph(values, full_partition)) == N:
                survivors.append(full_partition)
        if len(survivors) != record["supported_unpooled_singleton_partition_count"]:
            raise AssertionError("CEGAR survivor census changed")
        for partition in survivors[:ADD_PER_ITERATION]:
            pool.append(partition)
            pool_set.add(canonical(partition))
    if (
        len(pool) != payload["singleton_obstruction_pool_size"]
        or len(pool) != 488
    ):
        raise AssertionError("CEGAR pool size changed")
    serialized = json.dumps(
        [[list(bundle) for bundle in partition] for partition in pool],
        separators=(",", ":"),
    ).encode()
    return {
        "iterations": len(payload["cegar_trace"]),
        "reconstructed_singleton_pool_size": len(pool),
        "reconstructed_singleton_pool_sha256": hashlib.sha256(serialized).hexdigest(),
        "supported_count_sequence": [
            record["supported_unpooled_singleton_partition_count"]
            for record in payload["cegar_trace"]
        ],
    }


def run(cap6_path, cap20_path, cegar_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    cap6 = load_boundary(cap6_path, 6, False)
    cap20 = load_boundary(cap20_path, 20, False)
    cegar = load_boundary(cegar_path, 6, True)
    trace = audit_trace(cegar)
    result = {
        "schema": SCHEMA,
        "status": "RADIUS_TWO_MIXED_HALL_GATE_OPEN",
        "n": N,
        "m": M,
        "selected_residual_shape": SHAPE,
        "blocked_balanced_transfer_radius": RADIUS,
        "blocked_balanced_partition_count": 63,
        "direct_boundaries": [
            {
                "source": str(path),
                "source_sha256": sha256(path),
                "upper": payload["upper"],
                "solver_wall_seconds": payload["solver_wall_seconds"],
                "solver_status": payload["solver_status"],
                "proto_sha256": payload["proto_sha256"],
            }
            for path, payload in ((cap6_path, cap6), (cap20_path, cap20))
        ],
        "cegar_boundary": {
            "source": str(cegar_path),
            "source_sha256": sha256(cegar_path),
            "upper": cegar["upper"],
            "solver_wall_seconds": cegar["solver_wall_seconds"],
            "solver_status": cegar["solver_status"],
            "proto_sha256": cegar["proto_sha256"],
            **trace,
        },
        "claim": (
            "No exact witness or bounded UNSAT proof is known after blocking "
            "all 63 balanced partitions within two transfers of a fixed "
            "threshold-passing 3+3+2 residual partition and all common-"
            "favorite singleton EFX partitions."
        ),
        "claim_boundary": (
            "Three UNKNOWN endpoints are computational boundaries only. "
            "They neither prove the radius-two implication nor refute it."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap6", type=Path, required=True)
    parser.add_argument("--cap20", type=Path, required=True)
    parser.add_argument("--cegar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.cap6, args.cap20, args.cegar, args.output)


if __name__ == "__main__":
    main()
