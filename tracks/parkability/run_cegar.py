#!/usr/bin/env python3
"""Run the first sound bounded CEGAR for zero parkable deletion triples."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import tempfile
import time
from pathlib import Path

import ortools

try:
    from . import core, independent
    from .master import ParkabilityMaster
except ImportError:
    import core
    import independent
    from master import ParkabilityMaster


POOL_SCHEMA = "parkable-deletion-pool-v1"
RESULT_SCHEMA = "parkable-deletion-cegar-result-v1"
PROPERTY = "zero_parkable_deletion_triples"
N = 4
M = 8
LOWER = 1


def atomic_write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def append_jsonl(path: Path | None, value: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def pool_document(triples: list[core.Triple], upper: int, symmetry: str) -> dict:
    return {
        "schema": POOL_SCHEMA,
        "property": PROPERTY,
        "n": N,
        "m": M,
        "lower": LOWER,
        "upper": upper,
        "symmetry": symmetry,
        "triples": [triple.to_dict() for triple in triples],
    }


def load_pool(path: Path | None, upper: int, symmetry: str) -> list[core.Triple]:
    if path is None or not path.exists():
        return []
    raw = json.loads(path.read_text())
    expected = {
        "schema": POOL_SCHEMA,
        "property": PROPERTY,
        "n": N,
        "m": M,
        "lower": LOWER,
        "upper": upper,
        "symmetry": symmetry,
    }
    expected_fields = set(expected) | {"triples"}
    if set(raw) != expected_fields:
        raise ValueError(
            "pool fields differ from the exact pool schema: "
            f"{sorted(set(raw) ^ expected_fields)}"
        )
    for field, value in expected.items():
        if raw.get(field) != value:
            raise ValueError(
                f"pool field {field!r} is {raw.get(field)!r}, expected {value!r}"
            )
    records = raw.get("triples")
    if not isinstance(records, list):
        raise ValueError("pool triples must be a JSON list")
    triples = [core.validate_triple(record, N, M) for record in records]
    if len(triples) != len(set(triples)):
        raise ValueError("pool contains duplicate triples")
    return triples


def canonical_sha256(value: object) -> str:
    encoded = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def write_terminal(
    path: Path,
    *,
    pool_path: Path,
    trace_path: Path | None,
    run_config: dict,
    status: str,
    upper: int,
    symmetry: str,
    iterations: int,
    pool: list[core.Triple],
    elapsed: float,
    extra: dict,
) -> dict:
    pool_bytes = pool_path.read_bytes()
    if json.loads(pool_bytes) != pool_document(pool, upper, symmetry):
        raise AssertionError("checkpointed pool does not match in-memory pool")
    trace_bytes = (
        trace_path.read_bytes()
        if trace_path is not None and trace_path.exists()
        else None
    )
    result = {
        "schema": RESULT_SCHEMA,
        "property": PROPERTY,
        "status": status,
        "n": N,
        "m": M,
        "lower": LOWER,
        "upper": upper,
        "symmetry": symmetry,
        "iterations": iterations,
        "pool_size": len(pool),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": hashlib.sha256(pool_bytes).hexdigest(),
        "trace_path": (str(trace_path.resolve()) if trace_path is not None else None),
        "trace_sha256": (
            hashlib.sha256(trace_bytes).hexdigest() if trace_bytes is not None else None
        ),
        "trace_role": "non_authoritative_current_session_telemetry",
        "iteration_scope": "current_session",
        "run_config": run_config,
        "elapsed_seconds": round(elapsed, 6),
        **extra,
    }
    atomic_write_json(path, result)
    return result


def run(
    *,
    upper: int,
    add_per_iteration: int,
    time_limit_s: float,
    workers: int,
    random_seed: int,
    symmetry: str,
    max_iterations: int,
    pool_path: Path,
    result_path: Path,
    trace_path: Path | None,
) -> dict:
    if upper < LOWER:
        raise ValueError("upper must be at least one")
    if add_per_iteration < 1:
        raise ValueError("add_per_iteration must be positive")
    if max_iterations < 0:
        raise ValueError("max_iterations cannot be negative")
    artifact_paths = [pool_path.resolve(), result_path.resolve()]
    if trace_path is not None:
        artifact_paths.append(trace_path.resolve())
    if len(artifact_paths) != len(set(artifact_paths)):
        raise ValueError("pool, result, and trace paths must be distinct")
    if trace_path is not None and trace_path.exists():
        raise ValueError("trace path must be new for each resumed session")

    pool = load_pool(pool_path, upper, symmetry)
    if not pool_path.exists():
        atomic_write_json(pool_path, pool_document(pool, upper, symmetry))
    started = time.time()
    run_config = {
        "add_per_iteration": add_per_iteration,
        "time_limit_seconds_per_master": time_limit_s,
        "workers": workers,
        "random_seed": random_seed,
        "max_iterations": max_iterations,
        "starting_pool_size": len(pool),
        "python_version": platform.python_version(),
        "ortools_version": ortools.__version__,
    }
    iteration = 0
    while True:
        iteration += 1
        master = ParkabilityMaster(N, M, LOWER, upper, symmetry=symmetry)
        for triple in pool:
            if not master.add_triple(triple):
                raise AssertionError("validated pool unexpectedly duplicated a triple")
        solved = master.solve(
            time_limit_s=time_limit_s,
            workers=workers,
            random_seed=random_seed,
        )
        elapsed = time.time() - started

        if solved.status == "UNSAT":
            result = write_terminal(
                result_path,
                pool_path=pool_path,
                trace_path=trace_path,
                run_config=run_config,
                status="UNSAT_CANDIDATE",
                upper=upper,
                symmetry=symmetry,
                iterations=iteration,
                pool=pool,
                elapsed=elapsed,
                extra={
                    "solver_status": solved.raw_status,
                    "solver": {
                        "wall_time_seconds": solved.wall_time_seconds,
                        "conflicts": solved.conflicts,
                        "branches": solved.branches,
                    },
                    "meaning": (
                        "bounded closure solver evidence; not a certified "
                        "theorem until the terminal master is independently "
                        "rebuilt and proof-checked"
                    ),
                },
            )
            print(f"UNSAT_CANDIDATE K={upper} iteration={iteration} pool={len(pool)}")
            return result

        if solved.status != "SAT":
            result = write_terminal(
                result_path,
                pool_path=pool_path,
                trace_path=trace_path,
                run_config=run_config,
                status="MASTER_UNKNOWN",
                upper=upper,
                symmetry=symmetry,
                iterations=iteration,
                pool=pool,
                elapsed=elapsed,
                extra={
                    "solver_status": solved.raw_status,
                    "solver": {
                        "wall_time_seconds": solved.wall_time_seconds,
                        "conflicts": solved.conflicts,
                        "branches": solved.branches,
                    },
                    "meaning": "inconclusive master solve",
                },
            )
            print(
                f"MASTER_UNKNOWN K={upper} iteration={iteration} "
                f"pool={len(pool)} raw={solved.raw_status}"
            )
            return result

        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=LOWER,
            upper=upper,
        )
        scan = core.landscape(
            values,
            sample_limit=add_per_iteration,
            stop_after=add_per_iteration,
            include_complete_count=False,
        )
        found = [core.validate_triple(record, N, M) for record in scan["triple_sample"]]
        for triple in found:
            if not core.triple_is_parkable(values, triple):
                raise AssertionError("core scan emitted an invalid triple")
            if not independent.is_parkable_triple(
                values,
                triple.floater,
                triple.base_owner,
                triple.host,
            ):
                raise AssertionError("independent verifier rejected a pooled triple")
            if triple in pool:
                raise AssertionError(
                    "master returned a matrix satisfying a pooled triple"
                )

        trace_record = {
            "session_iteration": iteration,
            "pool_size_before": len(pool),
            "candidate_sha256": canonical_sha256(values),
            "candidate_values": [list(row) for row in values],
            "solver": {
                "status": solved.raw_status,
                "wall_time_seconds": solved.wall_time_seconds,
                "conflicts": solved.conflicts,
                "branches": solved.branches,
            },
            "slave": scan,
        }

        if found:
            pool.extend(found)
            trace_record["added_triples"] = [triple.to_dict() for triple in found]
            atomic_write_json(pool_path, pool_document(pool, upper, symmetry))
            trace_record["pool_size_after"] = len(pool)
            trace_record["pool_sha256_after"] = hashlib.sha256(
                pool_path.read_bytes()
            ).hexdigest()
            append_jsonl(trace_path, trace_record)
            print(
                f"iteration={iteration} pool={len(pool)} "
                f"added={len(found)} candidate={trace_record['candidate_sha256'][:12]}"
            )
            if max_iterations and iteration >= max_iterations:
                return write_terminal(
                    result_path,
                    pool_path=pool_path,
                    trace_path=trace_path,
                    run_config=run_config,
                    status="ITERATION_LIMIT",
                    upper=upper,
                    symmetry=symmetry,
                    iterations=iteration,
                    pool=pool,
                    elapsed=time.time() - started,
                    extra={"meaning": "inconclusive checkpoint"},
                )
            continue

        if not scan["exhaustive"]:
            raise AssertionError("zero-triple scan did not exhaust the universe")
        literal_base_first = independent.enumerate_base_first(values)
        literal_completion_first = independent.enumerate_completion_first(values)
        if literal_base_first or literal_completion_first:
            raise AssertionError("independent verifier found a missed parking triple")
        literal_base_counts = independent.count_removed_good_efx0_bases(values)
        if list(literal_base_counts) != scan["efx0_base_count_by_floater"]:
            raise AssertionError("EFX0 deletion-base counts disagree")
        complete_primary = core.count_efx0_allocations(values)
        complete_independent = independent.count_complete_efx0(values)
        if complete_primary != complete_independent:
            raise AssertionError("complete EFX0 counts disagree")
        scan["complete_efx0_count"] = complete_primary
        trace_record["independent_zero_audit"] = {
            "base_first_parkable_triples": len(literal_base_first),
            "completion_first_parkable_triples": len(literal_completion_first),
            "efx0_base_count_by_floater": list(literal_base_counts),
            "complete_efx0_count": complete_independent,
        }
        trace_record["pool_size_after"] = len(pool)
        trace_record["pool_sha256_after"] = hashlib.sha256(
            pool_path.read_bytes()
        ).hexdigest()
        append_jsonl(trace_path, trace_record)
        result = write_terminal(
            result_path,
            pool_path=pool_path,
            trace_path=trace_path,
            run_config=run_config,
            status="ZERO_PARKABLE_TRIPLES",
            upper=upper,
            symmetry=symmetry,
            iterations=iteration,
            pool=pool,
            elapsed=time.time() - started,
            extra={
                "values": [list(row) for row in values],
                "values_sha256": canonical_sha256(values),
                "landscape": scan,
                "independent_audit": trace_record["independent_zero_audit"],
                "meaning": (
                    "exact counterexample to parkable deletion; the same "
                    "matrix has complete EFX0 allocations"
                    if complete_independent > 0
                    else "exact counterexample to parkable deletion and to "
                    "additive EFX0 existence"
                ),
            },
        )
        print(
            f"ZERO_PARKABLE_TRIPLES K={upper} iteration={iteration} "
            f"complete_efx0={complete_independent}"
        )
        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--K", type=int, required=True)
    parser.add_argument("--add", type=int, default=16)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--symmetry", choices=("none", "double_lex"), default="none")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="stop after this many SAT iterations; zero means no limit",
    )
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    run(
        upper=args.K,
        add_per_iteration=args.add,
        time_limit_s=args.time_limit,
        workers=args.workers,
        random_seed=args.random_seed,
        symmetry=args.symmetry,
        max_iterations=args.max_iterations,
        pool_path=args.pool,
        result_path=args.result,
        trace_path=args.trace,
    )


if __name__ == "__main__":
    main()
