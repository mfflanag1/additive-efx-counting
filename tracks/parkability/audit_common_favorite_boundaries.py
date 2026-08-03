#!/usr/bin/env python3
"""Audit the tight common-favorite and residual-family boundaries."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .anneal_efx_family import has_common_strict_favorite
    from .fast_count import FastParkability
    from .run_integer_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from anneal_efx_family import has_common_strict_favorite
    from fast_count import FastParkability
    from run_integer_partition_cegar import supported_partitions


SCHEMA = "common-favorite-efx-4x9-boundary-audit-v1"
TIGHT_VALUES = (
    (15, 11, 12, 2, 2, 2, 1, 2, 2),
    (16, 15, 2, 3, 1, 4, 3, 3, 3),
    (24, 8, 10, 1, 1, 1, 1, 3, 1),
    (19, 10, 11, 1, 1, 1, 2, 3, 2),
)
RESIDUAL_FALSIFICATION_VALUES = (
    (13, 12, 7, 6, 5, 4, 3, 2, 1),
) * 4
EXPECTED = {
    "tight18": {
        "values": TIGHT_VALUES,
        "labeled_shapes": {(6, 1, 1, 1): 12, (5, 2, 1, 1): 6},
        "unlabeled_shapes": {(6, 1, 1, 1): 1, (5, 2, 1, 1): 1},
        "source": "efx49_common_favorite_family_anneal_seed132.json",
    },
    "balanced_or_residual_falsification": {
        "values": RESIDUAL_FALSIFICATION_VALUES,
        "labeled_shapes": {
            (3, 3, 2, 1): 288,
            (4, 2, 2, 1): 120,
            (4, 3, 1, 1): 72,
        },
        "unlabeled_shapes": {
            (3, 3, 2, 1): 12,
            (4, 2, 2, 1): 5,
            (4, 3, 1, 1): 3,
        },
        "source": (
            "efx49_rankgap13_common_balanced_or_residual6111_"
            "matching_session1.json"
        ),
    },
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(assignment: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (assignment.count(agent) for agent in range(4)),
            reverse=True,
        )
    )


def shape_key(bundle_shape: tuple[int, ...]) -> str:
    return "+".join(map(str, bundle_shape))


def residual_matching_sets(
    values: tuple[tuple[int, ...], ...],
) -> list[tuple[int, ...]]:
    successful = []
    for residual in itertools.combinations(range(9), 6):
        singletons = tuple(good for good in range(9) if good not in residual)
        edges = [
            [
                values[agent][good]
                >= sum(values[agent][item] for item in residual)
                - min(values[agent][item] for item in residual)
                for good in singletons
            ]
            for agent in range(4)
        ]
        if any(
            all(edges[agent][position] for position, agent in enumerate(matching))
            for matching in itertools.permutations(range(4), 3)
        ):
            successful.append(residual)
    return successful


def audit(results_dir: Path) -> dict:
    universe = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    audited = []
    for name, expected in EXPECTED.items():
        values = expected["values"]
        source_path = results_dir / expected["source"]
        source = json.loads(source_path.read_text())
        frozen_values = tuple(tuple(row) for row in source.get("values") or ())
        if frozen_values != values:
            raise AssertionError(f"{name} source matrix changed")
        if name == "tight18":
            expected_source = {
                "schema": "complete-efx-family-anneal-result-v1",
                "status": "CHECKPOINT",
                "iterations_requested": 30000,
                "iterations_completed": 30000,
                "random_seed": 132,
                "shape_codes": [3222],
                "singleton_goods": [0],
                "common_favorite_good": 0,
            }
            if source.get("landscape", {}).get(
                "complete_efx0_family_count"
            ) != 18:
                raise AssertionError("tight18 source landscape changed")
        else:
            expected_source = {
                "schema": "integer-partition-cp-sat-result-v1",
                "status": "ZERO_SUPPORTED_PARTITIONS",
                "n": 4,
                "m": 9,
                "upper": 13,
                "partition_shape": None,
                "partition_shapes": [[6, 1, 1, 1], [3, 2, 2, 2]],
                "require_distinct_item_values": True,
                "favorite_pattern": [0, 0, 0, 0],
                "favorite_pattern_stabilizer": True,
                "obstruction_encoding": "matching_clauses",
                "solver_status": "OPTIMAL",
            }
        mismatches = {
            key: {"expected": value, "actual": source.get(key)}
            for key, value in expected_source.items()
            if source.get(key) != value
        }
        if mismatches:
            raise AssertionError((source_path, mismatches))
        if name == "tight18":
            for seed, digest in source.get("seed_sha256", {}).items():
                seed_path = results_dir / Path(seed).name
                if not seed_path.is_file() or file_sha256(seed_path) != digest:
                    raise AssertionError("tight18 seed chain is broken")
        else:
            proto_path = results_dir / Path(source["proto_path"]).name
            pool_path = results_dir / (
                "efx49_rankgap13_common_balanced_or_residual6111_"
                "matching_pool.json"
            )
            if (
                not proto_path.is_file()
                or file_sha256(proto_path) != source["proto_sha256"]
                or not pool_path.is_file()
                or file_sha256(pool_path) != source["pool_sha256"]
            ):
                raise AssertionError("residual-family artifact chain is broken")
        if not has_common_strict_favorite(
            [list(row) for row in values],
            0,
        ):
            raise AssertionError(f"{name} lost its strict common favorite")

        literal_shapes: Counter[tuple[int, ...]] = Counter()
        for assignment in itertools.product(range(4), repeat=9):
            if independent.is_complete_efx0(values, assignment):
                literal_shapes[shape(assignment)] += 1
        core_assignments = list(core.iter_efx0_assignments(values))
        if (
            dict(literal_shapes) != expected["labeled_shapes"]
            or len(core_assignments) != sum(literal_shapes.values())
        ):
            raise AssertionError(f"{name} labeled census changed")

        supported = supported_partitions(values, universe)
        supported_shapes = Counter(
            tuple(sorted(map(len, partition), reverse=True))
            for partition in supported
        )
        if (
            dict(supported_shapes) != expected["unlabeled_shapes"]
            or any((0,) not in partition for partition in supported)
        ):
            raise AssertionError(f"{name} partition census changed")

        residuals = residual_matching_sets(values)
        residual_partitions = [
            partition
            for partition in supported
            if tuple(sorted(map(len, partition), reverse=True))
            == (6, 1, 1, 1)
        ]
        if len(residuals) != len(residual_partitions):
            raise AssertionError(f"{name} residual-threshold lemma replay failed")

        audited.append({
            "name": name,
            "source_path": str(source_path.resolve()),
            "source_sha256": file_sha256(source_path),
            "values": [list(row) for row in values],
            "strict_common_favorite_good": 0,
            "labeled_complete_efx_count": sum(literal_shapes.values()),
            "labeled_shape_counts": {
                shape_key(bundle_shape): count
                for bundle_shape, count in sorted(literal_shapes.items())
            },
            "unlabeled_supported_partition_count": len(supported),
            "unlabeled_shape_counts": {
                shape_key(bundle_shape): count
                for bundle_shape, count in sorted(supported_shapes.items())
            },
            "all_supporting_partitions_isolate_common_favorite": True,
            "balanced_partition_count": supported_shapes[(3, 2, 2, 2)],
            "residual_6111_partition_count": len(residual_partitions),
            "residual_threshold_matching_sets": [
                list(residual) for residual in residuals
            ],
        })

    evaluator = FastParkability(4, 9)
    one_row_transfer_counts = []
    values = [list(row) for row in TIGHT_VALUES]
    for agent in range(4):
        for source in range(9):
            for target in range(9):
                if source == target:
                    continue
                for amount in range(1, values[agent][source]):
                    candidate = [row[:] for row in values]
                    candidate[agent][source] -= amount
                    candidate[agent][target] += amount
                    if not has_common_strict_favorite(candidate, 0):
                        continue
                    one_row_transfer_counts.append(
                        evaluator.complete_efx0_family_landscape(
                            candidate,
                            shape_codes=(3222,),
                            singleton_goods=(0,),
                        )["complete_efx0_family_count"]
                    )
    if (
        len(one_row_transfer_counts) != 841
        or min(one_row_transfer_counts) != 18
    ):
        raise AssertionError("tight18 one-row transfer boundary changed")

    continuation_records = []
    for seed in (135, 136, 137):
        continuation_path = (
            results_dir
            / f"efx49_common_favorite_family_anneal_seed{seed}.json"
        )
        continuation = json.loads(continuation_path.read_text())
        expected_continuation = {
            "schema": "complete-efx-family-anneal-result-v1",
            "status": "CHECKPOINT",
            "iterations_requested": 60000,
            "iterations_completed": 60000,
            "random_seed": seed,
            "shape_codes": [3222],
            "singleton_goods": [0],
            "common_favorite_good": 0,
            "improvements": 0,
            "values": [list(row) for row in TIGHT_VALUES],
        }
        mismatches = {
            key: {"expected": value, "actual": continuation.get(key)}
            for key, value in expected_continuation.items()
            if continuation.get(key) != value
        }
        if (
            mismatches
            or continuation.get("landscape", {}).get(
                "complete_efx0_family_count"
            )
            != 18
        ):
            raise AssertionError((continuation_path, mismatches))
        for source, digest in continuation.get("seed_sha256", {}).items():
            source_path = Path(source)
            if not source_path.is_file() or file_sha256(source_path) != digest:
                raise AssertionError("continuation seed chain is broken")
        continuation_records.append({
            "random_seed": seed,
            "result_path": str(continuation_path.resolve()),
            "result_sha256": file_sha256(continuation_path),
            "iterations": continuation["iterations_completed"],
            "accepted_moves": continuation["accepted_moves"],
            "improvements": continuation["improvements"],
            "best_family_count": continuation["landscape"][
                "complete_efx0_family_count"
            ],
        })

    return {
        "schema": SCHEMA,
        "status": "COMMON_FAVORITE_BOUNDARY_AUDIT_PASSED",
        "claim": (
            "The tight profile has exactly 18 complete EFX allocations, all "
            "favorite-singleton; the cap-13 identical-row profile refutes "
            "balanced-or-(6,1,1,1) while preserving favorite-singleton EFX."
        ),
        "cases": audited,
        "tight18_local_transfer_audit": {
            "positive_one_row_transfers_preserving_common_favorite": len(
                one_row_transfer_counts
            ),
            "minimum_target_family_count": min(one_row_transfer_counts),
            "meaning": (
                "heuristic local-minimum evidence only; not a proof of "
                "global minimality or existence"
            ),
        },
        "tight18_independent_continuations": continuation_records,
        "limitations": [
            "Neither profile is an additive-EFX counterexample.",
            "The 18-allocation endpoint is heuristic search output.",
            "The residual-family falsification rules out only the two-shape cover.",
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
