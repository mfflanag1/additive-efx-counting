#!/usr/bin/env python3
"""Audit a dual-encoded bounded repeated-resident bridge theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import FAVORITE, N
    from .decide_common_favorite_threshold_pass_hall import residual_partitions
    from .optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import FAVORITE, N
    from decide_common_favorite_threshold_pass_hall import residual_partitions
    from optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )


SCHEMA = "common-favorite-rank1-extended-bridge-collision-cap4-audit-v1"
SOURCE_SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"
SOURCE_STATUS = "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_pool(source):
    return tuple(sorted(
        tuple(sorted(tuple(sorted(bundle)) for bundle in partition))
        for partition in source["singleton_obstruction_partitions"]
    ))


def validate_source(path, pair, encoding, upper):
    source = json.loads(path.read_text())
    expected_counts = (
        (5244, 0, 0)
        if encoding == "duplicate_matching_clauses"
        else (0, 21413, 115368)
    )
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status") != SOURCE_STATUS
        or source.get("solver_status") != "INFEASIBLE"
        or source.get("upper") != upper
        or source.get("conversion_scope") != "radius2_extended_bridge"
        or source.get("hall_obstruction") != "any"
        or source.get("obstruction_encoding") != encoding
        or source.get("cell_symmetry") is not True
        or source.get("identical_residents") is not False
        or source.get("resident_collision") is not False
        or source.get("resident_equality_pair") != pair
        or source.get("blocked_partition_count") != 45
        or source.get("singleton_obstruction_pool_size") != 392
        or source.get("comparison_variables") != 9680
        or (
            source.get("matching_clauses"),
            source.get("hall_selectors"),
            source.get("hall_edge_clauses"),
        )
        != expected_counts
    ):
        raise ValueError(f"source metadata changed: {path}")
    proto_path = Path(source["proto"])
    if (
        not proto_path.is_file()
        or sha256(proto_path) != source["proto_sha256"]
        or proto_path.stat().st_size != source["proto_bytes"]
    ):
        raise AssertionError(f"proto hash or size changed: {path}")
    return source, proto_path


def audit_duplicate_hall_reduction():
    checked = 0
    for owner_mask, duplicate_mask, distinct_mask in itertools.product(
        range(1 << N),
        repeat=3,
    ):
        graph = tuple(
            tuple(bool(mask & (1 << bundle)) for bundle in range(N))
            for mask in (
                owner_mask,
                duplicate_mask,
                duplicate_mask,
                distinct_mask,
            )
        )
        compressed_obstruction = (
            duplicate_mask.bit_count() <= 1
            or owner_mask == 0
            or distinct_mask == 0
            or (owner_mask | distinct_mask).bit_count() <= 1
            or (duplicate_mask | owner_mask).bit_count() <= 2
            or (duplicate_mask | distinct_mask).bit_count() <= 2
            or (duplicate_mask | owner_mask | distinct_mask).bit_count() <= 3
        )
        if compressed_obstruction != (matching_rank(graph) < N):
            raise AssertionError("compressed duplicate-row Hall test is not exact")
        checked += 1
    return checked


def run(
    matching12_path,
    matching23_path,
    hall12_path,
    hall23_path,
    output_path,
    upper=4,
):
    if output_path.exists():
        raise ValueError("output must be new")
    if upper not in {4, 5}:
        raise ValueError("the audited cap must be 4 or 5")
    source_specs = (
        (matching12_path, "12", "duplicate_matching_clauses"),
        (matching23_path, "23", "duplicate_matching_clauses"),
        (hall12_path, "12", "duplicate_hall_selectors"),
        (hall23_path, "23", "duplicate_hall_selectors"),
    )
    sources = []
    protos = []
    for path, pair, encoding in source_specs:
        source, proto = validate_source(path, pair, encoding, upper)
        sources.append(source)
        protos.append(proto)

    pools = tuple(normalized_pool(source) for source in sources)
    if any(pool != pools[0] for pool in pools[1:]) or len(set(pools[0])) != 392:
        raise AssertionError("the four masters do not share one 392-partition pool")
    singleton_universe = {
        tuple(sorted(((FAVORITE,),) + residual))
        for residual in residual_partitions()
    }
    if len(singleton_universe) != 966 or any(
        partition not in singleton_universe for partition in pools[0]
    ):
        raise AssertionError("the shared pool left the singleton universe")

    graph_count = audit_duplicate_hall_reduction()
    nonvacuity_values = (
        (4, 1, 1, 1, 1, 1, 1, 1, 1),
        (4, 2, 2, 2, 1, 1, 1, 1, 1),
        (4, 2, 2, 2, 1, 1, 1, 1, 1),
        (4, 2, 2, 2, 1, 1, 1, 1, 1),
    )
    repairs = repair_partitions("bridge45")
    if not in_cell(nonvacuity_values, repairs):
        raise AssertionError("cap-4 nonvacuity profile left the theorem cell")
    support = supporting_singletons(nonvacuity_values, singleton_partitions())
    if len(support) != 225 or any(
        matching_rank(feasible_graph(nonvacuity_values, partition)) != N
        for partition in support
    ):
        raise AssertionError("cap-4 nonvacuity support census changed")

    source_records = []
    for (path, pair, encoding), source, proto in zip(
        source_specs,
        sources,
        protos,
        strict=True,
    ):
        source_records.append({
            "resident_equality_pair": pair,
            "encoding": encoding,
            "source": str(path),
            "source_sha256": sha256(path),
            "proto": str(proto),
            "proto_sha256": sha256(proto),
            "solver_wall_seconds": source["solver_wall_seconds"],
            "conflicts": source["conflicts"],
            "branches": source["branches"],
        })

    result = {
        "schema": (
            SCHEMA
            if upper == 4
            else "common-favorite-rank1-extended-bridge-collision-cap5-audit-v1"
        ),
        "status": f"DUAL_ENCODED_REPEATED_RESIDENT_CAP{upper}_THEOREM_CANDIDATE",
        "n": 4,
        "m": 9,
        "domain": f"positive integer additive valuations in [1,{upper}]",
        "repair_partition_count": 45,
        "favorite_singleton_partition_count": len(singleton_universe),
        "singleton_obstruction_pool_size": len(pools[0]),
        "resident_case_split": ["12", "23"],
        "case_split_reason": (
            "The cell symmetry orders the three resident rows lexicographically, "
            "so any repeated pair is adjacent and lies in case 12 or case 23."
        ),
        "encodings": [
            "duplicate_matching_clauses",
            "duplicate_hall_selectors",
        ],
        "quotient_matching_count_per_partition": 12,
        "duplicate_hall_case_count": 7,
        "duplicate_hall_selector_count_per_partition": 49,
        "duplicate_hall_graphs_exhaustively_checked": graph_count,
        "sources": source_records,
        "nonvacuity_values": [list(row) for row in nonvacuity_values],
        "nonvacuity_singleton_support_count": len(support),
        "claim": (
            f"Within the positive cap-{upper} rank-one selected cell, if at least two "
            "resident valuation rows coincide, then either one of the 45 "
            "extended-bridge repairs or a favorite-singleton partition supports EFX."
        ),
        "claim_boundary": (
            "This is a dual-encoded CP-SAT theorem candidate without external "
            "proof logs. It does not cover pairwise-distinct residents, values "
            f"above {upper}, the other Hall ranks, or general additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matching12", type=Path, required=True)
    parser.add_argument("--matching23", type=Path, required=True)
    parser.add_argument("--hall12", type=Path, required=True)
    parser.add_argument("--hall23", type=Path, required=True)
    parser.add_argument("--upper", type=int, choices=(4, 5), default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.matching12,
        args.matching23,
        args.hall12,
        args.hall23,
        args.output,
        args.upper,
    )


if __name__ == "__main__":
    main()
