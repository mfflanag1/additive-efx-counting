#!/usr/bin/env python3
"""Adversarial search for a zero-support extended rank-one bridge profile."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

import numpy as np

try:
    from . import core
    from .anneal import append_jsonl, atomic_json
    from .optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_rank_one_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )
except ImportError:
    import core
    from anneal import append_jsonl, atomic_json
    from optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_rank_one_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )


SCHEMA = "common-favorite-rank1-extended-bridge-anneal-v1"


class PartitionFamilyEvaluator:
    def __init__(self, partitions, n: int = 4, m: int = 9) -> None:
        self.n = n
        self.m = m
        self.partitions = tuple(partitions)
        subsets = np.arange(1 << m, dtype=np.int64)
        goods = np.arange(m, dtype=np.int64)
        self.bits = ((subsets[:, None] >> goods) & 1).astype(np.int64)
        self.masks = np.asarray(
            [
                [sum(1 << good for good in bundle) for bundle in partition]
                for partition in self.partitions
            ],
            dtype=np.int64,
        )
        if self.masks.shape != (len(self.partitions), n):
            raise ValueError("every partition must contain n bundles")
        self.permutations = np.asarray(
            tuple(itertools.permutations(range(n))),
            dtype=np.int64,
        )

    def support_mask(self, raw_values) -> np.ndarray:
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
            self.bits[None, :, :].astype(bool),
            matrix[:, None, :],
            sentinel,
        ).min(axis=2)
        minima[:, 0] = 0
        thresholds = totals - minima
        bundle_values = np.transpose(totals[:, self.masks], (1, 0, 2))
        maximum_thresholds = thresholds[:, self.masks].max(axis=2).T
        feasible = bundle_values >= maximum_thresholds[:, :, None]
        support = np.zeros(len(self.partitions), dtype=bool)
        agents = np.arange(self.n)
        for permutation in self.permutations:
            support |= feasible[:, agents, permutation].all(axis=1)
        return support

    def support_count(self, values) -> int:
        return int(self.support_mask(values).sum())


def load_values(path: Path, upper: int):
    document = json.loads(path.read_text())
    raw = document.get("best_values", document.get("values"))
    return core.validate_values(
        raw,
        expected_n=4,
        expected_m=9,
        lower=1,
        upper=upper,
    )


def diversity_key(values) -> tuple[int, int]:
    residents = values[1:]
    identical_pairs = sum(
        residents[left] == residents[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    coordinate_equalities = sum(
        residents[left][good] == residents[right][good]
        for left in range(3)
        for right in range(left + 1, 3)
        for good in range(9)
    )
    return identical_pairs, coordinate_equalities


def search_key(values, singleton_support: int) -> tuple[int, int, int]:
    return singleton_support, *diversity_key(values)


def energy(values, singleton_support: int) -> float:
    identical, coordinate_equalities = diversity_key(values)
    return singleton_support + identical * 0.02 + coordinate_equalities * 0.0002


def mutate(values, upper: int, rng: random.Random):
    candidate = [list(row) for row in values]
    draw = rng.random()
    coordinate_count = 1 if draw < 0.65 else 2 if draw < 0.93 else 3
    coordinates = rng.sample(tuple(itertools.product(range(4), range(9))), coordinate_count)
    changed = False
    for observer, good in coordinates:
        old = candidate[observer][good]
        new = rng.randint(1, upper - 1)
        if new >= old:
            new += 1
        candidate[observer][good] = new
        changed |= new != old
    return tuple(tuple(row) for row in candidate) if changed else values


def run(
    *,
    seed_path: Path,
    upper: int,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        upper < 2
        or iterations < 1
        or initial_temperature <= 0
        or final_temperature <= 0
        or output_path.exists()
        or (trace_path is not None and trace_path.exists())
    ):
        raise ValueError("valid parameters and new output paths are required")
    singleton_universe = singleton_partitions()
    repairs = repair_partitions("bridge45")
    singleton_evaluator = PartitionFamilyEvaluator(singleton_universe)
    repair_evaluator = PartitionFamilyEvaluator(repairs)
    current = load_values(seed_path, upper)
    if not in_rank_one_cell(current) or repair_evaluator.support_count(current):
        raise ValueError("seed is outside the blocked extended-bridge cell")
    literal_seed_support = len(supporting_singletons(current, singleton_universe))
    current_support = singleton_evaluator.support_count(current)
    if literal_seed_support != current_support:
        raise AssertionError("vectorized and literal seed support disagree")
    best = current
    best_support = current_support
    rng = random.Random(random_seed)
    accepted = 0
    valid_candidates = 0
    improvements = 0
    started = time.time()

    for iteration in range(1, iterations + 1):
        candidate = mutate(current, upper, rng)
        if candidate == current or not in_rank_one_cell(candidate):
            continue
        if repair_evaluator.support_count(candidate):
            continue
        valid_candidates += 1
        candidate_support = singleton_evaluator.support_count(candidate)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = energy(candidate, candidate_support) - energy(
            current,
            current_support,
        )
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_support = candidate_support
            accepted += 1
        if search_key(candidate, candidate_support) < search_key(
            best,
            best_support,
        ):
            best = candidate
            best_support = candidate_support
            improvements += 1
            record = {
                "iteration": iteration,
                "elapsed_seconds": round(time.time() - started, 6),
                "singleton_support_count": best_support,
                "diversity_key": list(diversity_key(best)),
                "values": [list(row) for row in best],
            }
            append_jsonl(trace_path, record)
            print(
                f"iteration={iteration} support={best_support} "
                f"diversity={diversity_key(best)}",
                flush=True,
            )
            if best_support == 0:
                break

    literal_best_support = len(supporting_singletons(best, singleton_universe))
    if (
        literal_best_support != best_support
        or repair_evaluator.support_count(best)
        or not in_rank_one_cell(best)
    ):
        raise AssertionError("final literal replay disagrees with search state")
    result = {
        "schema": SCHEMA,
        "status": (
            "ZERO_SINGLETON_EXTENDED_BRIDGE_COUNTEREXAMPLE_CANDIDATE"
            if best_support == 0
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A zero profile refutes only the 45-state extended rank-one "
            "bridge lemma, not complete additive EFX; independent full "
            "allocation replay is required before promotion."
        ),
        "seed": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "upper": upper,
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "valid_candidate_count": valid_candidates,
        "accepted_move_count": accepted,
        "improvement_count": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "singleton_partition_count": len(singleton_universe),
        "repair_partition_count": len(repairs),
        "best_singleton_support_count": best_support,
        "best_diversity_key": list(diversity_key(best)),
        "values": [list(row) for row in best],
        "claim_boundary": (
            "This is adversarial search in one bounded local proof cell. "
            "It neither proves the bridge lemma nor decides complete EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--upper", type=int, default=6)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=1.5)
    parser.add_argument("--final-temperature", type=float, default=0.01)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    run(
        seed_path=args.seed,
        upper=args.upper,
        iterations=args.iterations,
        random_seed=args.random_seed,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        output_path=args.output,
        trace_path=args.trace,
    )


if __name__ == "__main__":
    main()
