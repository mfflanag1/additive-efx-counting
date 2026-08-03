#!/usr/bin/env python3
"""Audit the sparse dual-encoding cap-12 common-favorite certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_generic_partition_cegar import load_pool
except ImportError:
    from anneal import atomic_json
    from run_generic_partition_cegar import load_pool


SCHEMA = "rank-gap12-common-favorite-sparse-dual-audit-v1"
EXPECTED_SINGLETON_PARTITIONS = {
    ((0,), (1, 2), (3, 4), (5, 6, 7, 8)),
    ((0,), (1, 2), (3, 4, 6), (5, 7, 8)),
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_committed_artifact(raw_path: str, results_dir: Path) -> Path:
    path = Path(raw_path)
    committed = results_dir / path.name
    return path if path.is_file() else committed


def audit(results_dir: Path) -> dict:
    pool_path = (
        results_dir
        / "efx49_rankgap12_favorites4_balanced_or_singleton_sparse_pool.json"
    )
    pool = load_pool(pool_path, 4, 9)
    pool_sha256 = file_sha256(pool_path)
    shape_counts = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in pool
    )
    singleton_partitions = {
        partition for partition in pool if (0,) in partition
    }
    if (
        len(pool) != 426
        or shape_counts
        != Counter({
            (3, 2, 2, 2): 424,
            (3, 3, 2, 1): 1,
            (4, 2, 2, 1): 1,
        })
        or singleton_partitions != EXPECTED_SINGLETON_PARTITIONS
    ):
        raise AssertionError("the sparse balanced-or-singleton pool changed")

    specifications = (
        (
            "matching_clauses",
            results_dir
            / "efx49_rankgap12_favorites4_balanced_or_singleton_sparse_session1.json",
        ),
        (
            "hall_selectors",
            results_dir
            / "efx49_rankgap12_favorites4_balanced_or_singleton_sparse_hall.json",
        ),
    )
    cells = []
    for encoding, result_path in specifications:
        raw = json.loads(result_path.read_text())
        expected = {
            "schema": "integer-partition-cp-sat-result-v1",
            "status": "UNSAT_BOUNDED_CELL_CANDIDATE",
            "n": 4,
            "m": 9,
            "upper": 12,
            "partition_universe_size": 2226,
            "partition_shape": [3, 2, 2, 2],
            "partition_singleton_goods": [0],
            "pool_size": 426,
            "pool_sha256": pool_sha256,
            "symmetry": "none",
            "exclude_universal_min": False,
            "exclude_peelable": False,
            "require_pairwise_distinct_rows": False,
            "require_distinct_item_values": True,
            "obstruction_encoding": encoding,
            "favorite_pattern": [0, 0, 0, 0],
            "favorite_pattern_stabilizer": True,
            "solver_status": "INFEASIBLE",
            "values": None,
        }
        mismatches = {
            key: {"expected": value, "actual": raw.get(key)}
            for key, value in expected.items()
            if raw.get(key) != value
        }
        if mismatches:
            raise AssertionError((result_path, mismatches))
        proto_path = resolve_committed_artifact(raw["proto_path"], results_dir)
        if (
            not proto_path.is_file()
            or file_sha256(proto_path) != raw["proto_sha256"]
            or proto_path.stat().st_size != raw["proto_bytes"]
        ):
            raise AssertionError(f"{result_path} has a broken proto reference")
        if not raw.get("trace") or raw["trace"][-1].get(
            "solver_status"
        ) != "INFEASIBLE":
            raise AssertionError(f"{result_path} lacks an infeasible trace")
        cells.append({
            "encoding": encoding,
            "result_path": str(result_path.resolve()),
            "result_sha256": file_sha256(result_path),
            "proto_path": str(proto_path.resolve()),
            "proto_sha256": raw["proto_sha256"],
            "solver_status": raw["solver_status"],
            "wall_time_seconds": raw["trace"][-1]["wall_time_seconds"],
            "comparison_variables": raw["comparison_variables"],
            "matching_clauses": raw["matching_clauses"],
            "hall_selectors": raw["hall_selectors"],
            "hall_edge_clauses": raw["hall_edge_clauses"],
        })

    return {
        "schema": SCHEMA,
        "status": "SPARSE_DUAL_ENCODING_AUDIT_PASSED",
        "claim": (
            "In the rank-distinct cap-12 common-favorite cell, either a "
            "shape-(3,2,2,2) EFX allocation exists or one of two canonical "
            "partitions isolating the common favorite supports EFX."
        ),
        "claim_level": (
            "computer-assisted theorem candidate: exact matching-clause and "
            "Hall-selector CP-SAT infeasibility verdicts"
        ),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": pool_sha256,
        "pool_size": len(pool),
        "balanced_partition_count": 424,
        "singleton_partition_count": 2,
        "singleton_partitions": [
            [list(bundle) for bundle in partition]
            for partition in sorted(singleton_partitions)
        ],
        "encodings": ["matching_clauses", "hall_selectors"],
        "cells": cells,
        "limitations": [
            "This is a finite rank-cap-12 statement, not arbitrary additivity.",
            "Both encodings were solved by OR-Tools CP-SAT.",
            "The sparse cells do not yet have external proof logs.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.results_dir)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
