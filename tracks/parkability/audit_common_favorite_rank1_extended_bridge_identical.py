#!/usr/bin/env python3
"""Audit the dual-encoded identical-resident extended-bridge theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import FAVORITE, N
    from .decide_common_favorite_threshold_pass_hall import residual_partitions
except ImportError:
    import core
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import FAVORITE, N
    from decide_common_favorite_threshold_pass_hall import residual_partitions


SCHEMA = "common-favorite-rank1-extended-bridge-identical-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"
CHECKPOINT_SCHEMA = "common-favorite-rank1-extended-bridge-search-checkpoint-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_pool(source):
    return tuple(sorted(
        tuple(sorted(tuple(sorted(bundle)) for bundle in partition))
        for partition in source["singleton_obstruction_partitions"]
    ))


def validate_source(path, encoding):
    source = json.loads(path.read_text())
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status")
        != "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
        or source.get("solver_status") != "INFEASIBLE"
        or source.get("upper") != 6
        or source.get("conversion_scope") != "radius2_extended_bridge"
        or source.get("hall_obstruction") != "any"
        or source.get("obstruction_encoding") != encoding
        or source.get("cell_symmetry") is not True
        or source.get("identical_residents") is not True
        or source.get("blocked_partition_count") != 45
        or source.get("singleton_obstruction_pool_size") != 392
    ):
        raise ValueError(f"{encoding} source metadata changed")
    proto_path = Path(source["proto"])
    if (
        not proto_path.is_file()
        or sha256(proto_path) != source["proto_sha256"]
        or proto_path.stat().st_size != source["proto_bytes"]
    ):
        raise AssertionError(f"{encoding} proto hash or size changed")
    return source, proto_path


def run(matching_path, hall_path, checkpoint_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    matching, matching_proto = validate_source(
        matching_path,
        "matching_clauses",
    )
    hall, hall_proto = validate_source(hall_path, "hall_selectors")
    matching_pool = normalized_pool(matching)
    hall_pool = normalized_pool(hall)
    if matching_pool != hall_pool or len(set(matching_pool)) != 392:
        raise AssertionError("dual encodings do not share one 392-partition pool")
    singleton_universe = {
        tuple(sorted(((FAVORITE,),) + residual))
        for residual in residual_partitions()
    }
    if any(partition not in singleton_universe for partition in matching_pool):
        raise AssertionError("the theorem pool left the singleton universe")

    checkpoint = json.loads(checkpoint_path.read_text())
    if (
        checkpoint.get("schema") != CHECKPOINT_SCHEMA
        or checkpoint.get("status")
        != "EXTENDED_BRIDGE45_BLOCKED_WITH_SINGLETON_REPAIRS"
    ):
        raise ValueError("checkpoint metadata changed")
    values = core.validate_values(
        checkpoint["values"], expected_n=4, expected_m=9, lower=1, upper=6
    )
    if values[1] != values[2] or values[1] != values[3]:
        raise AssertionError("checkpoint residents ceased to be identical")
    checkpoint_support = tuple(
        tuple(sorted(((FAVORITE,),) + residual))
        for residual in residual_partitions()
        if matching_rank(
            feasible_graph(values, ((FAVORITE,),) + residual)
        )
        == N
    )
    if len(checkpoint_support) != 6 or any(
        partition not in set(matching_pool) for partition in checkpoint_support
    ):
        raise AssertionError("checkpoint no longer supplies the six-support upper bound")

    result = {
        "schema": SCHEMA,
        "status": "DUAL_ENCODED_IDENTICAL_RESIDENT_CAP6_THEOREM_CANDIDATE",
        "n": 4,
        "m": 9,
        "domain": "positive integer additive valuations in [1,6]",
        "matching_source": str(matching_path),
        "matching_source_sha256": sha256(matching_path),
        "matching_proto": str(matching_proto),
        "matching_proto_sha256": sha256(matching_proto),
        "matching_solver_wall_seconds": matching["solver_wall_seconds"],
        "hall_source": str(hall_path),
        "hall_source_sha256": sha256(hall_path),
        "hall_proto": str(hall_proto),
        "hall_proto_sha256": sha256(hall_proto),
        "hall_solver_wall_seconds": hall["solver_wall_seconds"],
        "singleton_obstruction_pool_size": len(matching_pool),
        "favorite_singleton_partition_count": len(singleton_universe),
        "repair_partition_count": 45,
        "identical_residents": True,
        "checkpoint": str(checkpoint_path),
        "checkpoint_sha256": sha256(checkpoint_path),
        "checkpoint_singleton_support_count": len(checkpoint_support),
        "claim": (
            "Within the positive cap-6 rank-one selected cell, if the three "
            "resident valuation rows are identical, then either one of the "
            "45 extended-bridge repairs or a favorite-singleton partition "
            "supports EFX."
        ),
        "claim_boundary": (
            "This is a dual-encoded CP-SAT theorem candidate without external "
            "proof logs. It does not cover unequal residents, values above 6, "
            "the other Hall ranks, or general additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matching", type=Path, required=True)
    parser.add_argument("--hall", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.matching, args.hall, args.checkpoint, args.output)


if __name__ == "__main__":
    main()
