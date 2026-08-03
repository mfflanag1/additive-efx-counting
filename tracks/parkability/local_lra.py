#!/usr/bin/env python3
"""Exact LRA CEGAR inside a normalized neighborhood of a near-counterexample."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

try:
    from . import core, independent
    from .lra_master import ParkabilityLRAMaster
    from .run_lra_cegar import (
        append_jsonl,
        atomic_json,
        atomic_write,
        canonical_sha256,
        has_universal_min,
        load_pool,
        select_diverse_triples,
    )
except ImportError:
    import core
    import independent
    from lra_master import ParkabilityLRAMaster
    from run_lra_cegar import (
        append_jsonl,
        atomic_json,
        atomic_write,
        canonical_sha256,
        has_universal_min,
        load_pool,
        select_diverse_triples,
    )


SCHEMA = "parkability-local-lra-result-v1"


def load_center(path: Path) -> tuple[tuple[int, ...], ...]:
    raw = json.loads(path.read_text())
    values = raw.get("values")
    if values is None and isinstance(raw.get("instance"), dict):
        values = raw["instance"].get("values")
    return core.validate_values(values, expected_n=4, expected_m=8, lower=1)


def run(
    *,
    center_path: Path,
    radius: Fraction,
    add_per_iteration: int,
    symmetry: str,
    minimum_cover: tuple[int, ...] | None,
    minimum_pattern: tuple[int, ...] | None,
    bottom_set: tuple[int, ...] | None,
    seed_pool_path: Path | None,
    time_limit_s: float,
    max_iterations: int,
    trace_path: Path,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if (
        radius <= 0
        or add_per_iteration < 1
        or time_limit_s < 0
        or max_iterations < 1
    ):
        raise ValueError("positive radius, add count, and iteration limit are required")
    paths = [trace_path.resolve(), result_path.resolve(), smt2_path.resolve()]
    if len(paths) != len(set(paths)) or any(path.exists() for path in paths):
        raise ValueError("trace, result, and SMT2 paths must be distinct and new")
    center = load_center(center_path)
    if has_universal_min(center):
        raise ValueError("center must lie in the no-universal-minimum case")
    coverage_radius = max(
        max(Fraction(value, sum(row)), 1 - Fraction(value, sum(row)))
        for row in center
        for value in row
    )
    covers_entire_simplex = radius >= coverage_radius

    master = ParkabilityLRAMaster(
        4,
        8,
        exclude_universal_min=True,
        symmetry=symmetry,
    )
    master.add_normalized_box(center, radius)
    if minimum_cover is not None:
        master.add_minimum_cover(minimum_cover)
    if minimum_pattern is not None:
        master.add_minimum_pattern(minimum_pattern)
    if bottom_set is not None:
        master.add_bottom_set(bottom_set)
    pool = load_pool(seed_pool_path) if seed_pool_path is not None else []
    pool_set = set(pool)
    all_center_triples = list(core.iter_parkable_triples(center))
    center_triples = [
        triple
        for triple in all_center_triples
        if triple not in pool_set
    ]
    pool.extend(center_triples)
    pool_set = set(pool)
    for triple in pool:
        master.add_triple(triple)
    append_jsonl(
        trace_path,
        {
            "session_iteration": 0,
            "role": "center_seed",
            "candidate_values": [list(row) for row in center],
            "candidate_sha256": canonical_sha256(center),
            "parkable_triple_count": len(all_center_triples),
            "seed_pool_size": len(pool) - len(center_triples),
            "added_triples": [triple.to_dict() for triple in center_triples],
            "pool_size_after": len(pool),
        },
    )
    started = time.time()

    for iteration in range(1, max_iterations + 1):
        solve_started = time.time()
        solved = master.solve(time_limit_s=time_limit_s)
        solve_seconds = time.time() - solve_started
        if solved.status != "SAT":
            status = (
                (
                    (
                        (
                            "GLOBAL_MINIMUM_PATTERN_UNSAT_CANDIDATE"
                            if minimum_pattern is not None
                            else (
                                "GLOBAL_MINIMUM_COVER_UNSAT_CANDIDATE"
                                if minimum_cover is not None
                                else "GLOBAL_BOTTOM_SET_UNSAT_CANDIDATE"
                            )
                        )
                        if (
                            minimum_cover is not None
                            or minimum_pattern is not None
                            or bottom_set is not None
                        )
                        else "GLOBAL_NO_UNIVERSAL_MIN_UNSAT_CANDIDATE"
                    )
                    if covers_entire_simplex
                    else "LOCAL_BOX_UNSAT_CANDIDATE"
                )
                if solved.status == "UNSAT"
                else "MASTER_UNKNOWN"
            )
            break

        assert solved.values is not None
        values = core.validate_values(
            solved.values, expected_n=4, expected_m=8, lower=1
        )
        selected, total, counts = select_diverse_triples(
            values,
            add_per_iteration,
            pool_set,
        )
        record = {
            "session_iteration": iteration,
            "pool_size_before": len(pool),
            "candidate_values": [list(row) for row in values],
            "candidate_sha256": canonical_sha256(values),
            "parkable_triple_count": total,
            "parkable_triple_count_by_floater_host": counts,
            "solver_wall_seconds": round(solve_seconds, 6),
        }
        if not selected:
            base_first = independent.enumerate_base_first(values)
            completion_first = independent.enumerate_completion_first(values)
            if base_first or completion_first:
                raise AssertionError("local zero candidate failed literal enumeration")
            complete = independent.count_complete_efx0(values)
            record["independent_zero_audit"] = {
                "base_first_parkable_triples": len(base_first),
                "completion_first_parkable_triples": len(completion_first),
                "complete_efx0_count": complete,
            }
            append_jsonl(trace_path, record)
            status = "ZERO_PARKABLE_TRIPLES"
            break

        for triple in selected:
            if not independent.is_parkable_triple(
                values, triple.floater, triple.base_owner, triple.host
            ):
                raise AssertionError("literal verifier rejected a local LRA triple")
            master.add_triple(triple)
            pool.append(triple)
            pool_set.add(triple)
        record["added_triples"] = [triple.to_dict() for triple in selected]
        record["pool_size_after"] = len(pool)
        append_jsonl(trace_path, record)
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"candidate_triples={total} solve={solve_seconds:.3f}s",
            flush=True,
        )
    else:
        status = "ITERATION_LIMIT"
        solved = None
        values = None
        complete = None

    atomic_write(smt2_path, master.to_smt2())
    result = {
        "schema": SCHEMA,
        "status": status,
        "center_path": str(center_path.resolve()),
        "center_sha256": hashlib.sha256(center_path.read_bytes()).hexdigest(),
        "center_values_sha256": canonical_sha256(center),
        "seed_pool_path": (
            str(seed_pool_path.resolve()) if seed_pool_path is not None else None
        ),
        "seed_pool_sha256": (
            hashlib.sha256(seed_pool_path.read_bytes()).hexdigest()
            if seed_pool_path is not None
            else None
        ),
        "normalized_linf_radius": str(radius),
        "radius_covering_entire_positive_simplex": str(coverage_radius),
        "box_covers_entire_positive_simplex": covers_entire_simplex,
        "case_cut": "no_universal_minimum_good",
        "symmetry": symmetry,
        "minimum_cover_goods": (
            list(minimum_cover) if minimum_cover is not None else None
        ),
        "minimum_pattern": (
            list(minimum_pattern) if minimum_pattern is not None else None
        ),
        "bottom_set_goods": list(bottom_set) if bottom_set is not None else None,
        "iterations": iteration,
        "pool_size": len(pool),
        "elapsed_seconds": round(time.time() - started, 6),
        "trace_path": str(trace_path.resolve()),
        "trace_sha256": hashlib.sha256(trace_path.read_bytes()).hexdigest(),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
        "solver_status": (
            solved.raw_status if solved is not None else "iteration_limit"
        ),
        "reason_unknown": (
            solved.reason_unknown if solved is not None else None
        ),
    }
    if status == "ZERO_PARKABLE_TRIPLES":
        result["values"] = [list(row) for row in values]
        result["values_sha256"] = canonical_sha256(values)
        result["complete_efx0_count"] = complete
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=Path, required=True)
    parser.add_argument("--radius", type=Fraction, required=True)
    parser.add_argument("--add", type=int, default=512)
    parser.add_argument("--symmetry", choices=("none", "double_lex"), default="none")
    minimum_group = parser.add_mutually_exclusive_group()
    minimum_group.add_argument("--minimum-cover", type=int, nargs=2)
    minimum_group.add_argument("--minimum-pattern", type=int, nargs=4)
    parser.add_argument("--bottom-set", type=int, nargs="+")
    parser.add_argument("--seed-pool", type=Path)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        center_path=args.center,
        radius=args.radius,
        add_per_iteration=args.add,
        symmetry=args.symmetry,
        minimum_cover=(
            tuple(args.minimum_cover) if args.minimum_cover is not None else None
        ),
        minimum_pattern=(
            tuple(args.minimum_pattern)
            if args.minimum_pattern is not None
            else None
        ),
        bottom_set=tuple(args.bottom_set) if args.bottom_set is not None else None,
        seed_pool_path=args.seed_pool,
        time_limit_s=args.time_limit,
        max_iterations=args.max_iterations,
        trace_path=args.trace,
        result_path=args.result,
        smt2_path=args.smt2,
    )


if __name__ == "__main__":
    main()
