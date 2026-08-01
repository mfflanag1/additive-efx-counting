#!/usr/bin/env python3
"""Extract exact SAT witnesses behind deletion minimality of the 130 core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import platform
import tempfile
import time
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path

import z3

try:
    from . import core
    from .run_partition_core import partition_shape
    from .shrink_partition_core import (
        canonical_partition,
        global_partition_indices,
        make_master,
    )
except ImportError:
    import core
    from run_partition_core import partition_shape
    from shrink_partition_core import (
        canonical_partition,
        global_partition_indices,
        make_master,
    )


SCHEMA = "partition-core-deletion-witnesses-v1"
CHECKPOINT_SCHEMA = "partition-lra-deletion-shrink-v1"
N = 4
M = 8
FAVORITES = (0, 0, 1, 2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def normalize_model_rows(
    model: z3.ModelRef,
    variables: list[list[z3.ArithRef]],
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for variable_row in variables:
        fractions = []
        for variable in variable_row:
            value = model.eval(variable, model_completion=True)
            fractions.append(
                Fraction(
                    value.numerator_as_long(),
                    value.denominator_as_long(),
                )
            )
        denominator = 1
        for value in fractions:
            denominator = (
                denominator * value.denominator
                // gcd(denominator, value.denominator)
            )
        integers = [int(value * denominator) for value in fractions]
        divisor = 0
        for value in integers:
            divisor = gcd(divisor, value)
        rows.append(tuple(value // divisor for value in integers))
    return tuple(rows)


def bundle_value(row: tuple[int, ...], bundle: tuple[int, ...]) -> int:
    return sum(row[good] for good in bundle)


def feasible_graph(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> tuple[tuple[bool, ...], ...]:
    graph = []
    for observer in range(N):
        observer_edges = []
        for own_index, own_bundle in enumerate(partition):
            own = bundle_value(values[observer], own_bundle)
            feasible = True
            for target_index, target_bundle in enumerate(partition):
                if own_index == target_index:
                    continue
                for removed in target_bundle:
                    remainder = tuple(
                        good for good in target_bundle if good != removed
                    )
                    if own < bundle_value(values[observer], remainder):
                        feasible = False
            observer_edges.append(feasible)
        graph.append(tuple(observer_edges))
    return tuple(graph)


def perfect_matchings(
    graph: tuple[tuple[bool, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        matching
        for matching in itertools.permutations(range(N))
        if all(
            graph[observer][matching[observer]]
            for observer in range(N)
        )
    )


def hall_witnesses(
    graph: tuple[tuple[bool, ...], ...],
) -> tuple[tuple[int, int, int], ...]:
    witnesses = []
    for mask in range(1, 1 << N):
        agents = tuple(
            observer for observer in range(N) if mask & (1 << observer)
        )
        neighbors = {
            bundle
            for observer in agents
            for bundle in range(N)
            if graph[observer][bundle]
        }
        if len(neighbors) < len(agents):
            witnesses.append(
                (mask, len(agents) - len(neighbors), len(neighbors))
            )
    return tuple(
        sorted(
            witnesses,
            key=lambda item: (-item[1], item[0].bit_count(), item[0]),
        )
    )


def matching_slacks(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
    matching: tuple[int, ...],
) -> list[int]:
    slacks = []
    for observer in range(N):
        own = bundle_value(values[observer], partition[matching[observer]])
        for target in range(N):
            if target == observer:
                continue
            target_bundle = partition[matching[target]]
            for removed in target_bundle:
                remainder = tuple(
                    good for good in target_bundle if good != removed
                )
                slacks.append(
                    own - bundle_value(values[observer], remainder)
                )
    return slacks


def partition_summary(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> dict:
    graph = feasible_graph(values, partition)
    matchings = perfect_matchings(graph)
    hall = hall_witnesses(graph)
    return {
        "graph": [
            [bundle for bundle, edge in enumerate(row) if edge]
            for row in graph
        ],
        "matching_count": len(matchings),
        "matchings": [list(matching) for matching in matchings],
        "hall_witnesses": [
            {
                "agent_mask": mask,
                "agent_count": mask.bit_count(),
                "deficiency": deficiency,
                "neighbor_count": neighbors,
            }
            for mask, deficiency, neighbors in hall
        ],
    }


def aggregate(records: list[dict]) -> dict:
    matching_counts = Counter()
    matching_counts_by_shape = Counter()
    own_favorite_counts = Counter()
    hall_counts = Counter()
    removed_graph_degree_patterns = Counter()
    universal_feasible_agents = Counter()
    full_support_counts = []
    for record in records:
        matching_counts[record["removed_partition"]["matching_count"]] += 1
        matching_counts_by_shape[
            (
                record["shape"],
                record["removed_partition"]["matching_count"],
            )
        ] += 1
        full_support_counts.append(
            record["full_universe_supported_partition_count"]
        )
        degree_pattern = tuple(
            len(neighbors)
            for neighbors in record["removed_partition"]["graph"]
        )
        removed_graph_degree_patterns[
            ",".join(map(str, degree_pattern))
        ] += 1
        for observer, degree in enumerate(degree_pattern):
            if degree == N:
                universal_feasible_agents[str(observer)] += 1
        for matching in record["removed_partition"]["matchings"]:
            for observer, bundle_index in enumerate(matching):
                owns_favorite = FAVORITES[observer] in record["partition"][
                    bundle_index
                ]
                own_favorite_counts[f"{observer}:{owns_favorite}"] += 1
        for key, count in record["obstructed_core_hall_histogram"].items():
            hall_counts[key] += count
    return {
        "completed_witness_count": len(records),
        "removed_partition_matching_count_histogram": dict(
            sorted(matching_counts.items())
        ),
        "removed_partition_matching_count_by_shape": {
            f"{shape}:{count}": frequency
            for (shape, count), frequency in sorted(
                matching_counts_by_shape.items()
            )
        },
        "removed_partition_graph_degree_pattern_histogram": dict(
            sorted(removed_graph_degree_patterns.items())
        ),
        "removed_partition_universal_feasible_agent_count": {
            str(observer): universal_feasible_agents.get(
                str(observer),
                0,
            )
            for observer in range(N)
        },
        "matching_agent_owns_favorite_counts": dict(
            sorted(own_favorite_counts.items())
        ),
        "obstructed_core_hall_histogram": dict(
            sorted(hall_counts.items())
        ),
        "full_universe_supported_partition_count": {
            "min": min(full_support_counts) if full_support_counts else None,
            "max": max(full_support_counts) if full_support_counts else None,
            "mean": (
                sum(full_support_counts) / len(full_support_counts)
                if full_support_counts
                else None
            ),
            "histogram": dict(
                sorted(Counter(full_support_counts).items())
            ),
        },
    }


def run(
    *,
    checkpoint_path: Path,
    output_path: Path,
    per_check_limit: float,
    max_new_witnesses: int,
    aggregate_only: bool,
) -> dict:
    checkpoint_hash = sha256(checkpoint_path)
    checkpoint = json.loads(checkpoint_path.read_text())
    if (
        checkpoint.get("schema") != CHECKPOINT_SCHEMA
        or checkpoint.get("status") != "SHRUNK_CORE_UNSAT"
        or checkpoint.get("n") != N
        or checkpoint.get("m") != M
        or checkpoint.get("favorite_pattern") != list(FAVORITES)
        or checkpoint.get("active_partition_count") != 130
    ):
        raise ValueError("not the finalized favorite-211 core")

    partitions = [
        canonical_partition(partition)
        for partition in checkpoint["active_partitions"]
    ]
    global_indices = checkpoint["active_global_partition_indices"]
    if len(partitions) != len(global_indices) or len(set(partitions)) != 130:
        raise ValueError("invalid active core")
    source = json.loads(Path(checkpoint["input"]).read_text())
    source_partitions = [
        canonical_partition(partition)
        for partition in source["core_partitions"]
    ]
    source_global_indices = global_partition_indices(source_partitions)
    active_source_positions = checkpoint["active_source_positions"]
    if (
        [source_partitions[position] for position in active_source_positions]
        != partitions
        or [
            source_global_indices[position]
            for position in active_source_positions
        ]
        != global_indices
    ):
        raise ValueError("active core is not bound to its source positions")

    previous_records = []
    if output_path.is_file():
        previous = json.loads(output_path.read_text())
        if (
            previous.get("schema") != SCHEMA
            or previous.get("checkpoint_sha256") != checkpoint_hash
        ):
            raise ValueError("existing witness output belongs to another core")
        previous_records = previous.get("records", [])
    completed = {
        record["removed_global_partition_index"]
        for record in previous_records
    }
    if aggregate_only:
        if not output_path.is_file():
            raise ValueError("--aggregate-only requires an existing output")
        payload = dict(previous)
        payload.update(
            {
                "completed_witness_count": len(previous_records),
                "new_witness_count": 0,
                "elapsed_seconds_this_run": 0,
                "aggregate": aggregate(previous_records),
            }
        )
        atomic_json(output_path, payload)
        return payload

    master = make_master(source)
    activations = []
    for global_index, partition in zip(
        source_global_indices,
        source_partitions,
    ):
        activation = z3.Bool(f"witness_partition_{global_index}")
        master.add_partition_obstruction(partition, activation=activation)
        activations.append(activation)
    master.solver.set(timeout=round(per_check_limit * 1000))

    universe = tuple(
        canonical_partition([list(bundle) for bundle in partition])
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
    )
    if len(universe) != 1_701:
        raise AssertionError("unexpected partition universe")

    records = list(previous_records)
    started = time.monotonic()
    new_count = 0
    for removed_position, removed_global_index in enumerate(global_indices):
        if removed_global_index in completed:
            continue
        if max_new_witnesses and new_count >= max_new_witnesses:
            break
        removed_source_position = active_source_positions[removed_position]
        assumptions = [
            activations[source_position]
            for source_position in active_source_positions
            if source_position != removed_source_position
        ]
        check_started = time.monotonic()
        status = master.solver.check(*assumptions)
        check_seconds = time.monotonic() - check_started
        if status != z3.sat:
            raise RuntimeError(
                f"deleting partition {removed_global_index} returned {status}"
            )
        values = normalize_model_rows(master.solver.model(), master.values)

        core_summaries = [
            partition_summary(values, partition)
            for partition in partitions
        ]
        supported_positions = [
            position
            for position, summary in enumerate(core_summaries)
            if summary["matching_count"]
        ]
        if supported_positions != [removed_position]:
            raise AssertionError(
                "deletion witness does not uniquely support its removed "
                "partition inside the core"
            )

        hall_histogram = Counter()
        for position, summary in enumerate(core_summaries):
            if position == removed_position:
                continue
            hall = summary["hall_witnesses"]
            if not hall:
                raise AssertionError("obstructed core partition has no Hall witness")
            primary = hall[0]
            key = (
                f"{partition_shape(partitions[position])}:"
                f"{primary['agent_mask']}:"
                f"{primary['deficiency']}"
            )
            hall_histogram[key] += 1

        full_supported = []
        full_shapes = Counter()
        for global_index, partition in enumerate(universe):
            if perfect_matchings(feasible_graph(values, partition)):
                full_supported.append(global_index)
                full_shapes[partition_shape(partition)] += 1

        removed_summary = core_summaries[removed_position]
        slacks = [
            matching_slacks(values, partitions[removed_position], matching)
            for matching in perfect_matchings(
                feasible_graph(values, partitions[removed_position])
            )
        ]
        records.append(
            {
                "removed_global_partition_index": removed_global_index,
                "removed_position": removed_position,
                "partition": [
                    list(bundle) for bundle in partitions[removed_position]
                ],
                "shape": partition_shape(partitions[removed_position]),
                "values": [list(row) for row in values],
                "solver_seconds": round(check_seconds, 6),
                "removed_partition": removed_summary,
                "matching_slacks": [
                    {
                        "minimum": min(items),
                        "zero_count": sum(value == 0 for value in items),
                        "strictly_positive_count": sum(
                            value > 0 for value in items
                        ),
                    }
                    for items in slacks
                ],
                "obstructed_core_hall_histogram": dict(
                    sorted(hall_histogram.items())
                ),
                "full_universe_supported_partition_count": len(
                    full_supported
                ),
                "full_universe_supported_count_by_shape": dict(
                    sorted(full_shapes.items())
                ),
                "removed_partition_supported_in_full_universe": (
                    removed_global_index in full_supported
                ),
            }
        )
        new_count += 1
        payload = {
            "schema": SCHEMA,
            "status": (
                "COMPLETE"
                if len(records) == len(partitions)
                else "ACTIVE"
            ),
            "meaning": (
                "exact SAT witnesses obtained by deleting each indispensable "
                "partition from the 130-partition UNSAT core"
            ),
            "checkpoint": str(checkpoint_path.resolve()),
            "checkpoint_sha256": checkpoint_hash,
            "host": {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "z3": z3.get_version_string(),
            },
            "active_partition_count": len(partitions),
            "completed_witness_count": len(records),
            "new_witness_count": new_count,
            "elapsed_seconds_this_run": round(
                time.monotonic() - started,
                6,
            ),
            "aggregate": aggregate(records),
            "records": sorted(
                records,
                key=lambda record: record[
                    "removed_global_partition_index"
                ],
            ),
        }
        atomic_json(output_path, payload)

    payload = json.loads(output_path.read_text())
    payload.update(
        {
            "status": (
                "COMPLETE"
                if len(records) == len(partitions)
                else "ACTIVE"
            ),
            "completed_witness_count": len(records),
            "new_witness_count": new_count,
            "elapsed_seconds_this_run": round(
                time.monotonic() - started,
                6,
            ),
            "aggregate": aggregate(records),
            "records": sorted(
                records,
                key=lambda record: record[
                    "removed_global_partition_index"
                ],
            ),
        }
    )
    atomic_json(output_path, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-check-limit", type=float, default=120)
    parser.add_argument("--max-new-witnesses", type=int, default=0)
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    payload = run(
        checkpoint_path=args.checkpoint,
        output_path=args.output,
        per_check_limit=args.per_check_limit,
        max_new_witnesses=args.max_new_witnesses,
        aggregate_only=args.aggregate_only,
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key != "records"
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
