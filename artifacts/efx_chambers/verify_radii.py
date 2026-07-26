#!/usr/bin/env python3
"""Verify exact rational EFX0 chamber radii for the six count-n witnesses."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import time
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_MANIFEST = ROOT / "repro/counting_witnesses/instances.json"
CERTIFICATES = HERE / "certificates.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": str(value),
    }


def constraint_records(values: list[list[int]], assignment: list[int]) -> list[dict]:
    n = len(values)
    bundles = [[] for _ in range(n)]
    for good, owner in enumerate(assignment):
        bundles[owner].append(good)
    records = []
    for removed_good, target in enumerate(assignment):
        target_remainder = [
            good for good in bundles[target] if good != removed_good
        ]
        for observer in range(n):
            if observer == target:
                continue
            own = bundles[observer]
            slack = sum(values[observer][good] for good in own) - sum(
                values[observer][good] for good in target_remainder
            )
            support = len(own) + len(target_remainder)
            records.append(
                {
                    "observer": observer,
                    "target": target,
                    "removed_good": removed_good,
                    "own_size": len(own),
                    "target_remainder_size": len(target_remainder),
                    "slack": slack,
                    "support": support,
                    "normalized_slack": (
                        str(Fraction(slack, support)) if support else "0"
                    ),
                }
            )
    return records


def extremal_constraint(
    values: list[list[int]],
    assignment: list[int],
    mode: str,
) -> dict:
    records = constraint_records(values, assignment)
    if mode == "efx":
        candidates = [record for record in records if record["support"] > 0]
        return min(
            candidates,
            key=lambda record: Fraction(
                record["slack"], record["support"]
            ),
        )
    if mode == "kill":
        candidates = [
            record
            for record in records
            if record["support"] > 0 and record["slack"] < 0
        ]
        return max(
            candidates,
            key=lambda record: Fraction(
                -record["slack"], record["support"]
            ),
        )
    raise ValueError(mode)


def enumerate_allocations(
    values: list[list[int]], chunk_size: int
) -> dict:
    n = len(values)
    m = len(values[0])
    total_allocations = n**m
    scale = math.lcm(*range(1, m)) if m > 1 else 1
    value_array = np.asarray(values, dtype=np.int64)
    maximum = int(value_array.max(initial=0))
    assert m * maximum * scale < (1 << 62)

    efx_count = 0
    efx_allocations = []
    efx_zero_constraints = 0
    efx_zero_allocations = 0
    efx_tautologies = 0
    global_efx_normalized = None
    global_efx_assignment = None
    global_efx_raw_slack = None
    global_kill_normalized = None
    global_kill_assignment = None

    for start in range(0, total_allocations, chunk_size):
        stop = min(start + chunk_size, total_allocations)
        size = stop - start
        indices = np.arange(start, stop, dtype=np.int64)
        work = indices.copy()
        assignments = np.empty((size, m), dtype=np.int8)
        for good in range(m):
            assignments[:, good] = work % n
            work //= n

        counts = np.empty((size, n), dtype=np.int16)
        for owner in range(n):
            counts[:, owner] = np.count_nonzero(
                assignments == owner, axis=1
            )

        is_efx = np.ones(size, dtype=bool)
        row_min_normalized = np.full(size, 1 << 62, dtype=np.int64)
        row_min_raw = np.full(size, 1 << 62, dtype=np.int64)
        row_best_kill = np.zeros(size, dtype=np.int64)
        row_zero_constraints = np.zeros(size, dtype=np.int16)
        row_tautologies = np.zeros(size, dtype=np.int16)
        rows = np.arange(size)

        for observer in range(n):
            totals = np.zeros((size, n), dtype=np.int64)
            for good in range(m):
                totals[rows, assignments[:, good]] += value_array[
                    observer, good
                ]
            own = totals[:, observer]
            own_count = counts[:, observer].astype(np.int64)

            for removed_good in range(m):
                targets = assignments[:, removed_good].astype(np.intp)
                active = targets != observer
                target_remainder = (
                    totals[rows, targets]
                    - value_array[observer, removed_good]
                )
                slack = own - target_remainder
                support = (
                    own_count
                    + counts[rows, targets].astype(np.int64)
                    - 1
                )
                is_efx &= (~active) | (slack >= 0)

                tautological = active & (support == 0)
                assert np.all(slack[tautological] == 0)
                row_tautologies += tautological
                valid = active & (support > 0)
                row_zero_constraints += valid & (slack == 0)
                row_min_raw = np.where(
                    valid & (slack < row_min_raw), slack, row_min_raw
                )

                factor = np.ones(size, dtype=np.int64)
                factor[valid] = scale // support[valid]
                normalized = slack * factor
                row_min_normalized = np.where(
                    valid & (normalized < row_min_normalized),
                    normalized,
                    row_min_normalized,
                )
                violation = valid & (slack < 0)
                row_best_kill = np.where(
                    violation & (-normalized > row_best_kill),
                    -normalized,
                    row_best_kill,
                )

        efx_rows = np.flatnonzero(is_efx)
        non_efx_rows = np.flatnonzero(~is_efx)
        efx_count += len(efx_rows)
        efx_allocations.extend(
            assignments[row].astype(int).tolist() for row in efx_rows
        )
        efx_zero_constraints += int(row_zero_constraints[efx_rows].sum())
        efx_zero_allocations += int(
            np.count_nonzero(row_zero_constraints[efx_rows])
        )
        efx_tautologies += int(row_tautologies[efx_rows].sum())

        if len(efx_rows):
            local_raw_slack = int(row_min_raw[efx_rows].min())
            if (
                global_efx_raw_slack is None
                or local_raw_slack < global_efx_raw_slack
            ):
                global_efx_raw_slack = local_raw_slack
            local_row = efx_rows[
                np.argmin(row_min_normalized[efx_rows])
            ]
            local_value = int(row_min_normalized[local_row])
            if (
                global_efx_normalized is None
                or local_value < global_efx_normalized
            ):
                global_efx_normalized = local_value
                global_efx_assignment = assignments[local_row].astype(
                    int
                ).tolist()

        if len(non_efx_rows):
            assert np.all(row_best_kill[non_efx_rows] > 0)
            local_row = non_efx_rows[
                np.argmin(row_best_kill[non_efx_rows])
            ]
            local_value = int(row_best_kill[local_row])
            if (
                global_kill_normalized is None
                or local_value < global_kill_normalized
            ):
                global_kill_normalized = local_value
                global_kill_assignment = assignments[local_row].astype(
                    int
                ).tolist()

    assert global_efx_normalized is not None
    assert global_kill_normalized is not None
    efx_margin = Fraction(global_efx_normalized, scale)
    kill_margin = Fraction(global_kill_normalized, scale)
    positivity_margin = Fraction(min(min(row) for row in values), 1)

    if efx_zero_constraints:
        open_radius = Fraction(0, 1)
        closed_radius = Fraction(0, 1)
        status = "OBSTRUCTED"
    else:
        open_radius = min(
            efx_margin, kill_margin, positivity_margin
        )
        closed_radius = open_radius / 2
        status = "CERTIFIED"

    efx_constraint = extremal_constraint(
        values, global_efx_assignment, "efx"
    )
    kill_constraint = extremal_constraint(
        values, global_kill_assignment, "kill"
    )
    assert Fraction(
        efx_constraint["slack"], efx_constraint["support"]
    ) == efx_margin
    assert Fraction(
        -kill_constraint["slack"], kill_constraint["support"]
    ) == kill_margin

    return {
        "status": status,
        "allocation_space": total_allocations,
        "efx0_count": efx_count,
        "efx0_allocations": sorted(efx_allocations),
        "nontrivial_efx_zero_constraints": efx_zero_constraints,
        "efx_allocations_with_nontrivial_zero": efx_zero_allocations,
        "tautological_zero_constraints": efx_tautologies,
        "minimum_raw_efx_slack": global_efx_raw_slack,
        "efx_normalized_margin": fraction_record(efx_margin),
        "non_efx_kill_margin": fraction_record(kill_margin),
        "positive_orthant_margin": fraction_record(positivity_margin),
        "certified_open_radius": fraction_record(open_radius),
        "certified_closed_radius": fraction_record(closed_radius),
        "efx_margin_witness": {
            "allocation": global_efx_assignment,
            "constraint": efx_constraint,
        },
        "kill_margin_witness": {
            "allocation": global_kill_assignment,
            "constraint": kill_constraint,
        },
    }


def source_records() -> list[dict]:
    manifest = json.loads(SOURCE_MANIFEST.read_text())
    return manifest["instances"]


def compute_record(source: dict, chunk_size: int) -> dict:
    source_path = ROOT / source["path"]
    actual_hash = sha256(source_path)
    assert actual_hash == source["sha256"]
    instance = json.loads(source_path.read_text())
    values = instance["values"]
    n, m = instance["n"], instance["m"]
    assert len(values) == n
    assert all(len(row) == m for row in values)
    assert all(
        type(value) is int and value > 0
        for row in values
        for value in row
    )
    computed = enumerate_allocations(values, chunk_size)
    assert computed["efx0_count"] == source["expected_efx0_count"]
    return {
        "id": source["id"],
        "source": source["path"],
        "source_sha256": source["sha256"],
        "n": n,
        "m": m,
        "expected_efx0_count": source["expected_efx0_count"],
        **computed,
    }


def verify_expected(actual: dict, expected: dict) -> None:
    for key, value in expected.items():
        assert actual.get(key) == value, (
            actual["id"],
            key,
            actual.get(key),
            value,
        )


def obstruction_regression() -> dict:
    result = enumerate_allocations([[1, 1, 1], [1, 1, 1]], 64)
    assert result["status"] == "OBSTRUCTED"
    assert result["nontrivial_efx_zero_constraints"] > 0
    assert result["efx_allocations_with_nontrivial_zero"] > 0
    assert result["certified_open_radius"]["fraction"] == "0"
    assert result["certified_closed_radius"]["fraction"] == "0"
    return {
        "status": result["status"],
        "nontrivial_efx_zero_constraints": result[
            "nontrivial_efx_zero_constraints"
        ],
        "efx_allocations_with_nontrivial_zero": result[
            "efx_allocations_with_nontrivial_zero"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-size", type=int, default=1 << 18)
    parser.add_argument("--compute-only", action="store_true")
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()
    assert args.chunk_size > 0

    requested = set(args.only)
    sources = [
        source
        for source in source_records()
        if not requested or source["id"] in requested
    ]
    assert {source["id"] for source in sources} == (
        requested or {source["id"] for source in source_records()}
    )
    expected_by_id = {}
    if not args.compute_only:
        certificate = json.loads(CERTIFICATES.read_text())
        assert certificate["source_manifest"] == str(
            SOURCE_MANIFEST.relative_to(ROOT)
        )
        assert certificate["source_manifest_sha256"] == sha256(
            SOURCE_MANIFEST
        )
        expected_by_id = {
            record["id"]: record for record in certificate["witnesses"]
        }
        assert set(expected_by_id) == {
            source["id"] for source in source_records()
        }

    started = time.perf_counter()
    obstruction = obstruction_regression()
    records = []
    for source in sources:
        record_started = time.perf_counter()
        record = compute_record(source, args.chunk_size)
        if not args.compute_only:
            verify_expected(record, expected_by_id[record["id"]])
        records.append(record)
        print(
            f'PASS {record["id"]}: count={record["efx0_count"]}, '
            f'open={record["certified_open_radius"]["fraction"]}, '
            f'closed={record["certified_closed_radius"]["fraction"]}, '
            f'zero={record["nontrivial_efx_zero_constraints"]}, '
            f'seconds={time.perf_counter() - record_started:.3f}',
            flush=True,
        )

    output = {
        "schema": 1,
        "status": "PASS",
        "mode": "compute-only" if args.compute_only else "verified",
        "source_manifest": str(SOURCE_MANIFEST.relative_to(ROOT)),
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "equality_obstruction_regression": obstruction,
        "witnesses": records,
        "seconds": round(time.perf_counter() - started, 6),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
