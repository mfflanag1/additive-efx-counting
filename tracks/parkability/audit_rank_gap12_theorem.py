#!/usr/bin/env python3
"""Audit the dual-encoding 4x9 rank-cap-12 EFX package."""

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


SCHEMA = "rank-gap12-efx-4x9-dual-encoding-audit-v1"
PATTERNS = {
    "4": (0, 0, 0, 0),
    "31": (0, 0, 0, 1),
    "22": (0, 0, 1, 1),
    "211": (0, 0, 1, 2),
    "1111": (0, 1, 2, 3),
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_stem(pattern_name: str, encoding: str) -> str:
    if pattern_name == "4":
        return (
            "efx49_rankgap12_favorites4_complete_"
            f"{'matching' if encoding == 'matching_clauses' else 'hall'}_"
            "stabilized_session"
            "2"
        )
    return (
        f"efx49_rankgap12_shape3222_favorites{pattern_name}_"
        f"{'matching' if encoding == 'matching_clauses' else 'hall'}_"
        "stabilized_session1"
    )


def pool_path(results_dir: Path, pattern_name: str, encoding: str) -> Path:
    if pattern_name == "4":
        return (
            results_dir
            / (
                "efx49_rankgap12_favorites4_complete_"
                f"{'matching' if encoding == 'matching_clauses' else 'hall'}_"
                "stabilized_pool.json"
            )
        )
    return (
        results_dir
        / (
            f"efx49_rankgap12_shape3222_favorites{pattern_name}_"
            f"{'matching' if encoding == 'matching_clauses' else 'hall'}_"
            "stabilized_pool.json"
        )
    )


def audit(results_dir: Path) -> dict:
    cells = []
    for pattern_name, pattern in PATTERNS.items():
        common = pattern_name == "4"
        for encoding in ("matching_clauses", "hall_selectors"):
            result_path = results_dir / f"{result_stem(pattern_name, encoding)}.json"
            raw = json.loads(result_path.read_text())
            expected = {
                "schema": "integer-partition-cp-sat-result-v1",
                "status": "UNSAT_BOUNDED_CELL_CANDIDATE",
                "n": 4,
                "m": 9,
                "upper": 12,
                "partition_universe_size": 7770 if common else 1260,
                "partition_shape": None if common else [3, 2, 2, 2],
                "pool_size": 472 if common else 417,
                "symmetry": "none",
                "exclude_universal_min": False,
                "exclude_peelable": False,
                "require_pairwise_distinct_rows": False,
                "require_distinct_item_values": True,
                "obstruction_encoding": encoding,
                "favorite_pattern": list(pattern),
                "favorite_pattern_stabilizer": True,
                "solver_status": "INFEASIBLE",
                "values": None,
            }
            mismatches = {
                key: {"expected": expected_value, "actual": raw.get(key)}
                for key, expected_value in expected.items()
                if raw.get(key) != expected_value
            }
            if mismatches:
                raise AssertionError((result_path, mismatches))
            if not raw.get("trace") or raw["trace"][-1].get(
                "solver_status"
            ) != "INFEASIBLE":
                raise AssertionError(f"{result_path} lacks an infeasible trace")

            proto_path = Path(raw["proto_path"])
            if (
                not proto_path.is_file()
                or file_sha256(proto_path) != raw["proto_sha256"]
                or proto_path.stat().st_size != raw["proto_bytes"]
            ):
                raise AssertionError(f"{result_path} has a broken proto reference")
            cell_pool_path = pool_path(results_dir, pattern_name, encoding)
            if file_sha256(cell_pool_path) != raw["pool_sha256"]:
                raise AssertionError(f"{result_path} has a broken pool hash")
            pool = load_pool(cell_pool_path, 4, 9)
            if len(pool) != expected["pool_size"]:
                raise AssertionError(f"{cell_pool_path} has the wrong size")
            shape_counts = Counter(
                tuple(sorted(map(len, partition), reverse=True))
                for partition in pool
            )
            if common:
                if (
                    shape_counts
                    != Counter({
                        (3, 2, 2, 2): 424,
                        (3, 3, 2, 1): 37,
                        (4, 2, 2, 1): 11,
                    })
                    or sum((0,) in partition for partition in pool) != 48
                    or any(
                        tuple(sorted(map(len, partition), reverse=True))
                        != (3, 2, 2, 2)
                        and (0,) not in partition
                        for partition in pool
                    )
                ):
                    raise AssertionError(
                        f"{cell_pool_path} is not the balanced-or-singleton pool"
                    )
            elif shape_counts != Counter({(3, 2, 2, 2): 417}):
                raise AssertionError(f"{cell_pool_path} is not a balanced pool")

            cells.append({
                "favorite_multiplicity": pattern_name,
                "favorite_pattern": list(pattern),
                "encoding": encoding,
                "result_path": str(result_path.resolve()),
                "result_sha256": file_sha256(result_path),
                "proto_path": str(proto_path.resolve()),
                "proto_sha256": raw["proto_sha256"],
                "pool_path": str(cell_pool_path.resolve()),
                "pool_sha256": raw["pool_sha256"],
                "pool_size": raw["pool_size"],
                "solver_status": raw["solver_status"],
                "wall_time_seconds": raw["trace"][-1]["wall_time_seconds"],
                "workers": (
                    8 if common else
                    (1 if encoding == "matching_clauses" else 2)
                ),
                "comparison_variables": raw["comparison_variables"],
                "matching_clauses": raw["matching_clauses"],
                "hall_selectors": raw["hall_selectors"],
                "hall_edge_clauses": raw["hall_edge_clauses"],
            })

    boundary_path = results_dir / "efx49_rankgap12_shape_boundary_audit.json"
    boundary = json.loads(boundary_path.read_text())
    if (
        boundary.get("status") != "BOUNDARY_AUDIT_PASSED"
        or boundary.get("literal_labeled_allocation_census", {}).get(
            "complete_efx_count"
        ) != 838
        or boundary.get("unlabeled_partition_census", {}).get(
            "partitions_isolating_common_favorite"
        ) != 48
    ):
        raise AssertionError("the cap-12 shape-boundary audit is incomplete")

    return {
        "schema": SCHEMA,
        "status": "DUAL_ENCODING_AUDIT_PASSED",
        "claim": (
            "Every four-agent, nine-good instance in which each row has "
            "nine distinct integer values from 1,...,12 admits a complete "
            "EFX allocation."
        ),
        "claim_level": (
            "computer-assisted theorem candidate: ten exact dual-encoding "
            "CP-SAT infeasibility verdicts with hash-pinned models"
        ),
        "domain": {
            "agents": 4,
            "goods": 9,
            "value_lower": 1,
            "value_upper": 12,
            "distinct_values_per_row": 9,
        },
        "favorite_orbits": list(PATTERNS),
        "favorite_orbit_count": len(PATTERNS),
        "encodings": ["matching_clauses", "hall_selectors"],
        "cell_count": len(cells),
        "structural_conclusion": {
            "non_common_favorite_orbits": (
                "an EFX allocation of shape (3,2,2,2) exists"
            ),
            "common_favorite_orbit": (
                "either an EFX allocation of shape (3,2,2,2) exists or "
                "the common favorite is an EFX singleton bundle"
            ),
            "common_pool_size": 472,
            "common_balanced_partitions": 424,
            "common_singleton_partitions": 48,
        },
        "cells": cells,
        "shape_boundary_audit": {
            "path": str(boundary_path.resolve()),
            "sha256": file_sha256(boundary_path),
            "complete_efx_count": 838,
            "shape_3+2+2+2_count": 0,
        },
        "limitations": [
            "This finite rank-cap domain is far smaller than arbitrary additive valuations.",
            "Both obstruction encodings were solved by the same OR-Tools CP-SAT engine.",
            "The cap-12 cells do not yet have external proof logs.",
            "Distinct item values are part of the finite-domain claim.",
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
