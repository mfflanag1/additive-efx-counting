#!/usr/bin/env python3
"""Exact real-arithmetic CEGAR over complete EFX0 allocations."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import z3

try:
    from . import core, independent
    from .lra_master import ParkabilityLRAMaster
    from .run_lra_cegar import (
        append_jsonl,
        atomic_json,
        atomic_write,
        canonical_sha256,
        has_universal_min,
        load_pool as load_triple_pool,
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
        load_pool as load_triple_pool,
    )


POOL_SCHEMA = "complete-efx-lra-pool-v1"
RESULT_SCHEMA = "complete-efx-lra-result-v1"
N = 4
M = 8


def validate_assignment(raw: Sequence[int]) -> tuple[int, ...]:
    assignment = tuple(raw)
    if len(assignment) != M or any(
        type(owner) is not int or not 0 <= owner < N for owner in assignment
    ):
        raise ValueError("every complete allocation must assign 8 goods to agents 0..3")
    return assignment


def pool_document(assignments: Sequence[Sequence[int]]) -> dict:
    return {
        "schema": POOL_SCHEMA,
        "n": N,
        "m": M,
        "domain": "strictly_positive_reals_normalized_per_row",
        "case_cut": "no_universal_minimum_good",
        "allocations": [list(validate_assignment(item)) for item in assignments],
    }


def load_pool(path: Path) -> list[tuple[int, ...]]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    expected = {
        "schema",
        "n",
        "m",
        "domain",
        "case_cut",
        "allocations",
    }
    if not isinstance(raw, dict) or set(raw) != expected:
        raise ValueError("complete-EFX pool has an unexpected schema")
    if (
        raw["schema"] != POOL_SCHEMA
        or raw["n"] != N
        or raw["m"] != M
        or raw["domain"] != "strictly_positive_reals_normalized_per_row"
        or raw["case_cut"] != "no_universal_minimum_good"
        or not isinstance(raw["allocations"], list)
    ):
        raise ValueError("complete-EFX pool metadata does not match this search")
    assignments = [validate_assignment(item) for item in raw["allocations"]]
    if len(assignments) != len(set(assignments)):
        raise ValueError("complete-EFX pool contains duplicate allocations")
    return assignments


def load_allocation_import(path: Path) -> list[tuple[int, ...]]:
    raw = json.loads(path.read_text())
    if isinstance(raw, dict):
        return load_pool(path)
    if not isinstance(raw, list):
        raise ValueError("imported allocation pool must be a list or complete pool")
    assignments = [validate_assignment(item) for item in raw]
    if len(assignments) != len(set(assignments)):
        raise ValueError("imported allocation pool contains duplicates")
    return assignments


def shape(assignment: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (sum(owner == agent for owner in assignment) for agent in range(N)),
            reverse=True,
        )
    )


def completion_of_triple(triple: core.Triple) -> tuple[int, ...]:
    return tuple(
        triple.host if good == triple.floater else owner
        for good, owner in enumerate(triple.base_owner)
    )


def has_peelable_good(values: Sequence[Sequence[int]]) -> bool:
    return any(
        value
        >= sum(row) - value - min(
            row[other] for other in range(len(row)) if other != good
        )
        for row in values
        for good, value in enumerate(row)
    )


def has_repeated_normalized_rows(values: Sequence[Sequence[int]]) -> bool:
    normalized = [
        tuple(Fraction(value, sum(row)) for value in row) for row in values
    ]
    return len(normalized) != len(set(normalized))


def has_favorite_good_matching(values: Sequence[Sequence[int]]) -> bool:
    favorite_goods = [
        tuple(good for good, value in enumerate(row) if value == max(row))
        for row in values
    ]
    return any(
        all(matching[observer] in favorite_goods[observer] for observer in range(N))
        for matching in itertools.permutations(range(M), N)
    )


def select_diverse_allocations(
    values: Sequence[Sequence[int]],
    limit: int,
    forbidden: set[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], int, dict[str, int]]:
    if limit < 1:
        raise ValueError("allocation limit must be positive")
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for assignment in core.iter_efx0_assignments(values):
        if assignment in forbidden:
            raise AssertionError("LRA candidate satisfies a pooled EFX allocation")
        buckets.setdefault(shape(assignment), []).append(assignment)
    total = sum(map(len, buckets.values()))
    counts = {
        "".join(map(str, allocation_shape)): len(assignments)
        for allocation_shape, assignments in sorted(buckets.items())
    }
    selected = []
    offsets = Counter()
    ordered_shapes = sorted(buckets)
    while len(selected) < min(limit, total):
        progressed = False
        for allocation_shape in ordered_shapes:
            offset = offsets[allocation_shape]
            bucket = buckets[allocation_shape]
            if offset < len(bucket):
                selected.append(bucket[offset])
                offsets[allocation_shape] += 1
                progressed = True
                if len(selected) == min(limit, total):
                    break
        if not progressed:
            break
    return selected, total, counts


def result_document(
    *,
    status: str,
    started: float,
    iteration: int,
    pool_path: Path,
    pool: Sequence[Sequence[int]],
    trace_path: Path | None,
    smt2_path: Path,
    imports: Sequence[dict],
    allocation_imports: Sequence[dict],
    symmetry: str,
    exclude_peelable: bool,
    require_pairwise_distinct_rows: bool,
    require_favorite_hall_deficiency: bool,
    extra: dict,
) -> dict:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "n": N,
        "m": M,
        "domain": "strictly_positive_reals_normalized_per_row",
        "case_cut": "no_universal_minimum_good",
        "exclude_peelable": exclude_peelable,
        "require_pairwise_distinct_rows": require_pairwise_distinct_rows,
        "require_favorite_hall_deficiency": require_favorite_hall_deficiency,
        "symmetry": symmetry,
        "certificate_universe": N**M,
        "iterations": iteration,
        "pool_size": len(pool),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "trace_path": str(trace_path.resolve()) if trace_path is not None else None,
        "trace_sha256": (
            hashlib.sha256(trace_path.read_bytes()).hexdigest()
            if trace_path is not None and trace_path.exists()
            else None
        ),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.time() - started, 6),
        "triple_pool_imports": list(imports),
        "allocation_pool_imports": list(allocation_imports),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
        **extra,
    }


def run(
    *,
    add_per_iteration: int,
    time_limit_s: float,
    max_iterations: int,
    symmetry: str,
    exclude_peelable: bool,
    require_pairwise_distinct_rows: bool,
    require_favorite_hall_deficiency: bool,
    triple_pool_paths: Sequence[Path],
    allocation_pool_paths: Sequence[Path],
    pool_path: Path,
    trace_path: Path | None,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if (
        add_per_iteration < 1
        or time_limit_s < 0
        or max_iterations < 0
        or symmetry not in {"none", "double_lex"}
    ):
        raise ValueError("invalid allocation count, timeout, or iteration limit")
    paths = [pool_path.resolve(), result_path.resolve(), smt2_path.resolve()]
    if trace_path is not None:
        paths.append(trace_path.resolve())
    triple_paths = [path.resolve() for path in triple_pool_paths]
    allocation_paths = [path.resolve() for path in allocation_pool_paths]
    import_paths = triple_paths + allocation_paths
    if any(path in paths for path in import_paths):
        raise ValueError("imported pools must differ from output paths")
    if len(import_paths) != len(set(import_paths)):
        raise ValueError("every imported pool path must be distinct")
    if len(paths) != len(set(paths)):
        raise ValueError("pool, trace, result, and SMT2 paths must be distinct")
    if trace_path is not None and trace_path.exists():
        raise ValueError("trace path must be new for every resumed session")

    pool = load_pool(pool_path)
    pool_set = set(pool)
    allocation_imports = []
    for allocation_pool_path in allocation_pool_paths:
        before = len(pool)
        assignments = load_allocation_import(allocation_pool_path)
        for assignment in assignments:
            if assignment not in pool_set:
                pool.append(assignment)
                pool_set.add(assignment)
        allocation_imports.append(
            {
                "path": str(allocation_pool_path.resolve()),
                "sha256": hashlib.sha256(
                    allocation_pool_path.read_bytes()
                ).hexdigest(),
                "allocation_count": len(assignments),
                "unique_allocations_added": len(pool) - before,
            }
        )
    imports = []
    for triple_pool_path in triple_pool_paths:
        before = len(pool)
        triples = load_triple_pool(triple_pool_path)
        for triple in triples:
            assignment = completion_of_triple(triple)
            if assignment not in pool_set:
                pool.append(assignment)
                pool_set.add(assignment)
        imports.append(
            {
                "path": str(triple_pool_path.resolve()),
                "sha256": hashlib.sha256(triple_pool_path.read_bytes()).hexdigest(),
                "triple_count": len(triples),
                "unique_completions_added": len(pool) - before,
            }
        )
    if not pool_path.exists() or imports or allocation_imports:
        atomic_json(pool_path, pool_document(pool))
    if imports or allocation_imports:
        append_jsonl(
            trace_path,
            {
                "session_iteration": 0,
                "role": "pool_import",
                "triple_pool_imports": imports,
                "allocation_pool_imports": allocation_imports,
                "pool_size_after": len(pool),
                "pool_sha256_after": hashlib.sha256(
                    pool_path.read_bytes()
                ).hexdigest(),
            },
        )
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=exclude_peelable,
        require_pairwise_distinct_rows=require_pairwise_distinct_rows,
        require_favorite_hall_deficiency=require_favorite_hall_deficiency,
        symmetry=symmetry,
    )
    for assignment in pool:
        if not master.add_complete_allocation(assignment):
            raise AssertionError("validated complete-EFX pool unexpectedly duplicated")

    started = time.time()
    iteration = 0
    while True:
        iteration += 1
        solve_started = time.time()
        solved = master.solve(time_limit_s=time_limit_s)
        solve_seconds = time.time() - solve_started
        if solved.status != "SAT":
            atomic_write(smt2_path, master.to_smt2())
            status = (
                "UNSAT_CANDIDATE" if solved.status == "UNSAT" else "MASTER_UNKNOWN"
            )
            result = result_document(
                status=status,
                started=started,
                iteration=iteration,
                pool_path=pool_path,
                pool=pool,
                trace_path=trace_path,
                smt2_path=smt2_path,
                imports=imports,
                allocation_imports=allocation_imports,
                symmetry=symmetry,
                exclude_peelable=exclude_peelable,
                require_pairwise_distinct_rows=require_pairwise_distinct_rows,
                require_favorite_hall_deficiency=(
                    require_favorite_hall_deficiency
                ),
                extra={
                    "solver_status": solved.raw_status,
                    "reason_unknown": solved.reason_unknown,
                    "meaning": (
                        "exact-LRA closure of complete EFX in the "
                        "no-universal-minimum case; independent proof required"
                        if solved.status == "UNSAT"
                        else "inconclusive exact-LRA master solve"
                    ),
                },
            )
            atomic_json(result_path, result)
            print(
                f"{status} iteration={iteration} pool={len(pool)} "
                f"solve={solve_seconds:.3f}s",
                flush=True,
            )
            return result

        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        if has_universal_min(values):
            raise AssertionError("complete-EFX LRA model violated the case cut")
        if exclude_peelable and has_peelable_good(values):
            raise AssertionError("complete-EFX LRA model violated the peeling cut")
        if (
            require_pairwise_distinct_rows
            and has_repeated_normalized_rows(values)
        ):
            raise AssertionError("complete-EFX LRA model violated the row-type cut")
        if (
            require_favorite_hall_deficiency
            and has_favorite_good_matching(values)
        ):
            raise AssertionError(
                "complete-EFX LRA model violated the favorite-Hall cut"
            )
        selected, total, shape_counts = select_diverse_allocations(
            values,
            add_per_iteration,
            pool_set,
        )
        record = {
            "session_iteration": iteration,
            "pool_size_before": len(pool),
            "candidate_values": [list(row) for row in values],
            "candidate_sha256": canonical_sha256(values),
            "complete_efx0_count": total,
            "complete_efx0_count_by_shape": shape_counts,
            "solver_wall_seconds": round(solve_seconds, 6),
        }
        if not selected:
            literal_count = independent.count_complete_efx0(values)
            base_triples = independent.enumerate_base_first(values)
            completion_triples = independent.enumerate_completion_first(values)
            if literal_count or base_triples or completion_triples:
                raise AssertionError("zero-EFX candidate failed independent audit")
            record["independent_zero_audit"] = {
                "complete_efx0_count": literal_count,
                "base_first_parkable_triples": len(base_triples),
                "completion_first_parkable_triples": len(completion_triples),
            }
            append_jsonl(trace_path, record)
            atomic_write(smt2_path, master.to_smt2())
            result = result_document(
                status="ZERO_COMPLETE_EFX0",
                started=started,
                iteration=iteration,
                pool_path=pool_path,
                pool=pool,
                trace_path=trace_path,
                smt2_path=smt2_path,
                imports=imports,
                allocation_imports=allocation_imports,
                symmetry=symmetry,
                exclude_peelable=exclude_peelable,
                require_pairwise_distinct_rows=require_pairwise_distinct_rows,
                require_favorite_hall_deficiency=(
                    require_favorite_hall_deficiency
                ),
                extra={
                    "values": [list(row) for row in values],
                    "values_sha256": canonical_sha256(values),
                    "independent_audit": record["independent_zero_audit"],
                    "meaning": (
                        "positive-rational additive-EFX counterexample, also "
                        "zero-parkability by threshold-cycle equivalence"
                    ),
                },
            )
            atomic_json(result_path, result)
            print(f"ZERO_COMPLETE_EFX0 iteration={iteration}", flush=True)
            return result

        for assignment in selected:
            if not independent.is_complete_efx0(values, assignment):
                raise AssertionError("literal verifier rejected an EFX allocation")
            if not master.add_complete_allocation(assignment):
                raise AssertionError("new complete allocation unexpectedly duplicated")
            pool.append(assignment)
            pool_set.add(assignment)
        atomic_json(pool_path, pool_document(pool))
        record["added_allocations"] = [list(item) for item in selected]
        record["pool_size_after"] = len(pool)
        record["pool_sha256_after"] = hashlib.sha256(
            pool_path.read_bytes()
        ).hexdigest()
        append_jsonl(trace_path, record)
        print(
            f"iteration={iteration} pool={len(pool)} added={len(selected)} "
            f"complete_efx0={total} solve={solve_seconds:.3f}s",
            flush=True,
        )
        if max_iterations and iteration >= max_iterations:
            atomic_write(smt2_path, master.to_smt2())
            result = result_document(
                status="ITERATION_LIMIT",
                started=started,
                iteration=iteration,
                pool_path=pool_path,
                pool=pool,
                trace_path=trace_path,
                smt2_path=smt2_path,
                imports=imports,
                allocation_imports=allocation_imports,
                symmetry=symmetry,
                exclude_peelable=exclude_peelable,
                require_pairwise_distinct_rows=require_pairwise_distinct_rows,
                require_favorite_hall_deficiency=(
                    require_favorite_hall_deficiency
                ),
                extra={"meaning": "inconclusive resumable exact-LRA checkpoint"},
            )
            atomic_json(result_path, result)
            return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", type=int, default=4096)
    parser.add_argument("--time-limit", type=float, default=900)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument(
        "--symmetry",
        choices=("none", "double_lex"),
        default="none",
    )
    parser.add_argument("--exclude-peelable", action="store_true")
    parser.add_argument("--require-pairwise-distinct-rows", action="store_true")
    parser.add_argument("--require-favorite-hall-deficiency", action="store_true")
    parser.add_argument("--triple-pool", type=Path, action="append", default=[])
    parser.add_argument(
        "--allocation-pool",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        add_per_iteration=args.add,
        time_limit_s=args.time_limit,
        max_iterations=args.max_iterations,
        symmetry=args.symmetry,
        exclude_peelable=args.exclude_peelable,
        require_pairwise_distinct_rows=args.require_pairwise_distinct_rows,
        require_favorite_hall_deficiency=args.require_favorite_hall_deficiency,
        triple_pool_paths=args.triple_pool,
        allocation_pool_paths=args.allocation_pool,
        pool_path=args.pool,
        trace_path=args.trace,
        result_path=args.result,
        smt2_path=args.smt2,
    )
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
