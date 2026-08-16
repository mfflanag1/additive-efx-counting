#!/usr/bin/env python3
"""Audit the reduced cap-4/cap-5 cores and the cap-6 shape ladder."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        OWNER,
        RESIDUAL,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import threshold_passes
    from .optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        OWNER,
        RESIDUAL,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import threshold_passes
    from optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )


SCHEMA = "common-favorite-rank1-core-shape-ladder-audit-v1"
CORE_SCHEMA = "common-favorite-rank1-extended-bridge-collision-core-v1"
DECISION_SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_partition(raw_partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in raw_partition))


def decoded_partitions(payload, field):
    partitions = tuple(
        canonical_partition(partition) for partition in payload[field]
    )
    if len(partitions) != len(set(partitions)):
        raise AssertionError(f"{field} contains duplicate partitions")
    return partitions


def shape(partition):
    return tuple(sorted(map(len, partition), reverse=True))


def shape_counts(partitions):
    return {
        "+".join(map(str, key)): value
        for key, value in sorted(Counter(map(shape, partitions)).items())
    }


def literal_edge(values, observer, own_bundle, partition):
    own_value = sum(values[observer][good] for good in own_bundle)
    return all(
        own_value
        >= sum(
            values[observer][other]
            for other in compared_bundle
            if other != removed
        )
        for compared_bundle in partition
        for removed in compared_bundle
    )


def literal_support(values, partition):
    return any(
        all(
            literal_edge(values, observer, partition[bundle], partition)
            for observer, bundle in enumerate(matching)
        )
        for matching in itertools.permutations(range(N))
    )


def validate_proto(payload, source_path):
    proto_path = Path(payload["proto"])
    if (
        not proto_path.is_file()
        or sha256(proto_path) != payload["proto_sha256"]
        or proto_path.stat().st_size != payload["proto_bytes"]
    ):
        raise AssertionError(f"proto hash or size changed: {source_path}")
    return {
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "proto": str(proto_path),
        "proto_sha256": sha256(proto_path),
    }


def validate_core(path, upper, encoding, size):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != CORE_SCHEMA
        or payload.get("status") != "SINGLETON_ASSUMPTION_CORE_EXTRACTED"
        or payload.get("solver_status") != "INFEASIBLE"
        or payload.get("replay_solver_status") != "INFEASIBLE"
        or payload.get("upper") != upper
        or payload.get("resident_equality_pair") != "12"
        or payload.get("obstruction_encoding") != encoding
        or payload.get("repair_partition_count") != 45
        or payload.get("singleton_obstruction_core_size") != size
    ):
        raise ValueError(f"core metadata changed: {path}")
    partitions = decoded_partitions(
        payload,
        "singleton_obstruction_core_partitions",
    )
    if len(partitions) != size:
        raise AssertionError(f"core size changed: {path}")
    record = validate_proto(payload, path)
    record.update({
        "encoding": encoding,
        "core_size": size,
        "solver_wall_seconds": payload["solver_wall_seconds"],
        "replay_solver_wall_seconds": payload["replay_solver_wall_seconds"],
    })
    return payload, partitions, record


def validate_hall_replay(path, expected_partitions):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != DECISION_SCHEMA
        or payload.get("status")
        != "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
        or payload.get("solver_status") != "INFEASIBLE"
        or payload.get("upper") != 5
        or payload.get("conversion_scope") != "radius2_extended_bridge"
        or payload.get("obstruction_encoding") != "duplicate_hall_selectors"
        or payload.get("resident_equality_pair") != "12"
        or payload.get("singleton_obstruction_pool_size") != 112
    ):
        raise ValueError(f"Hall replay metadata changed: {path}")
    partitions = decoded_partitions(payload, "singleton_obstruction_partitions")
    if partitions != expected_partitions:
        raise AssertionError("the cap-5 Hall replay does not use the matching core")
    record = validate_proto(payload, path)
    record.update({
        "encoding": "duplicate_hall_selectors",
        "core_size": 112,
        "solver_wall_seconds": payload["solver_wall_seconds"],
    })
    return payload, record


def validate_trace(path, before, final_pool, expected_shapes, expected_values):
    payload = json.loads(path.read_text())
    trace = payload.get("cegar_trace", [])
    if (
        payload.get("schema") != DECISION_SCHEMA
        or payload.get("status") != "ITERATION_LIMIT"
        or payload.get("solver_status") != "OPTIMAL"
        or payload.get("upper") != 6
        or payload.get("conversion_scope") != "radius2_extended_bridge"
        or payload.get("obstruction_encoding") != "duplicate_hall_selectors"
        or payload.get("resident_equality_pair") != "12"
        or payload.get("singleton_obstruction_pool_size") != final_pool
        or len(trace) != 1
        or trace[0].get("singleton_pool_size_before") != before
        or trace[0].get("values") != expected_values
    ):
        raise ValueError(f"cap-6 trace metadata changed: {path}")

    values = tuple(tuple(row) for row in expected_values)
    if (
        any(row[FAVORITE] <= max(row[1:]) for row in values)
        or not threshold_passes(values, OWNER, RESIDUAL)
        or resident_graph(values) != ((True, False, False),) * 3
        or values[1] != values[2]
    ):
        raise AssertionError(f"cap-6 trace left the rank-one cell: {path}")

    repairs = repair_partitions("bridge45")
    if any(
        literal_support(values, partition)
        or matching_rank(feasible_graph(values, partition)) == N
        for partition in repairs
    ):
        raise AssertionError(f"a cap-6 trace supports a bridge repair: {path}")

    universe = singleton_partitions()
    vector_support = supporting_singletons(values, universe)
    literal_support_set = tuple(
        partition for partition in universe if literal_support(values, partition)
    )
    if vector_support != literal_support_set:
        raise AssertionError(f"literal and graph singleton censuses disagree: {path}")
    if (
        len(vector_support)
        != trace[0]["supported_unpooled_singleton_partition_count"]
        or shape_counts(vector_support) != expected_shapes
    ):
        raise AssertionError(f"cap-6 trace support census changed: {path}")

    pool = decoded_partitions(payload, "singleton_obstruction_partitions")
    before_pool = set(pool[:before])
    if any(partition in before_pool for partition in vector_support):
        raise AssertionError(f"cap-6 trace supports an active cut: {path}")

    record = validate_proto(payload, path)
    record.update({
        "cuts_before_solve": before,
        "cuts_after_learning": final_pool,
        "solver_wall_seconds": trace[0]["solver_wall_seconds"],
        "values": expected_values,
        "identical_residents": values[1] == values[2] == values[3],
        "new_singleton_support_count": len(vector_support),
        "new_singleton_support_by_shape": expected_shapes,
    })
    return record


def run(
    cap4_core_path,
    cap5_matching_core_path,
    cap5_hall_replay_path,
    cap6_paths,
    output_path,
):
    if output_path.exists():
        raise ValueError("output must be new")
    cap4, cap4_partitions, cap4_record = validate_core(
        cap4_core_path,
        4,
        "duplicate_hall_selectors",
        29,
    )
    cap5, cap5_partitions, cap5_matching_record = validate_core(
        cap5_matching_core_path,
        5,
        "duplicate_matching_clauses",
        112,
    )
    _, cap5_hall_record = validate_hall_replay(
        cap5_hall_replay_path,
        cap5_partitions,
    )

    singleton_universe = set(singleton_partitions())
    if (
        not set(cap4_partitions) <= singleton_universe
        or not set(cap5_partitions) <= singleton_universe
    ):
        raise AssertionError("a reduced core left the singleton universe")
    cap5_balanced = {
        partition for partition in cap5_partitions if shape(partition) == (3, 3, 2, 1)
    }
    if cap5_balanced != set(cap4_partitions):
        raise AssertionError("the cap-5 balanced layer is not the cap-4 core")
    if shape_counts(cap4_partitions) != {"3+3+2+1": 29}:
        raise AssertionError("cap-4 core shape census changed")
    cap5_shapes = {
        "3+3+2+1": 29,
        "4+2+2+1": 35,
        "4+3+1+1": 48,
    }
    if shape_counts(cap5_partitions) != cap5_shapes:
        raise AssertionError("cap-5 core shape census changed")

    trace_specs = (
        (
            112,
            113,
            {"5+2+1+1": 6},
            [
                [6, 5, 1, 1, 1, 1, 1, 4, 1],
                [6, 5, 1, 1, 1, 1, 1, 4, 1],
                [6, 5, 1, 1, 1, 1, 1, 4, 1],
                [6, 5, 1, 1, 1, 1, 1, 4, 1],
            ],
        ),
        (
            118,
            145,
            {"3+3+2+1": 12, "4+2+2+1": 15},
            [
                [6, 1, 1, 1, 1, 1, 1, 3, 1],
                [6, 5, 5, 1, 4, 4, 1, 1, 3],
                [6, 5, 5, 1, 4, 4, 1, 1, 3],
                [6, 5, 5, 1, 4, 4, 1, 1, 3],
            ],
        ),
        (
            145,
            196,
            {"3+3+2+1": 30, "4+3+1+1": 20, "5+2+1+1": 1},
            [
                [6, 1, 1, 1, 1, 1, 1, 5, 1],
                [6, 4, 4, 1, 1, 1, 1, 5, 1],
                [6, 4, 4, 1, 1, 1, 1, 5, 1],
                [6, 4, 4, 1, 1, 1, 1, 5, 1],
            ],
        ),
        (
            196,
            211,
            {"4+2+2+1": 15},
            [
                [6, 1, 1, 1, 2, 2, 1, 4, 1],
                [6, 4, 4, 4, 1, 1, 3, 1, 4],
                [6, 4, 4, 4, 1, 1, 3, 1, 4],
                [6, 4, 4, 4, 1, 1, 3, 1, 4],
            ],
        ),
    )
    trace_records = [
        validate_trace(path, *spec)
        for path, spec in zip(cap6_paths, trace_specs, strict=True)
    ]

    result = {
        "schema": SCHEMA,
        "status": "DUAL_ENCODED_CAP5_CORE_AND_CAP6_SAT_LADDER_AUDITED",
        "n": 4,
        "m": 9,
        "selected_cell": {
            "favorite": FAVORITE,
            "owner": OWNER,
            "residual_partition": [list(bundle) for bundle in RESIDUAL],
            "resident_equality_pair": "12",
            "repair_family": "radius2_extended_bridge",
            "repair_partition_count": 45,
        },
        "cap4": {
            "core_size": len(cap4_partitions),
            "core_shape_counts": shape_counts(cap4_partitions),
            "source": cap4_record,
            "claim_boundary": cap4["claim_boundary"],
        },
        "cap5": {
            "shared_core_size": len(cap5_partitions),
            "core_shape_counts": shape_counts(cap5_partitions),
            "balanced_layer_equals_cap4_core": True,
            "matching_source": cap5_matching_record,
            "hall_replay_source": cap5_hall_record,
            "claim": (
                "At cap 5, these same 112 singleton obstructions plus the 45 "
                "extended-bridge obstructions are infeasible in both the "
                "duplicate-matching and duplicate-Hall encodings."
            ),
            "claim_boundary": cap5["claim_boundary"],
        },
        "cap6": {
            "status": "SAT_THROUGH_196_CUTS_211_CUT_MASTER_NOT_RUN",
            "trace": trace_records,
            "last_solved_cut_count": 196,
            "last_new_singleton_support_count": 15,
            "current_unsolved_pool_size": 211,
            "all_trace_models_have_identical_residents": all(
                record["identical_residents"] for record in trace_records
            ),
        },
        "analytic_consequences": [
            "The 29-partition cap-4 menu is not cap-free: the first cap-5 model has 52 unpooled singleton repairs.",
            "A shape-only extension is false: later cap-6 models escape through new origin placements in shapes already present in the cap-5 core.",
            "The cap-5 core adds only the 4+2+2+1 and 4+3+1+1 layers to the exact cap-4 balanced core.",
            "Every audited cap-6 adversary has three identical resident rows, isolating origin-sensitive bundle comparisons inside the repeated-row subcell.",
        ],
        "claim_boundary": (
            "This audit sharpens a bounded repeated-resident local theorem and "
            "records a SAT cap-6 CEGAR frontier. It does not prove the 211-cut "
            "cap-6 master infeasible, does not cover pairwise-distinct residents "
            "or values above 6, and does not resolve complete additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap4-core", type=Path, required=True)
    parser.add_argument("--cap5-matching-core", type=Path, required=True)
    parser.add_argument("--cap5-hall-replay", type=Path, required=True)
    parser.add_argument("--cap6-stage", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.cap6_stage) != 4:
        raise ValueError("exactly four cap-6 stage paths are required")
    run(
        args.cap4_core,
        args.cap5_matching_core,
        args.cap5_hall_replay,
        tuple(args.cap6_stage),
        args.output,
    )


if __name__ == "__main__":
    main()
