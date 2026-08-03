#!/usr/bin/env python3
"""Audit the normalized aggregate-minimum deletion selector for EFX."""

from __future__ import annotations

import argparse
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path

try:
    from . import core, independent
    from .fast_count import FastParkability
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from fast_count import FastParkability
    from lra_master import ParkabilityLRAMaster


def normalized_aggregate_scores(
    values: tuple[tuple[int, ...], ...],
) -> tuple[Fraction, ...]:
    row_totals = tuple(sum(row) for row in values)
    return tuple(
        sum(
            (Fraction(values[observer][good], row_totals[observer])
             for observer in range(len(values))),
            Fraction(),
        )
        for good in range(len(values[0]))
    )


def aggregate_minimum_goods(
    values: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    scores = normalized_aggregate_scores(values)
    minimum = min(scores)
    return tuple(good for good, score in enumerate(scores) if score == minimum)


def parkable_counts_by_floater(
    values: tuple[tuple[int, ...], ...],
    counter: FastParkability | None = None,
) -> tuple[int, ...]:
    if counter is None:
        counts = [0] * len(values[0])
        for triple in core.iter_parkable_triples(values):
            counts[triple.floater] += 1
        return tuple(counts)
    landscape = counter.landscape(values)
    return tuple(
        sum(host_counts)
        for host_counts in landscape["parkable_triple_count_by_floater_host"]
    )


def selector_failure(
    values: tuple[tuple[int, ...], ...],
    counter: FastParkability | None = None,
) -> dict | None:
    minimizers = aggregate_minimum_goods(values)
    counts = parkable_counts_by_floater(values, counter)
    failed = tuple(good for good in minimizers if counts[good] == 0)
    if not failed:
        return None
    scores = normalized_aggregate_scores(values)
    return {
        "values": [list(row) for row in values],
        "aggregate_scores": [
            f"{score.numerator}/{score.denominator}" for score in scores
        ],
        "aggregate_minimum_goods": list(minimizers),
        "unparkable_aggregate_minimum_goods": list(failed),
        "parkable_triple_count_by_floater": list(counts),
    }


def run_exhaustive(n: int, m: int, levels: tuple[int, ...]) -> dict:
    if not levels or any(level < 1 for level in levels):
        raise ValueError("levels must be positive integers")
    counter = FastParkability(n, m)
    started = time.time()
    checked = 0
    for flat in itertools.product(levels, repeat=n * m):
        values = tuple(
            tuple(flat[observer * m:(observer + 1) * m])
            for observer in range(n)
        )
        failure = selector_failure(values, counter)
        checked += 1
        if failure is not None:
            return {
                "status": "COUNTEREXAMPLE",
                "mode": "exhaustive",
                "n": n,
                "m": m,
                "levels": list(levels),
                "instances_checked": checked,
                "elapsed_seconds": time.time() - started,
                **failure,
            }
    return {
        "status": "EXHAUSTED_NO_COUNTEREXAMPLE",
        "mode": "exhaustive",
        "n": n,
        "m": m,
        "levels": list(levels),
        "instances_checked": checked,
        "elapsed_seconds": time.time() - started,
    }


def run_random(
    n: int,
    m: int,
    samples: int,
    maximum: int,
    seed: int,
) -> dict:
    if samples < 1 or maximum < 1:
        raise ValueError("samples and maximum must be positive")
    counter = FastParkability(n, m)
    rng = random.Random(seed)
    started = time.time()
    for index in range(samples):
        values = tuple(
            tuple(rng.randint(1, maximum) for _ in range(m))
            for _ in range(n)
        )
        failure = selector_failure(values, counter)
        if failure is not None:
            return {
                "status": "COUNTEREXAMPLE",
                "mode": "random",
                "n": n,
                "m": m,
                "samples_requested": samples,
                "instances_checked": index + 1,
                "maximum": maximum,
                "seed": seed,
                "elapsed_seconds": time.time() - started,
                **failure,
            }
    return {
        "status": "NO_COUNTEREXAMPLE",
        "mode": "random",
        "n": n,
        "m": m,
        "samples_requested": samples,
        "instances_checked": samples,
        "maximum": maximum,
        "seed": seed,
        "elapsed_seconds": time.time() - started,
    }


def iter_parkable_triples_for_floater(
    values: tuple[tuple[int, ...], ...],
    floater: int,
):
    for base in core.iter_efx_bases(values, floater):
        owner = tuple(base["base_owner"])
        for host in base["parkable_hosts"]:
            yield core.Triple(floater, owner, host)


def run_cegar(
    n: int,
    m: int,
    floater: int,
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
) -> dict:
    if not 0 <= floater < m:
        raise ValueError("floater is outside the goods range")
    if add_per_iteration < 1 or max_iterations < 0 or time_limit_s < 0:
        raise ValueError("invalid CEGAR limit")
    master = ParkabilityLRAMaster(n, m)
    master.add_aggregate_minimum_good(floater, strict=True)
    pooled: set[core.Triple] = set()
    started = time.time()
    iteration = 0

    while True:
        iteration += 1
        solved = master.solve(time_limit_s=time_limit_s)
        if solved.status != "SAT":
            return {
                "status": (
                    "UNSAT_CANDIDATE"
                    if solved.status == "UNSAT"
                    else "MASTER_UNKNOWN"
                ),
                "mode": "exact_lra_cegar",
                "n": n,
                "m": m,
                "selected_floater": floater,
                "selector": "strict_normalized_aggregate_minimum",
                "iterations": iteration,
                "pool_size": len(pooled),
                "solver_status": solved.raw_status,
                "reason_unknown": solved.reason_unknown,
                "elapsed_seconds": time.time() - started,
                "smt2": master.to_smt2(),
            }

        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
        )
        scores = normalized_aggregate_scores(values)
        if not all(
            scores[floater] < scores[other]
            for other in range(m)
            if other != floater
        ):
            raise AssertionError("decoded candidate lost strict aggregate minimality")

        valid = [
            triple
            for triple in iter_parkable_triples_for_floater(values, floater)
            if triple not in pooled
        ]
        if not valid:
            literal = [
                triple
                for triple in independent.enumerate_base_first(values)
                if triple[0] == floater
            ]
            if literal:
                raise AssertionError("literal verifier found a missed parking triple")
            return {
                "status": "COUNTEREXAMPLE",
                "mode": "exact_lra_cegar",
                "n": n,
                "m": m,
                "selected_floater": floater,
                "selector": "strict_normalized_aggregate_minimum",
                "iterations": iteration,
                "pool_size": len(pooled),
                "values": [list(row) for row in values],
                "aggregate_scores": [
                    f"{score.numerator}/{score.denominator}" for score in scores
                ],
                "complete_efx0_count": independent.count_complete_efx0(values),
                "elapsed_seconds": time.time() - started,
                "smt2": master.to_smt2(),
            }

        selected = valid[:add_per_iteration]
        for triple in selected:
            if not independent.is_parkable_triple(
                values,
                triple.floater,
                triple.base_owner,
                triple.host,
            ):
                raise AssertionError("literal verifier rejected selected triple")
            if not master.add_triple(triple):
                raise AssertionError("new triple was unexpectedly duplicated")
            pooled.add(triple)
        print(
            f"iteration={iteration} pool={len(pooled)} "
            f"candidate_triples={len(valid)} added={len(selected)}",
            flush=True,
        )
        if max_iterations and iteration >= max_iterations:
            return {
                "status": "ITERATION_LIMIT",
                "mode": "exact_lra_cegar",
                "n": n,
                "m": m,
                "selected_floater": floater,
                "selector": "strict_normalized_aggregate_minimum",
                "iterations": iteration,
                "pool_size": len(pooled),
                "elapsed_seconds": time.time() - started,
                "smt2": master.to_smt2(),
            }


def parse_levels(raw: str) -> tuple[int, ...]:
    levels = tuple(int(item) for item in raw.split(","))
    if len(levels) != len(set(levels)):
        raise ValueError("levels must be distinct")
    return levels


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    exhaustive = subparsers.add_parser("exhaustive")
    exhaustive.add_argument("--n", type=int, required=True)
    exhaustive.add_argument("--m", type=int, required=True)
    exhaustive.add_argument("--levels", default="1,2")

    random_parser = subparsers.add_parser("random")
    random_parser.add_argument("--n", type=int, required=True)
    random_parser.add_argument("--m", type=int, required=True)
    random_parser.add_argument("--samples", type=int, required=True)
    random_parser.add_argument("--maximum", type=int, default=100)
    random_parser.add_argument("--seed", type=int, default=20260730)

    cegar = subparsers.add_parser("cegar")
    cegar.add_argument("--n", type=int, required=True)
    cegar.add_argument("--m", type=int, required=True)
    cegar.add_argument("--floater", type=int, default=0)
    cegar.add_argument("--add", type=int, default=128)
    cegar.add_argument("--max-iterations", type=int, default=0)
    cegar.add_argument("--time-limit", type=float, default=0)

    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.mode == "exhaustive":
        result = run_exhaustive(args.n, args.m, parse_levels(args.levels))
    elif args.mode == "random":
        result = run_random(
            args.n,
            args.m,
            args.samples,
            args.maximum,
            args.seed,
        )
    else:
        result = run_cegar(
            args.n,
            args.m,
            args.floater,
            args.add,
            args.max_iterations,
            args.time_limit,
        )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
