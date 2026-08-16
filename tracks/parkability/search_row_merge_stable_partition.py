#!/usr/bin/env python3
"""Search for a row merge whose endpoints share no EFX partition."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

import numpy as np

try:
    from . import core, independent
    from .anneal import atomic_json, mutate
    from .audit_row_merge_interpolation import path_audit
except ImportError:
    import core
    import independent
    from anneal import atomic_json, mutate
    from audit_row_merge_interpolation import path_audit


SCHEMA = "row-merge-stable-partition-search-v1"


class EndpointPartitionEvaluator:
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        assignment_indices = np.arange(n**m, dtype=np.int64)
        goods = np.arange(m, dtype=np.int64)
        assignments = (assignment_indices[:, None] // (n**goods)) % n
        rows = np.arange(len(assignments))
        self.masks = np.zeros((len(assignments), n), dtype=np.int64)
        for good in range(m):
            self.masks[rows, assignments[:, good]] |= 1 << good
        sorted_masks = np.sort(self.masks, axis=1)
        radix = 1 << m
        self.partition_codes = sorted_masks @ (
            radix ** np.arange(n, dtype=np.int64)
        )
        subsets = np.arange(radix, dtype=np.int64)
        self.bits = ((subsets[:, None] >> goods) & 1).astype(bool)

    def support(
        self, raw_values: list[list[int]]
    ) -> tuple[np.ndarray, np.ndarray, int]:
        values = core.validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        matrix = np.asarray(values, dtype=np.int64)
        totals = matrix @ self.bits.T
        sentinel = int(matrix.max()) + 1
        minima = np.where(
            self.bits[None, :, :],
            matrix[:, None, :],
            sentinel,
        ).min(axis=2)
        minima[:, 0] = 0
        thresholds = totals - minima
        valid = np.ones(len(self.masks), dtype=bool)
        normalized_margin = np.full(len(self.masks), np.inf)
        row_totals = matrix.sum(axis=1)
        for observer in range(self.n):
            own = totals[observer, self.masks[:, observer]]
            for target in range(self.n):
                if observer != target:
                    slack = own - thresholds[observer, self.masks[:, target]]
                    valid &= slack >= 0
                    normalized_margin = np.minimum(
                        normalized_margin,
                        slack / row_totals[observer],
                    )
        valid_codes = self.partition_codes[valid]
        codes, inverse = np.unique(valid_codes, return_inverse=True)
        best_margins = np.full(len(codes), -np.inf)
        np.maximum.at(best_margins, inverse, normalized_margin[valid])
        return codes, best_margins, int(valid.sum())


def load_values(path: Path) -> list[list[int]]:
    payload = json.loads(path.read_text())
    values = payload.get("values", payload.get("candidate_values"))
    if values is None:
        raise ValueError(f"{path} contains no values")
    return [list(row) for row in core.validate_values(values, lower=1)]


def merged_values(
    values: list[list[int]], moving: int, base: int
) -> list[list[int]]:
    merged = [row[:] for row in values]
    merged[moving] = merged[base][:]
    return merged


def landscape(
    evaluator: EndpointPartitionEvaluator,
    values: list[list[int]],
    moving: int,
    base: int,
) -> dict:
    target_partitions, target_margins, target_allocations = evaluator.support(values)
    base_partitions, base_margins, base_allocations = evaluator.support(
        merged_values(values, moving, base)
    )
    shared = np.intersect1d(
        target_partitions,
        base_partitions,
        assume_unique=True,
    )
    target_shared = target_margins[
        np.searchsorted(target_partitions, shared)
    ]
    base_shared = base_margins[np.searchsorted(base_partitions, shared)]
    shared_margins = np.minimum(target_shared, base_shared)
    return {
        "shared_endpoint_partition_count": len(shared),
        "target_endpoint_partition_count": len(target_partitions),
        "base_endpoint_partition_count": len(base_partitions),
        "target_endpoint_allocation_count": target_allocations,
        "base_endpoint_allocation_count": base_allocations,
        "weakest_shared_support_margin": (
            float(shared_margins.min()) if len(shared_margins) else None
        ),
        "shared_support_margin_sum": float(shared_margins.sum()),
        "shared_partition_codes": [int(code) for code in shared],
    }


def objective(record: dict) -> float:
    weakest_margin = record["weakest_shared_support_margin"] or 0.0
    return (
        record["shared_endpoint_partition_count"]
        + 0.05 * weakest_margin
        + 0.005 * record["shared_support_margin_sum"]
        + 1e-4
        * (
            record["target_endpoint_partition_count"]
            + record["base_endpoint_partition_count"]
        )
        + 1e-7
        * (
            record["target_endpoint_allocation_count"]
            + record["base_endpoint_allocation_count"]
        )
    )


def best_key(record: dict) -> tuple[int, int, int, int, int]:
    return (
        record["shared_endpoint_partition_count"],
        record["weakest_shared_support_margin"] or 0.0,
        record["shared_support_margin_sum"],
        record["target_endpoint_partition_count"]
        + record["base_endpoint_partition_count"],
        record["target_endpoint_allocation_count"]
        + record["base_endpoint_allocation_count"],
        record["target_endpoint_partition_count"],
        record["target_endpoint_allocation_count"],
    )


def run(
    *,
    seed_path: Path,
    moving: int,
    base: int,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
) -> dict:
    if output_path.exists():
        raise ValueError("output path must be new")
    if iterations < 1 or initial_temperature <= 0 or final_temperature <= 0:
        raise ValueError("positive iterations and temperatures are required")
    values = load_values(seed_path)
    n = len(values)
    m = len(values[0])
    if n != 4 or moving == base or not 0 <= moving < n or not 0 <= base < n:
        raise ValueError("distinct moving/base agents in a four-agent profile required")
    evaluator = EndpointPartitionEvaluator(n, m)
    rng = random.Random(random_seed)
    started = time.time()
    current = [row[:] for row in values]
    current_record = landscape(evaluator, current, moving, base)
    best = [row[:] for row in current]
    best_record = dict(current_record)
    accepted = 0
    improvements = 0

    for iteration in range(1, iterations + 1):
        candidate = mutate(
            current,
            current_record["shared_endpoint_partition_count"],
            rng,
        )
        if candidate == current:
            continue
        candidate_record = landscape(evaluator, candidate, moving, base)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = objective(candidate_record) - objective(current_record)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_record = candidate_record
            accepted += 1
        if best_key(candidate_record) < best_key(best_record):
            best = [row[:] for row in candidate]
            best_record = dict(candidate_record)
            improvements += 1
            print(
                f"iteration={iteration} shared="
                f"{best_record['shared_endpoint_partition_count']} "
                f"target={best_record['target_endpoint_partition_count']} "
                f"base={best_record['base_endpoint_partition_count']}",
                flush=True,
            )
            if best_record["shared_endpoint_partition_count"] == 0:
                break

    status = "CHECKPOINT"
    exact_audit = None
    if best_record["shared_endpoint_partition_count"] == 0:
        audit = path_audit(best, moving, base)
        target_count = independent.count_complete_efx0(best)
        base_count = independent.count_complete_efx0(
            merged_values(best, moving, base)
        )
        if (
            audit["stable_partition"] is not None
            or audit["full_path_partition_count"] != 0
            or audit["efx_allocation_count_at_one"] != target_count
            or audit["efx_allocation_count_at_zero"] != base_count
        ):
            raise AssertionError("zero-overlap candidate failed exact path audit")
        status = "NO_STABLE_PARTITION"
        exact_audit = audit

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": (
            "No shared endpoint partition refutes fixed-partition row-merge "
            "coverage for this profile. It does not refute EFX existence or "
            "row-merge continuation by changing partitions."
        ),
        "seed": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "n": n,
        "m": m,
        "moving_agent": moving,
        "base_agent": base,
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "values": best,
        "merged_endpoint_values": merged_values(best, moving, base),
        "landscape": best_record,
        "exact_path_audit": exact_audit,
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--moving", type=int, default=3)
    parser.add_argument("--base", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=1.0)
    parser.add_argument("--final-temperature", type=float, default=0.01)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        moving=args.moving,
        base=args.base,
        iterations=args.iterations,
        random_seed=args.random_seed,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        output_path=args.output,
    )
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
