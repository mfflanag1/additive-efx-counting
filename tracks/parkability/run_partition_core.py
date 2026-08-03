#!/usr/bin/env python3
"""Extract and replay an assumption core of partition obstructions."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from . import core
    from .lra_master import ParkabilityLRAMaster
    from .run_lra_cegar import atomic_json, atomic_write
except ImportError:
    import core
    from lra_master import ParkabilityLRAMaster
    from run_lra_cegar import atomic_json, atomic_write


SCHEMA = "partition-lra-core-result-v1"
N = 4
M = 8


def partition_shape(partition: tuple[tuple[int, ...], ...]) -> str:
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


def make_master(
    favorite_pattern: tuple[int, ...],
    *,
    pattern_stabilizer: bool,
) -> ParkabilityLRAMaster:
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
    )
    master.add_strict_favorite_pattern(favorite_pattern)
    if pattern_stabilizer:
        master.add_favorite_pattern_stabilizer(favorite_pattern)
    return master


def run(
    *,
    favorite_pattern: tuple[int, ...],
    pattern_stabilizer: bool,
    time_limit_s: float,
    input_core_path: Path | None,
    result_path: Path,
    smt2_path: Path,
) -> dict:
    if (
        len(favorite_pattern) != N
        or any(not 0 <= good < M for good in favorite_pattern)
        or time_limit_s < 0
        or result_path.exists()
        or smt2_path.exists()
        or result_path.resolve() == smt2_path.resolve()
    ):
        raise ValueError("invalid pattern, timeout, or output paths")
    started = time.time()
    if input_core_path is None:
        partitions = list(core.iter_unlabeled_nonempty_partitions(N, M))
    else:
        source = json.loads(input_core_path.read_text())
        if (
            source.get("schema") != SCHEMA
            or source.get("status") != "CORE_UNSAT_CANDIDATE"
            or source.get("favorite_pattern") != list(favorite_pattern)
            or source.get("favorite_pattern_stabilizer") != pattern_stabilizer
        ):
            raise ValueError("input core metadata does not match this run")
        partitions = [
            tuple(tuple(bundle) for bundle in partition)
            for partition in source["core_partitions"]
        ]
    master = make_master(
        favorite_pattern,
        pattern_stabilizer=pattern_stabilizer,
    )
    activations = []
    for index, partition in enumerate(partitions):
        activation = z3.Bool(f"enable_partition_{index}")
        master.add_partition_obstruction(
            partition,
            activation=activation,
        )
        activations.append(activation)
    build_seconds = time.time() - started
    master.solver.set(timeout=round(time_limit_s * 1000), unsat_core=True)
    solve_started = time.time()
    status = master.solver.check(*activations)
    solve_seconds = time.time() - solve_started
    if status != z3.unsat:
        result = {
            "schema": SCHEMA,
            "status": "CORE_UNKNOWN" if status == z3.unknown else "CORE_SAT",
            "solver_status": str(status),
            "reason_unknown": (
                master.solver.reason_unknown() if status == z3.unknown else None
            ),
            "n": N,
            "m": M,
            "favorite_pattern": list(favorite_pattern),
            "favorite_pattern_stabilizer": pattern_stabilizer,
            "partition_count": len(partitions),
            "input_core_path": (
                str(input_core_path.resolve())
                if input_core_path is not None
                else None
            ),
            "formula_build_seconds": round(build_seconds, 6),
            "assumption_solve_seconds": round(solve_seconds, 6),
            "elapsed_seconds": round(time.time() - started, 6),
            "environment": {
                "python": platform.python_version(),
                "z3": z3.get_version_string(),
            },
        }
        atomic_json(result_path, result)
        print(json.dumps(result, indent=2), flush=True)
        return result

    core_names = {str(item) for item in master.solver.unsat_core()}
    core_indices = [
        index
        for index, activation in enumerate(activations)
        if str(activation) in core_names
    ]
    if not core_indices:
        raise AssertionError("UNSAT assumption solve returned an empty core")
    core_partitions = [partitions[index] for index in core_indices]
    replay = make_master(
        favorite_pattern,
        pattern_stabilizer=pattern_stabilizer,
    )
    for partition in core_partitions:
        replay.add_partition_obstruction(partition)
    replay_started = time.time()
    replay_result = replay.solve(time_limit_s=time_limit_s)
    replay_seconds = time.time() - replay_started
    atomic_write(smt2_path, replay.to_smt2())
    shape_counts = Counter(map(partition_shape, core_partitions))
    result = {
        "schema": SCHEMA,
        "status": (
            "CORE_UNSAT_CANDIDATE"
            if replay_result.status == "UNSAT"
            else "CORE_REPLAY_" + replay_result.status
        ),
        "solver_status": replay_result.raw_status,
        "reason_unknown": replay_result.reason_unknown,
        "meaning": "exact QF_LRA assumption core; independent proof required",
        "n": N,
        "m": M,
        "favorite_pattern": list(favorite_pattern),
        "favorite_pattern_stabilizer": pattern_stabilizer,
        "partition_count": len(partitions),
        "input_core_path": (
            str(input_core_path.resolve())
            if input_core_path is not None
            else None
        ),
        "core_partition_count": len(core_partitions),
        "core_partition_count_by_shape": dict(sorted(shape_counts.items())),
        "core_partition_indices": core_indices,
        "core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in core_partitions
        ],
        "formula_build_seconds": round(build_seconds, 6),
        "assumption_solve_seconds": round(solve_seconds, 6),
        "core_replay_seconds": round(replay_seconds, 6),
        "elapsed_seconds": round(time.time() - started, 6),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--favorite-pattern", required=True)
    parser.add_argument("--favorite-pattern-stabilizer", action="store_true")
    parser.add_argument("--time-limit", type=float, default=3600)
    parser.add_argument("--input-core", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        favorite_pattern=tuple(map(int, args.favorite_pattern.split(","))),
        pattern_stabilizer=args.favorite_pattern_stabilizer,
        time_limit_s=args.time_limit,
        input_core_path=args.input_core,
        result_path=args.result,
        smt2_path=args.smt2,
    )


if __name__ == "__main__":
    main()
