#!/usr/bin/env python3
"""Audit the sufficient-cap common-favorite structural frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json, has_universal_min
    from .run_efx_lra_cegar import (
        has_peelable_good,
        has_repeated_normalized_rows,
    )
    from .run_generic_partition_cegar import load_pool, supported_partitions
except ImportError:
    import core
    from anneal import atomic_json, has_universal_min
    from run_efx_lra_cegar import (
        has_peelable_good,
        has_repeated_normalized_rows,
    )
    from run_generic_partition_cegar import load_pool, supported_partitions


SCHEMA = "common-favorite-efx-4x9-sufficient-cap-audit-v1"
UNCUT_SESSIONS = (
    (1, 485, 661),
    (2, 661, 719),
    (3, 719, 811),
)
RESIDUAL_RESULTS = (
    (
        "matching_clauses",
        "efx49_common_favorite_structural_integer19683_"
        "residual2_matching_session1.json",
        "efx49_common_favorite_structural_integer19683_"
        "residual2_matching_pool.json",
    ),
    (
        "hall_selectors",
        "efx49_common_favorite_structural_integer19683_"
        "residual2_hall_session1.json",
        "efx49_common_favorite_structural_integer19683_"
        "residual2_hall_pool.json",
    ),
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_proto(raw: dict) -> Path:
    proto_path = Path(raw["proto_path"])
    if (
        not proto_path.is_file()
        or file_sha256(proto_path) != raw["proto_sha256"]
        or proto_path.stat().st_size != raw["proto_bytes"]
    ):
        raise AssertionError("broken CP-SAT proto reference")
    return proto_path


def audit(results_dir: Path) -> dict:
    start_path = (
        results_dir / "efx49_common_favorite_real_structural_pool485.json"
    )
    final_path = (
        results_dir
        / "efx49_common_favorite_structural_integer19683_pool.json"
    )
    pool = load_pool(start_path, 4, 9)
    final_pool = load_pool(final_path, 4, 9)
    if len(pool) != 485 or len(final_pool) != 811:
        raise AssertionError("sufficient-cap pool endpoints changed")
    pool_set = set(pool)
    target_universe = [
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(4, 9)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2)
        or (0,) in partition
    ]
    if len(target_universe) != 2226:
        raise AssertionError("target partition universe changed")

    session_records = []
    model_flags = []
    for session, expected_before, expected_after in UNCUT_SESSIONS:
        result_path = (
            results_dir
            / (
                "efx49_common_favorite_structural_integer19683_"
                f"session{session}.json"
            )
        )
        raw = json.loads(result_path.read_text())
        expected = {
            "schema": "integer-partition-cp-sat-result-v1",
            "status": "ITERATION_LIMIT",
            "n": 4,
            "m": 9,
            "upper": 19683,
            "partition_universe_size": 2226,
            "partition_shape": [3, 2, 2, 2],
            "partition_singleton_goods": [0],
            "pool_size": expected_after,
            "require_distinct_item_values": False,
            "obstruction_encoding": "matching_clauses",
            "favorite_pattern": [0, 0, 0, 0],
            "favorite_pattern_stabilizer": True,
            "solver_status": "OPTIMAL",
            "values": None,
        }
        mismatches = {
            key: {"expected": value, "actual": raw.get(key)}
            for key, value in expected.items()
            if raw.get(key) != value
        }
        if mismatches or len(raw.get("trace", [])) != 5:
            raise AssertionError((result_path, mismatches))
        proto_path = validate_proto(raw)
        if len(pool) != expected_before:
            raise AssertionError("uncut pool chain has the wrong starting size")

        additions = 0
        for record in raw["trace"]:
            values = core.validate_values(
                record["values"],
                expected_n=4,
                expected_m=9,
                lower=1,
                upper=19683,
            )
            if any(
                values[agent][0] <= values[agent][good]
                for agent in range(4)
                for good in range(1, 9)
            ):
                raise AssertionError("learning model left the favorite cell")
            survivors = supported_partitions(values, target_universe)
            if (
                len(survivors) != record["supported_partition_count"]
                or any(partition in pool_set for partition in survivors)
            ):
                raise AssertionError("learning model replay changed")
            for partition in survivors[:128]:
                pool.append(partition)
                pool_set.add(partition)
                additions += 1
            model_flags.append({
                "session": session,
                "iteration": record["iteration"],
                "supported_partition_count": len(survivors),
                "has_item_ties": any(len(set(row)) < 9 for row in values),
                "has_universal_minimum": has_universal_min(values),
                "has_peelable_pair": has_peelable_good(values),
                "has_repeated_normalized_rows": has_repeated_normalized_rows(
                    values
                ),
            })
        if len(pool) != expected_after:
            raise AssertionError("uncut pool chain has the wrong ending size")
        session_records.append({
            "session": session,
            "result_path": str(result_path.resolve()),
            "result_sha256": file_sha256(result_path),
            "proto_path": str(proto_path.resolve()),
            "proto_sha256": raw["proto_sha256"],
            "pool_before": expected_before,
            "pool_after": expected_after,
            "models": len(raw["trace"]),
            "new_partitions": additions,
        })

    if pool != final_pool or any(not flags["has_item_ties"] for flags in model_flags):
        raise AssertionError("final sufficient-cap pool reconstruction failed")

    first_residual_path = (
        results_dir
        / (
            "efx49_common_favorite_structural_integer19683_"
            "residual_session1.json"
        )
    )
    first_residual_pool_path = (
        results_dir
        / (
            "efx49_common_favorite_structural_integer19683_"
            "residual_pool.json"
        )
    )
    first_residual = json.loads(first_residual_path.read_text())
    if (
        first_residual.get("status") != "MASTER_UNKNOWN"
        or first_residual.get("pool_size") != 719
        or first_residual.get("solver_status") != "UNKNOWN"
        or file_sha256(first_residual_pool_path)
        != first_residual.get("pool_sha256")
    ):
        raise AssertionError("first residual timeout changed")
    validate_proto(first_residual)

    residual_records = []
    for encoding, result_name, pool_name in RESIDUAL_RESULTS:
        result_path = results_dir / result_name
        pool_path = results_dir / pool_name
        raw = json.loads(result_path.read_text())
        expected = {
            "schema": "integer-partition-cp-sat-result-v1",
            "status": "MASTER_UNKNOWN",
            "n": 4,
            "m": 9,
            "upper": 19683,
            "partition_universe_size": 2226,
            "partition_shape": [3, 2, 2, 2],
            "partition_singleton_goods": [0],
            "pool_size": 811,
            "exclude_universal_min": True,
            "exclude_peelable": True,
            "require_pairwise_distinct_rows": True,
            "require_distinct_item_values": True,
            "obstruction_encoding": encoding,
            "favorite_pattern": [0, 0, 0, 0],
            "favorite_pattern_stabilizer": True,
            "solver_status": "UNKNOWN",
            "values": None,
        }
        mismatches = {
            key: {"expected": value, "actual": raw.get(key)}
            for key, value in expected.items()
            if raw.get(key) != value
        }
        if (
            mismatches
            or load_pool(pool_path, 4, 9) != final_pool
            or file_sha256(pool_path) != raw.get("pool_sha256")
        ):
            raise AssertionError((result_path, mismatches))
        proto_path = validate_proto(raw)
        residual_records.append({
            "encoding": encoding,
            "result_path": str(result_path.resolve()),
            "result_sha256": file_sha256(result_path),
            "proto_path": str(proto_path.resolve()),
            "proto_sha256": raw["proto_sha256"],
            "pool_path": str(pool_path.resolve()),
            "pool_sha256": raw["pool_sha256"],
            "solver_status": raw["solver_status"],
            "wall_time_seconds": raw["trace"][-1]["wall_time_seconds"],
        })

    shape_counts = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in final_pool
    )
    return {
        "schema": SCHEMA,
        "status": "SUFFICIENT_CAP_FRONTIER_AUDIT_PASSED",
        "claim": (
            "The common-favorite structural pool was exactly reconstructed "
            "from 15 sufficient-cap models; both generic residual encodings "
            "remain unknown after 900-second solves."
        ),
        "claim_level": "verified research frontier; no theorem verdict",
        "domain": {
            "agents": 4,
            "goods": 9,
            "integer_cap": 19683,
            "favorite_pattern": [0, 0, 0, 0],
            "target_partition_count": len(target_universe),
        },
        "start_pool": {
            "path": str(start_path.resolve()),
            "sha256": file_sha256(start_path),
            "size": 485,
        },
        "final_pool": {
            "path": str(final_path.resolve()),
            "sha256": file_sha256(final_path),
            "size": len(final_pool),
            "shape_counts": {
                "+".join(map(str, shape)): count
                for shape, count in sorted(shape_counts.items())
            },
        },
        "uncut_sessions": session_records,
        "learning_model_count": len(model_flags),
        "learning_models_with_item_ties": sum(
            flags["has_item_ties"] for flags in model_flags
        ),
        "learning_models_with_universal_minimum": sum(
            flags["has_universal_minimum"] for flags in model_flags
        ),
        "learning_models_with_peelable_pair": sum(
            flags["has_peelable_pair"] for flags in model_flags
        ),
        "learning_models_with_repeated_normalized_rows": sum(
            flags["has_repeated_normalized_rows"] for flags in model_flags
        ),
        "first_residual_timeout": {
            "result_path": str(first_residual_path.resolve()),
            "result_sha256": file_sha256(first_residual_path),
            "pool_size": 719,
            "wall_time_seconds": first_residual["trace"][-1][
                "wall_time_seconds"
            ],
        },
        "dual_residual_timeouts": residual_records,
        "interpretation": (
            "The full sufficient cap makes an infeasibility verdict "
            "decisive for the residual cell, but both current encodings "
            "timed out. No countermodel to the target family and no "
            "infeasibility proof was obtained in the generic residual."
        ),
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
