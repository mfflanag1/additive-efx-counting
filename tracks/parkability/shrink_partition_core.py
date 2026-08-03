#!/usr/bin/env python3
"""Resume-safe deletion shrinking for a partition-obstruction UNSAT core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
    from .run_partition_core import partition_shape
except ImportError:
    import core
    from lra_master import ParkabilityLRAMaster
    from run_lra_cegar import atomic_json, atomic_write
    from run_partition_core import partition_shape


SCHEMA = "partition-lra-deletion-shrink-v1"
SOURCE_SCHEMA = "partition-lra-core-result-v1"
N = 4
M = 8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_partition(
    raw_partition: list[list[int]],
) -> tuple[tuple[int, ...], ...]:
    partition = tuple(
        sorted(tuple(sorted(bundle)) for bundle in raw_partition)
    )
    if (
        len(partition) != N
        or any(not bundle for bundle in partition)
        or sorted(good for bundle in partition for good in bundle)
        != list(range(M))
    ):
        raise ValueError("source contains an invalid partition")
    return partition


def load_source(path: Path) -> tuple[dict, list[tuple[tuple[int, ...], ...]]]:
    source = json.loads(path.read_text())
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status") != "CORE_UNSAT_CANDIDATE"
        or source.get("n") != N
        or source.get("m") != M
        or len(source.get("favorite_pattern", [])) != N
    ):
        raise ValueError("input is not a compatible UNSAT partition core")
    partitions = [
        canonical_partition(partition)
        for partition in source["core_partitions"]
    ]
    if (
        len(partitions) != source.get("core_partition_count")
        or len(set(partitions)) != len(partitions)
    ):
        raise ValueError("source core count or uniqueness mismatch")
    return source, partitions


def global_partition_indices(
    partitions: list[tuple[tuple[int, ...], ...]],
) -> list[int]:
    universe = {
        tuple(sorted(tuple(sorted(bundle)) for bundle in partition)): index
        for index, partition in enumerate(
            core.iter_unlabeled_nonempty_partitions(N, M)
        )
    }
    if len(universe) != 1_701:
        raise AssertionError("unexpected partition-universe size")
    try:
        return [universe[partition] for partition in partitions]
    except KeyError as error:
        raise ValueError("source partition is absent from the universe") from error


def make_master(source: dict) -> ParkabilityLRAMaster:
    favorite_pattern = tuple(source["favorite_pattern"])
    stabilizer = source.get("favorite_pattern_stabilizer")
    if type(stabilizer) is not bool:
        raise ValueError("source omits favorite-pattern stabilizer status")
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
    )
    master.add_strict_favorite_pattern(favorite_pattern)
    if stabilizer:
        master.add_favorite_pattern_stabilizer(favorite_pattern)
    return master


def parse_chunk_sizes(raw: str) -> list[int]:
    sizes = [int(item) for item in raw.split(",")]
    if not sizes or any(size < 1 for size in sizes):
        raise ValueError("chunk sizes must be positive")
    return sorted(set(sizes), reverse=True)


def structural_statistics(
    partitions: list[tuple[tuple[int, ...], ...]],
    active: list[int],
    favorite_pattern: list[int],
) -> dict:
    selected = [partitions[position] for position in active]
    favorite_goods = sorted(set(favorite_pattern))
    singleton_counts = Counter(
        bundle[0]
        for partition in selected
        for bundle in partition
        if len(bundle) == 1
    )
    cobundle_counts = Counter(
        pair
        for partition in selected
        for bundle in partition
        for pair in itertools.combinations(bundle, 2)
    )
    size_by_good = {
        str(good): dict(
            sorted(
                Counter(
                    len(bundle)
                    for partition in selected
                    for bundle in partition
                    if good in bundle
                ).items()
            )
        )
        for good in range(M)
    }
    favorite_groupings = Counter()
    favorite_goods_separate = 0
    favorite_set = set(favorite_goods)
    for partition in selected:
        groups = sorted(
            tuple(good for good in bundle if good in favorite_set)
            for bundle in partition
            if any(good in favorite_set for good in bundle)
        )
        key = "|".join(
            ",".join(map(str, group))
            for group in groups
        )
        favorite_groupings[key] += 1
        if len(groups) == len(favorite_goods):
            favorite_goods_separate += 1
    return {
        "distinct_favorite_goods": favorite_goods,
        "distinct_favorite_good_count": len(favorite_goods),
        "all_distinct_favorite_goods_separate_count": (
            favorite_goods_separate
        ),
        "favorite_good_grouping_counts": dict(
            sorted(favorite_groupings.items())
        ),
        "singleton_good_counts": {
            str(good): singleton_counts.get(good, 0)
            for good in range(M)
        },
        "bundle_size_by_good": size_by_good,
        "cobundle_pair_counts": {
            f"{left}-{right}": count
            for (left, right), count in sorted(cobundle_counts.items())
        },
    }


def checkpoint_payload(
    *,
    input_path: Path,
    input_sha256: str,
    source: dict,
    global_indices: list[int],
    active: list[int],
    checks: list[dict],
    known_unsat: bool,
    started: float,
) -> dict:
    active_partitions = [global_indices[position] for position in active]
    return {
        "schema": SCHEMA,
        "status": "ACTIVE_UNSAT_CORE" if known_unsat else "UNVERIFIED",
        "input": str(input_path.resolve()),
        "input_sha256": input_sha256,
        "n": N,
        "m": M,
        "favorite_pattern": source["favorite_pattern"],
        "favorite_pattern_stabilizer": source[
            "favorite_pattern_stabilizer"
        ],
        "source_partition_count": len(global_indices),
        "active_partition_count": len(active),
        "active_source_positions": active,
        "active_global_partition_indices": active_partitions,
        "active_count_by_shape": dict(
            sorted(
                Counter(
                    partition_shape(
                        canonical_partition(
                            source["core_partitions"][position]
                        )
                    )
                    for position in active
                ).items()
            )
        ),
        "check_count": len(checks),
        "checks": checks,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
    }


def run(
    *,
    input_path: Path,
    checkpoint_path: Path,
    result_path: Path,
    smt2_path: Path,
    chunk_sizes: list[int],
    per_check_limit_s: float,
    total_limit_s: float,
) -> dict:
    if (
        per_check_limit_s <= 0
        or total_limit_s <= 0
        or len({checkpoint_path.resolve(), result_path.resolve(), smt2_path.resolve()})
        != 3
    ):
        raise ValueError("invalid limits or colliding output paths")
    started = time.monotonic()
    source, partitions = load_source(input_path)
    input_hash = sha256(input_path)
    global_indices = global_partition_indices(partitions)
    active = list(range(len(partitions)))
    checks: list[dict] = []
    known_unsat = False
    if checkpoint_path.is_file():
        checkpoint = json.loads(checkpoint_path.read_text())
        if (
            checkpoint.get("schema") != SCHEMA
            or checkpoint.get("input_sha256") != input_hash
            or checkpoint.get("status") != "ACTIVE_UNSAT_CORE"
        ):
            raise ValueError("checkpoint does not match the input core")
        active = checkpoint["active_source_positions"]
        checks = checkpoint.get("checks", [])
        if (
            not active
            or active != sorted(set(active))
            or any(not 0 <= position < len(partitions) for position in active)
        ):
            raise ValueError("checkpoint has invalid active positions")
        known_unsat = True

    master = make_master(source)
    activations = []
    activation_positions = {}
    for position, partition in enumerate(partitions):
        activation = z3.Bool(f"shrink_partition_{global_indices[position]}")
        master.add_partition_obstruction(
            partition,
            activation=activation,
        )
        activations.append(activation)
        activation_positions[str(activation)] = position
    master.solver.set(
        timeout=round(per_check_limit_s * 1000),
        unsat_core=True,
    )

    def save_checkpoint() -> None:
        atomic_json(
            checkpoint_path,
            checkpoint_payload(
                input_path=input_path,
                input_sha256=input_hash,
                source=source,
                global_indices=global_indices,
                active=active,
                checks=checks,
                known_unsat=known_unsat,
                started=started,
            ),
        )

    def check(
        trial: list[int],
        *,
        phase: str,
        requested_removed: list[int],
    ) -> tuple[str, list[int] | None]:
        check_started = time.monotonic()
        status = master.solver.check(
            *(activations[position] for position in trial)
        )
        seconds = time.monotonic() - check_started
        core_positions = None
        if status == z3.unsat:
            names = {str(item) for item in master.solver.unsat_core()}
            core_positions = sorted(
                activation_positions[name]
                for name in names
            )
            if not set(core_positions) <= set(trial):
                raise AssertionError("solver returned an invalid assumption core")
        checks.append(
            {
                "phase": phase,
                "status": str(status),
                "active_before": len(active),
                "trial_count": len(trial),
                "requested_removed_count": len(requested_removed),
                "requested_removed_global_indices": [
                    global_indices[position]
                    for position in requested_removed
                ],
                "returned_core_count": (
                    len(core_positions)
                    if core_positions is not None
                    else None
                ),
                "seconds": round(seconds, 6),
                "reason_unknown": (
                    master.solver.reason_unknown()
                    if status == z3.unknown
                    else None
                ),
            }
        )
        return str(status), core_positions

    if not known_unsat:
        status, core_positions = check(
            active,
            phase="initial-core",
            requested_removed=[],
        )
        if status != "unsat" or core_positions is None:
            diagnostic = checkpoint_payload(
                input_path=input_path,
                input_sha256=input_hash,
                source=source,
                global_indices=global_indices,
                active=active,
                checks=checks,
                known_unsat=False,
                started=started,
            )
            diagnostic["status"] = "SOURCE_CORE_" + status.upper()
            atomic_json(result_path, diagnostic)
            raise RuntimeError(f"source core did not replay UNSAT: {status}")
        active = core_positions
        known_unsat = True
        save_checkpoint()

    deadline = started + total_limit_s
    for chunk_size in chunk_sizes:
        offset = 0
        while offset < len(active) and time.monotonic() < deadline:
            requested_removed = active[offset : offset + chunk_size]
            removed_set = set(requested_removed)
            trial = [
                position
                for position in active
                if position not in removed_set
            ]
            status, core_positions = check(
                trial,
                phase=f"delete-{chunk_size}",
                requested_removed=requested_removed,
            )
            if status == "unsat" and core_positions is not None:
                active = core_positions
                known_unsat = True
            else:
                offset += chunk_size
            save_checkpoint()

    replay = make_master(source)
    for position in active:
        replay.add_partition_obstruction(partitions[position])
    replay_started = time.monotonic()
    replay_result = replay.solve(time_limit_s=per_check_limit_s)
    replay_seconds = time.monotonic() - replay_started
    atomic_write(smt2_path, replay.to_smt2())
    active_shapes = Counter(
        partition_shape(partitions[position])
        for position in active
    )
    result = checkpoint_payload(
        input_path=input_path,
        input_sha256=input_hash,
        source=source,
        global_indices=global_indices,
        active=active,
        checks=checks,
        known_unsat=known_unsat,
        started=started,
    )
    result.update(
        {
            "status": (
                "SHRUNK_CORE_UNSAT"
                if replay_result.status == "UNSAT"
                else "SHRUNK_CORE_REPLAY_" + replay_result.status
            ),
            "active_count_by_shape": dict(sorted(active_shapes.items())),
            "active_partitions": [
                [
                    list(bundle)
                    for bundle in partitions[position]
                ]
                for position in active
            ],
            "structural_statistics": structural_statistics(
                partitions,
                active,
                source["favorite_pattern"],
            ),
            "replay_status": replay_result.raw_status,
            "replay_reason_unknown": replay_result.reason_unknown,
            "replay_seconds": round(replay_seconds, 6),
            "smt2": str(smt2_path.resolve()),
            "smt2_sha256": sha256(smt2_path),
            "time_budget_exhausted": time.monotonic() >= deadline,
        }
    )
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument(
        "--chunk-sizes",
        default="32,16,8,4,2,1",
    )
    parser.add_argument("--per-check-limit", type=float, default=900)
    parser.add_argument("--total-limit", type=float, default=7200)
    args = parser.parse_args()
    run(
        input_path=args.input,
        checkpoint_path=args.checkpoint,
        result_path=args.result,
        smt2_path=args.smt2,
        chunk_sizes=parse_chunk_sizes(args.chunk_sizes),
        per_check_limit_s=args.per_check_limit,
        total_limit_s=args.total_limit,
    )


if __name__ == "__main__":
    main()
