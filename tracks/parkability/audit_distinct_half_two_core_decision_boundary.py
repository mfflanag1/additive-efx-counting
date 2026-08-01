#!/usr/bin/env python3
"""Replay exact and bounded decision boundaries for the two-core target."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal_distinct_half_rank_augmentation import Landscape
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .analyze_distinct_half_two_core_seed_pool import analyze as analyze_seed_pool
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_two_core_cegar import two_core_witnesses
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal_distinct_half_rank_augmentation import Landscape
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from analyze_distinct_half_two_core_seed_pool import analyze as analyze_seed_pool
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_two_core_cegar import two_core_witnesses
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-two-core-decision-boundary-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_cegar(path, expected_status, expected_counts, expected_pool):
    payload = json.loads(path.read_text())
    universe = tuple(favorite_pair_balanced_universe())
    pool = set()
    trace_summary = []
    for position, trace in enumerate(payload["trace"], start=1):
        values = core.validate_values(
            trace["values"], expected_n=4, expected_m=9, lower=1
        )
        audit_branch(values)
        if two_core_witnesses(values):
            raise AssertionError("CEGAR trace model has a two-core witness")
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if (
            trace["iteration"] != position
            or trace["pool_size_before"] != len(pool)
            or trace["favorite_pair_efx_survivors"] != len(survivors)
        ):
            raise AssertionError("CEGAR trace replay changed")
        trace_summary.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])

    smt2_path = Path(payload["smt2_path"])
    if (
        payload["status"] != expected_status
        or trace_summary != expected_counts
        or len(pool) != expected_pool
        or payload["pool_size"] != expected_pool
        or sha256(smt2_path) != payload["smt2_sha256"]
        or payload["values"] is not None
        or payload["literal_complete_efx_count"] is not None
    ):
        raise AssertionError("CEGAR endpoint changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "status": payload["status"],
        "reason_unknown": payload["reason_unknown"],
        "obstruction_encoding": payload["favorite_pair_obstruction_encoding"],
        "trace_survivor_counts": trace_summary,
        "replayed_pool_size": len(pool),
        "smt2_sha256": payload["smt2_sha256"],
    }


def audit_cpsat(path):
    payload = json.loads(path.read_text())
    proto_path = Path(payload["proto_path"])
    if (
        payload["status"] != "CP_SAT_UNKNOWN"
        or payload["solver_status"] != "UNKNOWN"
        or payload["cap"] != 20
        or payload["two_core_candidate_count"] != 168
        or payload.get("time_limit_seconds") != 300.0
        or payload["elapsed_seconds"] < 300
        or payload["values"] is not None
        or sha256(proto_path) != payload["proto_sha256"]
    ):
        raise AssertionError("CP-SAT endpoint changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "status": payload["status"],
        "cap": payload["cap"],
        "conflicts": payload["conflicts"],
        "branches": payload["branches"],
        "elapsed_seconds": payload["elapsed_seconds"],
        "proto_sha256": payload["proto_sha256"],
    }


def audit_cpsat_cegar(path):
    payload = json.loads(path.read_text())
    resume_path = Path(payload["resume_source"])
    resume = json.loads(resume_path.read_text())
    resume_proto = Path(resume["proto_path"])
    if (
        sha256(resume_path) != payload["resume_source_sha256"]
        or resume.get("trace") != payload["trace"]
        or sha256(resume_proto) != resume["proto_sha256"]
    ):
        raise AssertionError("CP-SAT CEGAR resume provenance changed")
    seed_paths = tuple(Path(source["path"]) for source in payload["seed_sources"])
    for source, seed_path in zip(payload["seed_sources"], seed_paths):
        if sha256(seed_path) != source["sha256"]:
            raise AssertionError("CP-SAT CEGAR seed hash changed")
    universe = tuple(favorite_pair_balanced_universe())
    seed_supported = set()
    for seed_path in seed_paths:
        seed_supported.update(
            supported_partitions(load_values(seed_path), list(universe))
        )
    pool = set(universe).difference(seed_supported)
    trace_counts = []
    final_values = None
    for position, trace in enumerate(payload["trace"], start=1):
        values = core.validate_values(
            trace["values"], expected_n=4, expected_m=9, lower=1
        )
        if max(max(row) for row in values) > payload["cap"]:
            raise AssertionError("CP-SAT CEGAR trace exceeds cap")
        audit_branch(values)
        if two_core_witnesses(values):
            raise AssertionError("CP-SAT CEGAR trace has a two-core witness")
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if (
            trace["iteration"] != position
            or trace["pool_size_before"] != len(pool)
            or trace["favorite_pair_efx_survivors"] != len(survivors)
        ):
            raise AssertionError("CP-SAT CEGAR trace replay changed")
        trace_counts.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
        final_values = values
    proto_path = Path(payload["proto_path"])
    if (
        payload["status"] != "CP_SAT_UNKNOWN"
        or payload["solver_status"] != "UNKNOWN"
        or payload["cap"] != 20
        or payload["seed_mode"] != "complement"
        or payload["seed_supported_union_size"] != 785
        or trace_counts != [398, 143, 20]
        or len(pool) != 331
        or payload["pool_size"] != 331
        or payload["iterations"] != 4
        or payload["two_core_candidate_count"] != 168
        or payload.get("two_core_scope") != "all"
        or payload.get("symmetry_breaking")
        != [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ]
        or payload.get("time_limit_seconds") != 900.0
        or payload["elapsed_seconds"] < 900
        or payload["values"] is not None
        or payload["literal_complete_efx_count"] is not None
        or sha256(proto_path) != payload["proto_sha256"]
    ):
        raise AssertionError("CP-SAT CEGAR endpoint changed")
    if final_values is None:
        raise AssertionError("CP-SAT CEGAR trace is empty")
    final_repairs = tuple(
        supported_partitions(final_values, list(universe))
    )
    partner_counts = Counter()
    triple_counts = Counter()
    for partition in final_repairs:
        favorite_pair = next(bundle for bundle in partition if 0 in bundle)
        partner_counts[next(good for good in favorite_pair if good != 0)] += 1
        triple_counts[next(bundle for bundle in partition if len(bundle) == 3)] += 1
    balanced_analyzer = Landscape("balanced")
    balanced_landscape = balanced_analyzer.audit(final_values)
    balanced_repairs = tuple(
        supported_partitions(final_values, list(balanced_analyzer.universe))
    )
    triple_cell_counts = Counter(
        tuple(good for good in favorite_bundle if good != 0)
        for partition in balanced_repairs
        for favorite_bundle in partition
        if 0 in favorite_bundle and len(favorite_bundle) == 3
    )
    full_triple_cells = tuple(
        cell for cell, count in sorted(triple_cell_counts.items()) if count == 15
    )
    literal_count = independent.count_complete_efx0(final_values)
    if (
        len(final_repairs) != 20
        or balanced_landscape["favorite_pair_perfect_partition_count"] != 20
        or len(balanced_repairs) != 35
        or full_triple_cells != ((7, 8),)
        or balanced_landscape["two_core_tutte_low_pair_count"] != 0
        or literal_count <= 0
    ):
        raise AssertionError("CP-SAT CEGAR final anatomy changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "resume_source": str(resume_path),
        "resume_source_sha256": sha256(resume_path),
        "status": payload["status"],
        "cap": payload["cap"],
        "trace_survivor_counts": trace_counts,
        "replayed_pool_size": len(pool),
        "conflicts": payload["conflicts"],
        "branches": payload["branches"],
        "elapsed_seconds": payload["elapsed_seconds"],
        "proto_sha256": payload["proto_sha256"],
        "final_profile": {
            "values": [list(row) for row in final_values],
            "favorite_pair_efx_partition_count": len(final_repairs),
            "favorite_partner_counts": {
                str(key): value for key, value in sorted(partner_counts.items())
            },
            "favorite_pair_triple_counts": {
                "+".join(map(str, key)): value
                for key, value in sorted(triple_counts.items())
            },
            "balanced_landscape": balanced_landscape,
            "full_favorite_triple_cells": [
                list(cell) for cell in full_triple_cells
            ],
            "literal_complete_efx_count": literal_count,
        },
    }


def audit_complement(
    path,
    expected_counts,
    expected_pool,
    expected_iterations,
    expected_reason,
    expected_two_core_encoding,
):
    payload = json.loads(path.read_text())
    seed_paths = tuple(Path(source["path"]) for source in payload["seed_sources"])
    for source, seed_path in zip(payload["seed_sources"], seed_paths):
        if sha256(seed_path) != source["sha256"]:
            raise AssertionError("complement seed hash changed")
    recomputed = analyze_seed_pool(seed_paths)
    seed_analysis = payload.get("seed_pool_analysis")
    if (
        recomputed["covered_partition_count"]
        != payload["seed_supported_union_size"]
        or recomputed["missing_partition_count"] != 55
    ):
        raise AssertionError("complement seed frontier changed")
    if seed_analysis is not None:
        analysis_path = Path(seed_analysis["path"])
        if (
            sha256(analysis_path) != seed_analysis["sha256"]
            or recomputed["missing_partition_count"]
            != seed_analysis["missing_partition_count"]
            or recomputed["missing_partitions_sha256"]
            != seed_analysis["missing_partitions_sha256"]
        ):
            raise AssertionError("complement seed analysis changed")
    universe = tuple(favorite_pair_balanced_universe())
    seed_supported = set()
    for seed_path in seed_paths:
        seed_supported.update(
            supported_partitions(
                load_values(seed_path),
                list(universe),
            )
        )
    pool = set(universe).difference(seed_supported)
    trace_counts = []
    for position, trace in enumerate(payload["trace"], start=1):
        values = core.validate_values(
            trace["values"], expected_n=4, expected_m=9, lower=1
        )
        audit_branch(values)
        if two_core_witnesses(values):
            raise AssertionError("seeded CEGAR trace model has a two-core witness")
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if (
            trace["iteration"] != position
            or trace["pool_size_before"] != len(pool)
            or trace["favorite_pair_efx_survivors"] != len(survivors)
        ):
            raise AssertionError("seeded CEGAR trace replay changed")
        trace_counts.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
    smt2_path = Path(payload["smt2_path"])
    if (
        payload["status"] != "MASTER_UNKNOWN"
        or payload["solver_status"] != "unknown"
        or payload["reason_unknown"] != expected_reason
        or payload["seed_mode"] != "complement"
        or trace_counts != expected_counts
        or len(pool) != expected_pool
        or payload["pool_size"] != expected_pool
        or payload["iterations"] != expected_iterations
        or payload["two_core_encoding"]["encoding"]
        != expected_two_core_encoding
        or payload["values"] is not None
        or payload["literal_complete_efx_count"] is not None
        or sha256(smt2_path) != payload["smt2_sha256"]
    ):
        raise AssertionError("complement CEGAR endpoint changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "status": payload["status"],
        "reason_unknown": payload["reason_unknown"],
        "two_core_encoding": payload["two_core_encoding"]["encoding"],
        "seed_supported_union_size": payload["seed_supported_union_size"],
        "trace_survivor_counts": trace_counts,
        "replayed_pool_size": len(pool),
        "missing_partitions_sha256": recomputed["missing_partitions_sha256"],
        "smt2_sha256": payload["smt2_sha256"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matching", type=Path, required=True)
    parser.add_argument("--hall", type=Path, required=True)
    parser.add_argument("--complement", type=Path, required=True)
    parser.add_argument("--reified-complement", type=Path, required=True)
    parser.add_argument("--cpsat", type=Path, required=True)
    parser.add_argument("--cpsat-cegar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": SCHEMA,
        "status": "TWO_CORE_DECISION_BOUNDARY_REPLAY_PASSED",
        "matching_cegar": audit_cegar(
            args.matching,
            "ITERATION_LIMIT",
            [598, 319, 228, 283, 279],
            40,
        ),
        "hall_cegar": audit_cegar(
            args.hall,
            "MASTER_UNKNOWN",
            [598, 270, 383],
            24,
        ),
        "complement_cegar": audit_complement(
            args.complement,
            [],
            55,
            1,
            "timeout",
            "direct",
        ),
        "reified_complement_cegar": audit_complement(
            args.reified_complement,
            [265],
            183,
            2,
            "canceled",
            "reified",
        ),
        "bounded_cpsat": audit_cpsat(args.cpsat),
        "bounded_cpsat_cegar": audit_cpsat_cegar(args.cpsat_cegar),
        "interpretation": (
            "Exact-real CEGAR produced only profiles with hundreds of "
            "favorite-pair repairs before its current boundaries. A "
            "separate 55-cut complement frontier timed out before its first "
            "model; a reified replay found one 265-repair model before its "
            "183-cut timeout. Bounded CP-SAT CEGAR reduced the remaining "
            "repairs from 398 to 143 to 20; the 331-cut continuation "
            "remained unknown after 900 seconds, and the full cap-20 "
            "formula also timed out. No two-core "
            "selection counterexample or UNSAT theorem is claimed."
        ),
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
