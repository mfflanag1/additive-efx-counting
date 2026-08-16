#!/usr/bin/env python3
"""Audit Hall-obstruction patterns in exact partition-deletion witnesses."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .analyze_core_deletion_witnesses import (
        CHECKPOINT_SCHEMA,
        SCHEMA as WITNESS_SCHEMA,
        feasible_graph,
        hall_witnesses,
        perfect_matchings,
    )
    from .analyze_shrunk_core import (
        anchored_pair_boundary,
        singleton_zero_anchor,
    )
    from .run_lra_cegar import atomic_json
    from .shrink_partition_core import canonical_partition
    from . import core
except ImportError:
    from analyze_core_deletion_witnesses import (
        CHECKPOINT_SCHEMA,
        SCHEMA as WITNESS_SCHEMA,
        feasible_graph,
        hall_witnesses,
        perfect_matchings,
    )
    from analyze_shrunk_core import (
        anchored_pair_boundary,
        singleton_zero_anchor,
    )
    from run_lra_cegar import atomic_json
    from shrink_partition_core import canonical_partition
    import core


SCHEMA = "partition-core-hall-pattern-audit-v1"
N = 4
M = 8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relocated_input(record_path: Path, declared: str) -> Path:
    path = Path(declared)
    if path.is_file():
        return path
    relocated = record_path.parent / path.name
    if relocated.is_file():
        return relocated
    raise FileNotFoundError(f"missing declared or relocated input: {declared}")


def mask_agents(mask: int) -> list[int]:
    return [agent for agent in range(N) if mask & (1 << agent)]


def exact_minimum_mask_covers(
    graph_masks: list[frozenset[int]],
) -> list[tuple[int, ...]]:
    universe = set(range(len(graph_masks)))
    coverage = {
        mask: {
            index
            for index, masks in enumerate(graph_masks)
            if mask in masks
        }
        for mask in range(1, 1 << N)
    }
    for size in range(1, 1 << N):
        solutions = []
        for masks in itertools.combinations(range(1, 1 << N), size):
            if set().union(*(coverage[mask] for mask in masks)) == universe:
                solutions.append(masks)
        if solutions:
            return solutions
    raise AssertionError("Hall witnesses failed to cover obstructed graphs")


def graph_signature(
    graph: tuple[tuple[bool, ...], ...],
) -> str:
    return "|".join(
        ",".join(str(bundle) for bundle, edge in enumerate(row) if edge)
        or "-"
        for row in graph
    )


def run(witness_path: Path, output_path: Path) -> dict:
    witness_hash = sha256(witness_path)
    witness = json.loads(witness_path.read_text())
    if (
        witness.get("schema") != WITNESS_SCHEMA
        or witness.get("active_partition_count") != 130
        or not witness.get("records")
    ):
        raise ValueError("not a nonempty 130-core deletion-witness file")

    checkpoint_path = relocated_input(witness_path, witness["checkpoint"])
    checkpoint_hash = sha256(checkpoint_path)
    if checkpoint_hash != witness["checkpoint_sha256"]:
        raise ValueError("witness/checkpoint hash mismatch")
    checkpoint = json.loads(checkpoint_path.read_text())
    if (
        checkpoint.get("schema") != CHECKPOINT_SCHEMA
        or checkpoint.get("status") != "SHRUNK_CORE_UNSAT"
        or checkpoint.get("n") != N
        or checkpoint.get("m") != M
        or checkpoint.get("favorite_pattern") != [0, 0, 1, 2]
    ):
        raise ValueError("not the finalized favorite-211 checkpoint")

    partitions = [
        canonical_partition(partition)
        for partition in checkpoint["active_partitions"]
    ]
    if len(partitions) != 130 or len(set(partitions)) != 130:
        raise ValueError("invalid active partition set")

    universe = tuple(
        canonical_partition([list(bundle) for bundle in partition])
        for partition in core.iter_unlabeled_nonempty_partitions(N, M)
    )
    singleton_family = {
        partition for partition in universe
        if singleton_zero_anchor(partition)
    }
    pair_family = {
        partition for partition in universe
        if anchored_pair_boundary(partition)
    }
    invariant_family = singleton_family | pair_family
    if (
        len(universe) != 1_701
        or len(singleton_family) != 131
        or len(pair_family) != 60
        or len(invariant_family) != 191
        or not set(partitions) <= invariant_family
    ):
        raise AssertionError("anchored-family census changed")

    primary_masks = Counter()
    all_masks = Counter()
    inclusion_minimal_masks = Counter()
    signatures = Counter()
    graph_masks = []
    checked_graphs = 0
    for record in witness["records"]:
        values = tuple(tuple(row) for row in record["values"])
        removed_position = record["removed_position"]
        for position, partition in enumerate(partitions):
            graph = feasible_graph(values, partition)
            matchings = perfect_matchings(graph)
            if position == removed_position:
                if not matchings:
                    raise AssertionError("removed partition lacks a matching")
                continue
            if matchings:
                raise AssertionError(
                    "nonremoved core partition unexpectedly has a matching"
                )
            hall = hall_witnesses(graph)
            if not hall:
                raise AssertionError("obstructed graph lacks a Hall witness")
            masks = frozenset(item[0] for item in hall)
            graph_masks.append(masks)
            checked_graphs += 1
            primary_masks[hall[0][0]] += 1
            all_masks.update(masks)
            inclusion_minimal = {
                mask
                for mask in masks
                if not any(
                    other != mask and other & mask == other
                    for other in masks
                )
            }
            inclusion_minimal_masks.update(inclusion_minimal)
            signatures[graph_signature(graph)] += 1

    expected_graphs = len(witness["records"]) * 129
    if checked_graphs != expected_graphs:
        raise AssertionError("unexpected obstructed-graph count")
    minimum_covers = exact_minimum_mask_covers(graph_masks)

    def mask_counter(counter: Counter) -> dict:
        return {
            str(mask): {
                "agents": mask_agents(mask),
                "count": counter[mask],
            }
            for mask in sorted(counter)
        }

    payload = {
        "schema": SCHEMA,
        "meaning": (
            "exact descriptive Hall-pattern audit of deletion witnesses; "
            "sample regularities are not universal theorems"
        ),
        "witnesses": str(witness_path.resolve()),
        "witnesses_sha256": witness_hash,
        "checkpoint": str(checkpoint_path.resolve()),
        "checkpoint_sha256": checkpoint_hash,
        "completed_deletion_witness_count": len(witness["records"]),
        "obstructed_graph_count": checked_graphs,
        "distinct_feasibility_graph_count": len(signatures),
        "hall_masks": {
            "primary": mask_counter(primary_masks),
            "all": mask_counter(all_masks),
            "inclusion_minimal": mask_counter(inclusion_minimal_masks),
            "minimum_cover_size": len(minimum_covers[0]),
            "minimum_cover_count": len(minimum_covers),
            "minimum_covers": [
                [
                    {"mask": mask, "agents": mask_agents(mask)}
                    for mask in cover
                ]
                for cover in minimum_covers
            ],
        },
        "top_feasibility_graph_signatures": [
            {"signature": signature, "count": count}
            for signature, count in signatures.most_common(20)
        ],
        "anchored_family": {
            "partition_universe_count": len(universe),
            "singleton_zero_family_count": len(singleton_family),
            "anchored_pair_boundary_count": len(pair_family),
            "invariant_union_count": len(invariant_family),
            "certified_core_count": len(partitions),
            "certified_core_is_subset": set(partitions) <= invariant_family,
        },
        "analytic_target": {
            "name": "anchored contested-favorite lemma",
            "statement": (
                "For every normalized positive additive 4x8 valuation with "
                "strict favorite pattern (0,0,1,2), no universal minimum, "
                "no peelable pair, and distinct rows, at least one of the "
                "191 invariant anchored partitions has a feasible perfect "
                "matching."
            ),
            "status": (
                "implied by the certified 130-partition UNSAT core, but a "
                "concise human proof is open"
            ),
            "hall_mask_warning": (
                "The sampled obstructed graphs do not collapse to a small "
                "list of dominant agent masks; use bundle geometry and "
                "threshold inequalities instead."
            ),
        },
    }
    atomic_json(output_path, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witnesses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run(args.witnesses, args.output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
