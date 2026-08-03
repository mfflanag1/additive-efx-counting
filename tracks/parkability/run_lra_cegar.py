#!/usr/bin/env python3
"""Run exact LRA CEGAR for parkable deletion over all positive valuations."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import tempfile
import time
from pathlib import Path

import z3

try:
    from . import core, independent
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    import independent
    from lra_master import ParkabilityLRAMaster


POOL_SCHEMA = "parkable-deletion-lra-pool-v1"
RESULT_SCHEMA = "parkable-deletion-lra-result-v1"
PROPERTY = "zero_parkable_deletion_triples"
N = 4
M = 8


def atomic_write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(contents)
        temporary = Path(handle.name)
    temporary.replace(path)


def atomic_json(path: Path, value: dict) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def append_jsonl(path: Path | None, value: dict) -> None:
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as handle:
            handle.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def canonical_sha256(value: object) -> str:
    encoded = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def has_universal_min(values: tuple[tuple[int, ...], ...]) -> bool:
    return any(
        all(values[observer][good] == min(values[observer]) for observer in range(N))
        for good in range(M)
    )


def pool_document(triples: list[core.Triple]) -> dict:
    return {
        "schema": POOL_SCHEMA,
        "property": PROPERTY,
        "n": N,
        "m": M,
        "domain": "strictly_positive_reals_normalized_per_row",
        "case_cut": "no_universal_minimum_good",
        "case_cut_basis": (
            "the universal-minimum case is parkable by seven-good EFX existence, "
            "EFX-preserving envy-cycle elimination, and parking at a source"
        ),
        "triples": [triple.to_dict() for triple in triples],
    }


def load_pool(path: Path) -> list[core.Triple]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    expected = pool_document([])
    records = raw.pop("triples", None)
    if raw != {key: value for key, value in expected.items() if key != "triples"}:
        raise ValueError("LRA pool metadata differs from the exact schema")
    if not isinstance(records, list):
        raise ValueError("pool triples must be a JSON list")
    triples = [core.validate_triple(record, N, M) for record in records]
    if len(triples) != len(set(triples)):
        raise ValueError("pool contains duplicate triples")
    return triples


def select_diverse_triples(
    values: tuple[tuple[int, ...], ...],
    limit: int,
    forbidden: set[core.Triple],
) -> tuple[list[core.Triple], int, list[list[int]]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    quota = max(1, math.ceil(limit / (N * M)))
    buckets: dict[tuple[int, int], list[core.Triple]] = {}
    overflow: list[core.Triple] = []
    counts = [[0] * N for _ in range(M)]
    total = 0
    for triple in core.iter_parkable_triples(values):
        if triple in forbidden:
            raise AssertionError("LRA candidate satisfies an already pooled triple")
        total += 1
        counts[triple.floater][triple.host] += 1
        bucket = buckets.setdefault((triple.floater, triple.host), [])
        if len(bucket) < quota:
            bucket.append(triple)
        elif len(overflow) < limit:
            overflow.append(triple)

    selected = [
        triple
        for key in sorted(buckets)
        for triple in buckets[key]
    ][:limit]
    if len(selected) < limit:
        selected.extend(overflow[: limit - len(selected)])
    return selected, total, counts


def terminal_result(
    *,
    status: str,
    started: float,
    iteration: int,
    pool_path: Path,
    pool: list[core.Triple],
    trace_path: Path | None,
    smt2_path: Path,
    extra: dict,
) -> dict:
    return {
        "schema": RESULT_SCHEMA,
        "property": PROPERTY,
        "status": status,
        "n": N,
        "m": M,
        "domain": "strictly_positive_reals_normalized_per_row",
        "case_cut": "no_universal_minimum_good",
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
    include_one_nonsingleton: bool,
    pool_path: Path,
    trace_path: Path | None,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if add_per_iteration < 1:
        raise ValueError("add_per_iteration must be positive")
    if time_limit_s < 0 or max_iterations < 0:
        raise ValueError("time limit and iteration limit cannot be negative")
    paths = [pool_path.resolve(), result_path.resolve(), smt2_path.resolve()]
    if trace_path is not None:
        paths.append(trace_path.resolve())
    if len(paths) != len(set(paths)):
        raise ValueError("pool, trace, result, and SMT2 paths must be distinct")
    if trace_path is not None and trace_path.exists():
        raise ValueError("trace path must be new for each resumed session")

    pool = load_pool(pool_path)
    pool_set = set(pool)
    if include_one_nonsingleton:
        for triple in core.iter_one_nonsingleton_triples(N, M):
            if triple not in pool_set:
                pool.append(triple)
                pool_set.add(triple)
    if not pool_path.exists() or include_one_nonsingleton:
        atomic_json(pool_path, pool_document(pool))
    master = ParkabilityLRAMaster(N, M, exclude_universal_min=True)
    for triple in pool:
        if not master.add_triple(triple):
            raise AssertionError("validated pool unexpectedly duplicated a triple")
    started = time.time()
    iteration = 0

    while True:
        iteration += 1
        solve_started = time.time()
        solved = master.solve(time_limit_s=time_limit_s)
        solve_seconds = time.time() - solve_started
        if solved.status != "SAT":
            atomic_write(smt2_path, master.to_smt2())
            status = "UNSAT_CANDIDATE" if solved.status == "UNSAT" else "MASTER_UNKNOWN"
            result = terminal_result(
                status=status,
                started=started,
                iteration=iteration,
                pool_path=pool_path,
                pool=pool,
                trace_path=trace_path,
                smt2_path=smt2_path,
                extra={
                    "one_nonsingleton_static_seed": include_one_nonsingleton,
                    "solver_status": solved.raw_status,
                    "reason_unknown": solved.reason_unknown,
                    "meaning": (
                        "exact-LRA closure of the no-universal-minimum case; "
                        "requires independent proof checking before theorem promotion"
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
            raise AssertionError("LRA case cut decoded to a universal-minimum matrix")
        selected, total, counts = select_diverse_triples(
            values, add_per_iteration, pool_set
        )
        record = {
            "session_iteration": iteration,
            "pool_size_before": len(pool),
            "candidate_sha256": canonical_sha256(values),
            "candidate_values": [list(row) for row in values],
            "solver_wall_seconds": round(solve_seconds, 6),
            "parkable_triple_count": total,
            "parkable_triple_count_by_floater_host": counts,
        }

        if selected:
            for triple in selected:
                if not core.triple_is_parkable(values, triple):
                    raise AssertionError("exact enumerator emitted an invalid triple")
                if not independent.is_parkable_triple(
                    values, triple.floater, triple.base_owner, triple.host
                ):
                    raise AssertionError("literal verifier rejected an LRA triple")
                if not master.add_triple(triple):
                    raise AssertionError("new LRA triple was unexpectedly duplicated")
                pool.append(triple)
                pool_set.add(triple)
            atomic_json(pool_path, pool_document(pool))
            record["added_triples"] = [triple.to_dict() for triple in selected]
            record["pool_size_after"] = len(pool)
            record["pool_sha256_after"] = hashlib.sha256(
                pool_path.read_bytes()
            ).hexdigest()
            append_jsonl(trace_path, record)
            print(
                f"iteration={iteration} pool={len(pool)} added={len(selected)} "
                f"candidate_triples={total} solve={solve_seconds:.3f}s",
                flush=True,
            )
            if max_iterations and iteration >= max_iterations:
                atomic_write(smt2_path, master.to_smt2())
                result = terminal_result(
                    status="ITERATION_LIMIT",
                    started=started,
                    iteration=iteration,
                    pool_path=pool_path,
                    pool=pool,
                    trace_path=trace_path,
                    smt2_path=smt2_path,
                    extra={
                        "one_nonsingleton_static_seed": (
                            include_one_nonsingleton
                        ),
                        "meaning": "inconclusive resumable exact-LRA checkpoint",
                    },
                )
                atomic_json(result_path, result)
                return result
            continue

        literal_base = independent.enumerate_base_first(values)
        literal_completion = independent.enumerate_completion_first(values)
        if literal_base or literal_completion:
            raise AssertionError("independent enumerator found a missed parking triple")
        complete_primary = core.count_efx0_allocations(values)
        complete_independent = independent.count_complete_efx0(values)
        if complete_primary != complete_independent:
            raise AssertionError("complete EFX0 counts disagree")
        record["independent_zero_audit"] = {
            "base_first_parkable_triples": len(literal_base),
            "completion_first_parkable_triples": len(literal_completion),
            "efx0_base_count_by_floater": list(
                independent.count_removed_good_efx0_bases(values)
            ),
            "complete_efx0_count": complete_independent,
        }
        append_jsonl(trace_path, record)
        atomic_write(smt2_path, master.to_smt2())
        result = terminal_result(
            status="ZERO_PARKABLE_TRIPLES",
            started=started,
            iteration=iteration,
            pool_path=pool_path,
            pool=pool,
            trace_path=trace_path,
            smt2_path=smt2_path,
            extra={
                "one_nonsingleton_static_seed": include_one_nonsingleton,
                "values": [list(row) for row in values],
                "values_sha256": canonical_sha256(values),
                "independent_audit": record["independent_zero_audit"],
                "meaning": (
                    "exact positive-rational counterexample to parkable deletion; "
                    "complete EFX0 existence is recorded separately"
                ),
            },
        )
        atomic_json(result_path, result)
        print(
            f"ZERO_PARKABLE_TRIPLES iteration={iteration} "
            f"complete_efx0={complete_independent}",
            flush=True,
        )
        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", type=int, default=128)
    parser.add_argument(
        "--time-limit",
        type=float,
        default=0,
        help="seconds per incremental LRA check; zero means no limit",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="zero means no iteration limit",
    )
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument(
        "--include-one-nonsingleton",
        action="store_true",
        help="preload all 6,720 reverse certificates of shape 5111",
    )
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        add_per_iteration=args.add,
        time_limit_s=args.time_limit,
        max_iterations=args.max_iterations,
        include_one_nonsingleton=args.include_one_nonsingleton,
        pool_path=args.pool,
        trace_path=args.trace,
        result_path=args.result,
        smt2_path=args.smt2,
    )


if __name__ == "__main__":
    main()
