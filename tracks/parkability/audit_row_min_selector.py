#!/usr/bin/env python3
"""Audit whether some row-minimum good is always EFX-parkable."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from pathlib import Path

try:
    from . import core, independent
    from .audit_aggregate_min_selector import (
        iter_parkable_triples_for_floater,
        parkable_counts_by_floater,
    )
    from .fast_count import FastParkability
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from audit_aggregate_min_selector import (
        iter_parkable_triples_for_floater,
        parkable_counts_by_floater,
    )
    from fast_count import FastParkability
    from lra_master import ParkabilityLRAMaster


def row_minimum_goods(
    values: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    return tuple(sorted({
        good
        for row in values
        for good, value in enumerate(row)
        if value == min(row)
    }))


def selector_failure(
    values: tuple[tuple[int, ...], ...],
    counter: FastParkability | None = None,
) -> dict | None:
    selected = row_minimum_goods(values)
    counts = parkable_counts_by_floater(values, counter)
    if any(counts[good] for good in selected):
        return None
    return {
        "values": [list(row) for row in values],
        "row_minimum_goods": list(selected),
        "parkable_triple_count_by_floater": list(counts),
    }


def run_random(
    n: int,
    m: int,
    samples: int,
    maximum: int,
    seed: int,
) -> dict:
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
        "instances_checked": samples,
        "maximum": maximum,
        "seed": seed,
        "elapsed_seconds": time.time() - started,
    }


def run_cegar(
    n: int,
    m: int,
    pattern: tuple[int, ...],
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
    smt2_path: Path | None,
) -> dict:
    if (
        len(pattern) != n
        or any(not 0 <= good < m for good in pattern)
        or add_per_iteration < 1
        or max_iterations < 0
        or time_limit_s < 0
    ):
        raise ValueError("invalid CEGAR parameters")
    selected_goods = tuple(sorted(set(pattern)))
    master = ParkabilityLRAMaster(n, m)
    master.add_strict_minimum_pattern(pattern)
    pooled: set[core.Triple] = set()
    started = time.time()
    iteration = 0

    def formula_record() -> dict:
        formula = master.to_smt2()
        record = {
            "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        }
        if smt2_path is not None:
            smt2_path.parent.mkdir(parents=True, exist_ok=True)
            smt2_path.write_text(formula)
            record["smt2_path"] = str(smt2_path.resolve())
        return record

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
                "strict_row_minimum_pattern": list(pattern),
                "selected_goods": list(selected_goods),
                "iterations": iteration,
                "pool_size": len(pooled),
                "solver_status": solved.raw_status,
                "reason_unknown": solved.reason_unknown,
                "elapsed_seconds": time.time() - started,
                **formula_record(),
            }

        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
        )
        if any(
            values[observer][minimum]
            >= min(
                values[observer][other]
                for other in range(m)
                if other != minimum
            )
            for observer, minimum in enumerate(pattern)
        ):
            raise AssertionError("decoded candidate lost strict row minima")

        valid = [
            triple
            for floater in selected_goods
            for triple in iter_parkable_triples_for_floater(values, floater)
            if triple not in pooled
        ]
        if not valid:
            literal = [
                triple
                for triple in independent.enumerate_base_first(values)
                if triple[0] in selected_goods
            ]
            if literal:
                raise AssertionError("literal verifier found a missed parking triple")
            return {
                "status": "COUNTEREXAMPLE",
                "mode": "exact_lra_cegar",
                "n": n,
                "m": m,
                "strict_row_minimum_pattern": list(pattern),
                "selected_goods": list(selected_goods),
                "iterations": iteration,
                "pool_size": len(pooled),
                "values": [list(row) for row in values],
                "parkable_triple_count_by_floater": list(
                    parkable_counts_by_floater(values)
                ),
                "complete_efx0_count": independent.count_complete_efx0(values),
                "elapsed_seconds": time.time() - started,
                **formula_record(),
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
                "strict_row_minimum_pattern": list(pattern),
                "selected_goods": list(selected_goods),
                "iterations": iteration,
                "pool_size": len(pooled),
                "elapsed_seconds": time.time() - started,
                **formula_record(),
            }


def parse_pattern(raw: str) -> tuple[int, ...]:
    return tuple(int(item) for item in raw.split(","))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    random_parser = subparsers.add_parser("random")
    random_parser.add_argument("--n", type=int, required=True)
    random_parser.add_argument("--m", type=int, required=True)
    random_parser.add_argument("--samples", type=int, required=True)
    random_parser.add_argument("--maximum", type=int, default=100)
    random_parser.add_argument("--seed", type=int, default=20260730)

    cegar = subparsers.add_parser("cegar")
    cegar.add_argument("--n", type=int, required=True)
    cegar.add_argument("--m", type=int, required=True)
    cegar.add_argument("--pattern", required=True)
    cegar.add_argument("--add", type=int, default=128)
    cegar.add_argument("--max-iterations", type=int, default=0)
    cegar.add_argument("--time-limit", type=float, default=0)
    cegar.add_argument("--smt2", type=Path)

    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.mode == "random":
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
            parse_pattern(args.pattern),
            args.add,
            args.max_iterations,
            args.time_limit,
            args.smt2,
        )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
