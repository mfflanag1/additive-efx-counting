#!/usr/bin/env python3
"""Replay exact-real and bounded boundaries for the full Hall-cell target."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import Landscape
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import full_hall_cells
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import Landscape
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import full_hall_cells
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-decision-boundary-audit-v2"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_exact_real(path):
    payload = json.loads(path.read_text())
    seed_paths = tuple(Path(source["path"]) for source in payload["seed_sources"])
    for source, seed_path in zip(payload["seed_sources"], seed_paths):
        if sha256(seed_path) != source["sha256"]:
            raise AssertionError("full-cell seed hash changed")
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
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("full-cell CEGAR trace has a full Hall cell")
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
            raise AssertionError("full-cell CEGAR trace replay changed")
        trace_counts.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
        final_values = values
    smt2_path = Path(payload["smt2_path"])
    if (
        payload["status"] != "MASTER_UNKNOWN"
        or payload["solver_status"] != "unknown"
        or payload["reason_unknown"] != "canceled"
        or payload["seed_mode"] != "complement"
        or payload["seed_supported_union_size"] != 785
        or trace_counts != [289]
        or len(pool) != 183
        or payload["pool_size"] != 183
        or payload["iterations"] != 2
        or payload["elapsed_seconds"] < 180
        or payload["values"] is not None
        or payload["literal_complete_efx_count"] is not None
        or sha256(smt2_path) != payload["smt2_sha256"]
    ):
        raise AssertionError("full-cell CEGAR endpoint changed")
    if final_values is None:
        raise AssertionError("full-cell CEGAR trace is empty")
    balanced_landscape = Landscape("balanced").audit(final_values)
    literal_count = independent.count_complete_efx0(final_values)
    if (
        balanced_landscape["favorite_pair_perfect_partition_count"] != 289
        or balanced_landscape["full_favorite_triple_cell_count"] != 0
        or literal_count <= 0
    ):
        raise AssertionError("full-cell CEGAR anatomy changed")
    return {
        "schema": SCHEMA,
        "status": "FULL_CELL_DECISION_BOUNDARY_REPLAY_PASSED",
        "source": str(path),
        "source_sha256": sha256(path),
        "solver_status": payload["status"],
        "reason_unknown": payload["reason_unknown"],
        "seed_supported_union_size": payload["seed_supported_union_size"],
        "trace_survivor_counts": trace_counts,
        "replayed_pool_size": len(pool),
        "elapsed_seconds": payload["elapsed_seconds"],
        "smt2_sha256": payload["smt2_sha256"],
        "trace_profile": {
            "values": [list(row) for row in final_values],
            "balanced_landscape": balanced_landscape,
            "literal_complete_efx_count": literal_count,
        },
        "interpretation": (
            "The exact-real no-full-cell master produced one profile with "
            "289 favorite-pair repairs, then timed out at 183 cuts. It is "
            "neither a full-cell counterexample nor a theorem."
        ),
    }


def audit_cpsat_cegar(path):
    payload = json.loads(path.read_text())
    seed_paths = tuple(Path(source["path"]) for source in payload["seed_sources"])
    for source, seed_path in zip(payload["seed_sources"], seed_paths):
        if sha256(seed_path) != source["sha256"]:
            raise AssertionError("bounded full-cell seed hash changed")
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
        audit_branch(values)
        if max(max(row) for row in values) > payload["cap"]:
            raise AssertionError("bounded full-cell trace exceeds cap")
        if full_hall_cells(values):
            raise AssertionError("bounded full-cell trace has a full Hall cell")
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
            raise AssertionError("bounded full-cell trace replay changed")
        trace_counts.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
        final_values = values

    resume_path = Path(payload["resume_source"])
    resume = json.loads(resume_path.read_text())
    resume_proto = Path(resume["proto_path"])
    proto_path = Path(payload["proto_path"])
    expected_encoding = {
        "accept_literals": 1680,
        "hall_failure_templates_per_pairing": 21,
        "hall_witness_literals": 8820,
        "low_pair_cells": 28,
    }
    if (
        payload["status"] != "CP_SAT_UNKNOWN"
        or payload["solver_status"] != "UNKNOWN"
        or payload["cap"] != 20
        or payload["seed_mode"] != "complement"
        or payload["seed_supported_union_size"] != 785
        or payload["full_hall_cell_forbidden"] is not True
        or payload["full_cell_encoding"] != expected_encoding
        or trace_counts != [357]
        or len(pool) != 412
        or payload["pool_size"] != 412
        or payload["iterations"] != 2
        or payload["add_per_iteration"] != 512
        or payload.get("time_limit_seconds") != 600.0
        or payload["elapsed_seconds"] < 600
        or payload["values"] is not None
        or payload["literal_complete_efx_count"] is not None
        or sha256(proto_path) != payload["proto_sha256"]
        or resume.get("schema") != payload["schema"]
        or resume.get("trace") != payload["trace"]
        or sha256(resume_path) != payload["resume_source_sha256"]
        or sha256(resume_proto) != resume["proto_sha256"]
        or payload.get("symmetry_breaking")
        != [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ]
    ):
        raise AssertionError("bounded full-cell endpoint changed")
    if final_values is None:
        raise AssertionError("bounded full-cell trace is empty")
    balanced_landscape = Landscape("balanced").audit(final_values)
    literal_count = independent.count_complete_efx0(final_values)
    if (
        balanced_landscape["favorite_pair_perfect_partition_count"] != 357
        or balanced_landscape["favorite_triple_perfect_partition_count"] != 0
        or balanced_landscape["full_favorite_triple_cell_count"] != 0
        or literal_count != 3563
    ):
        raise AssertionError("bounded full-cell anatomy changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "resume_source": str(resume_path),
        "resume_source_sha256": sha256(resume_path),
        "status": payload["status"],
        "cap": payload["cap"],
        "trace_survivor_counts": trace_counts,
        "replayed_pool_size": len(pool),
        "elapsed_seconds": payload["elapsed_seconds"],
        "conflicts": payload["conflicts"],
        "branches": payload["branches"],
        "proto_sha256": payload["proto_sha256"],
        "trace_profile": {
            "values": [list(row) for row in final_values],
            "balanced_landscape": balanced_landscape,
            "literal_complete_efx_count": literal_count,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--cpsat-cegar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit_exact_real(args.result)
    result["bounded_cpsat_cegar"] = audit_cpsat_cegar(args.cpsat_cegar)
    result["interpretation"] = (
        "The exact-real master found one no-full-cell profile with 289 "
        "favorite-pair repairs before its 183-cut unknown boundary. A "
        "separate cap-20 CP-SAT trace found a no-full-cell profile with "
        "357 repairs; its 412-cut continuation remained unknown after "
        "600 seconds. Neither endpoint is a counterexample or theorem."
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
