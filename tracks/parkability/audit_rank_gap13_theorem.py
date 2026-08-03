#!/usr/bin/env python3
"""Audit the 4x9 rank-cap-13 EFX theorem-candidate package."""

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


SCHEMA = "rank-gap13-efx-4x9-audit-v1"
CELLS = {
    "4": {
        "pattern": [0, 0, 0, 0],
        "singleton_goods": [0],
        "pool_size": 446,
        "matching": (
            "efx49_rankgap13_favorites4_balanced_or_singleton_sparse_"
            "matching_session2"
        ),
        "hall": (
            "efx49_rankgap13_favorites4_balanced_or_singleton_sparse_"
            "hall_session1"
        ),
        "hall_status": "INFEASIBLE",
    },
    "31": {
        "pattern": [0, 0, 0, 1],
        "singleton_goods": [0, 1],
        "pool_size": 560,
        "matching": (
            "efx49_rankgap13_favorites31_balanced_or_favorite_singleton_"
            "matching_session1"
        ),
        "hall": (
            "efx49_rankgap13_favorites31_balanced_or_favorite_singleton_"
            "hall_session1"
        ),
        "hall_status": "INFEASIBLE",
    },
    "22": {
        "pattern": [0, 0, 1, 1],
        "singleton_goods": [0, 1],
        "pool_size": 535,
        "matching": (
            "efx49_rankgap13_favorites22_balanced_or_favorite_singleton_"
            "matching_session1"
        ),
        "hall": (
            "efx49_rankgap13_favorites22_balanced_or_favorite_singleton_"
            "hall_session1"
        ),
        "hall_status": "INFEASIBLE",
    },
    "211": {
        "pattern": [0, 0, 1, 2],
        "singleton_goods": [],
        "pool_size": 417,
        "matching": (
            "efx49_rankgap13_shape3222_favorites211_"
            "matching_stabilized_session1"
        ),
        "hall": (
            "efx49_rankgap13_shape3222_favorites211_"
            "hall_stabilized_session1"
        ),
        "hall_status": "INFEASIBLE",
    },
    "1111": {
        "pattern": [0, 1, 2, 3],
        "singleton_goods": [],
        "pool_size": 417,
        "matching": (
            "efx49_rankgap13_shape3222_favorites1111_"
            "matching_stabilized_session1"
        ),
        "hall": (
            "efx49_rankgap13_shape3222_favorites1111_"
            "hall_stabilized_session1"
        ),
        "hall_status": "INFEASIBLE",
    },
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_committed_artifact(raw_path: str, results_dir: Path) -> Path:
    path = Path(raw_path)
    committed = results_dir / path.name
    return path if path.is_file() else committed


def expected_shape_counts(name: str) -> Counter[tuple[int, ...]]:
    return {
        "4": Counter({
            (3, 2, 2, 2): 427,
            (3, 3, 2, 1): 14,
            (4, 2, 2, 1): 5,
        }),
        "31": Counter({
            (3, 2, 2, 2): 454,
            (3, 3, 2, 1): 78,
            (4, 2, 2, 1): 21,
            (4, 3, 1, 1): 7,
        }),
        "22": Counter({
            (3, 2, 2, 2): 434,
            (3, 3, 2, 1): 75,
            (4, 2, 2, 1): 18,
            (4, 3, 1, 1): 8,
        }),
        "211": Counter({(3, 2, 2, 2): 417}),
        "1111": Counter({(3, 2, 2, 2): 417}),
    }[name]


def audit(results_dir: Path) -> dict:
    cells = []
    matching_closed = 0
    hall_closed = 0
    for name, cell in CELLS.items():
        result_records = {}
        for encoding, stem in (
            ("matching_clauses", cell["matching"]),
            ("hall_selectors", cell["hall"]),
        ):
            result_path = results_dir / f"{stem}.json"
            raw = json.loads(result_path.read_text())
            pool_path = results_dir / f"{stem.rsplit('_session', 1)[0]}_pool.json"
            if encoding == "matching_clauses":
                expected_solver_status = "INFEASIBLE"
                expected_status = "UNSAT_BOUNDED_CELL_CANDIDATE"
            else:
                expected_solver_status = cell["hall_status"]
                expected_status = (
                    "UNSAT_BOUNDED_CELL_CANDIDATE"
                    if expected_solver_status == "INFEASIBLE"
                    else "MASTER_UNKNOWN"
                )
            expected = {
                "schema": "integer-partition-cp-sat-result-v1",
                "status": expected_status,
                "n": 4,
                "m": 9,
                "upper": 13,
                "pool_size": cell["pool_size"],
                "symmetry": "none",
                "exclude_universal_min": False,
                "exclude_peelable": False,
                "require_pairwise_distinct_rows": False,
                "require_distinct_item_values": True,
                "obstruction_encoding": encoding,
                "favorite_pattern": cell["pattern"],
                "favorite_pattern_stabilizer": True,
                "solver_status": expected_solver_status,
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
            ) != expected_solver_status:
                raise AssertionError(f"{result_path} has a broken trace")
            proto_path = resolve_committed_artifact(
                raw["proto_path"], results_dir
            )
            if (
                not proto_path.is_file()
                or file_sha256(proto_path) != raw["proto_sha256"]
                or proto_path.stat().st_size != raw["proto_bytes"]
            ):
                raise AssertionError(f"{result_path} has a broken proto")
            if (
                not pool_path.is_file()
                or file_sha256(pool_path) != raw["pool_sha256"]
            ):
                raise AssertionError(f"{result_path} has a broken pool")
            pool = load_pool(pool_path, 4, 9)
            shape_counts = Counter(
                tuple(sorted(map(len, partition), reverse=True))
                for partition in pool
            )
            if (
                len(pool) != cell["pool_size"]
                or shape_counts != expected_shape_counts(name)
                or any(
                    tuple(sorted(map(len, partition), reverse=True))
                    != (3, 2, 2, 2)
                    and not any(
                        (good,) in partition for good in cell["singleton_goods"]
                    )
                    for partition in pool
                )
            ):
                raise AssertionError(f"{pool_path} has the wrong structural scope")
            result_records[encoding] = {
                "result_path": str(result_path.resolve()),
                "result_sha256": file_sha256(result_path),
                "proto_path": str(proto_path.resolve()),
                "proto_sha256": raw["proto_sha256"],
                "pool_path": str(pool_path.resolve()),
                "pool_sha256": raw["pool_sha256"],
                "pool_size": raw["pool_size"],
                "solver_status": raw["solver_status"],
                "wall_time_seconds": raw["trace"][-1]["wall_time_seconds"],
                "comparison_variables": raw["comparison_variables"],
                "matching_clauses": raw["matching_clauses"],
                "hall_selectors": raw["hall_selectors"],
                "hall_edge_clauses": raw["hall_edge_clauses"],
            }
        matching_closed += (
            result_records["matching_clauses"]["solver_status"] == "INFEASIBLE"
        )
        hall_closed += (
            result_records["hall_selectors"]["solver_status"] == "INFEASIBLE"
        )
        cells.append({
            "favorite_multiplicity": name,
            "favorite_pattern": cell["pattern"],
            "designated_singleton_goods": cell["singleton_goods"],
            "structural_pool_size": cell["pool_size"],
            "matching": result_records["matching_clauses"],
            "hall": result_records["hall_selectors"],
        })

    boundary_path = results_dir / "efx49_rankgap13_shape_boundaries_audit.json"
    boundary = json.loads(boundary_path.read_text())
    if boundary.get("status") != "BOUNDARY_AUDIT_PASSED":
        raise AssertionError("the cap-13 boundary audit is incomplete")
    return {
        "schema": SCHEMA,
        "status": "DUAL_ENCODING_AUDIT_PASSED",
        "claim": (
            "Every four-agent, nine-good instance in which each row has "
            "nine distinct integer values from 1,...,13 admits a complete "
            "EFX allocation."
        ),
        "claim_level": (
            "computer-assisted theorem candidate: all five exact "
            "matching-clause cells and all five independent Hall-selector "
            "cells are infeasible"
        ),
        "domain": {
            "agents": 4,
            "goods": 9,
            "value_lower": 1,
            "value_upper": 13,
            "distinct_values_per_row": 9,
        },
        "structural_conclusion": (
            "An EFX allocation exists that either has shape (3,2,2,2) or "
            "isolates a designated favorite good as a singleton."
        ),
        "matching_closed_cells": matching_closed,
        "hall_closed_cells": hall_closed,
        "favorite_orbit_count": len(CELLS),
        "cells": cells,
        "shape_boundaries": {
            "path": str(boundary_path.resolve()),
            "sha256": file_sha256(boundary_path),
        },
        "limitations": [
            "This finite rank-cap domain is far smaller than arbitrary additive valuations.",
            "All terminal verdicts use OR-Tools CP-SAT and lack external proof logs.",
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
