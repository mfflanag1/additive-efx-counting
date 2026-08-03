#!/usr/bin/env python3
"""Audit the open mixed-Hall rank-selection gates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from .run_common_favorite_mixed_zero_neighbor_cegar import (
        proportional_rows,
        reconstruct_seed_motifs,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_threshold_pass_hall import (
        FAVORITE,
        M,
        N,
        SHAPES,
        residual_partitions,
        threshold_passes,
    )
    from run_common_favorite_mixed_zero_neighbor_cegar import (
        proportional_rows,
        reconstruct_seed_motifs,
    )


SCHEMA = "common-favorite-mixed-selection-gate-audit-v1"
EXPECTED_PROFILE_CENSUS = (
    {
        "threshold_pass_count": 114,
        "maximum_resident_rank": 2,
        "maximum_rank_pass_count": 49,
        "maximum_rank_type_count": {"pair_witness": 9, "zero_bundle": 40},
        "maximum_edge_count": 6,
        "maximum_edge_pass_type_count": {"zero_bundle": 2},
    },
    {
        "threshold_pass_count": 273,
        "maximum_resident_rank": 2,
        "maximum_rank_pass_count": 273,
        "maximum_rank_type_count": {"pair_witness": 120, "zero_bundle": 153},
        "maximum_edge_count": 5,
        "maximum_edge_pass_type_count": {"pair_witness": 12},
    },
    {
        "threshold_pass_count": 36,
        "maximum_resident_rank": 2,
        "maximum_rank_pass_count": 17,
        "maximum_rank_type_count": {"pair_witness": 6, "zero_bundle": 11},
        "maximum_edge_count": 6,
        "maximum_edge_pass_type_count": {"zero_bundle": 1},
    },
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resident_graph(values, owner, partition):
    graph = feasible_graph(values, ((FAVORITE,),) + partition)
    return tuple(
        tuple(graph[agent][bundle] for bundle in range(1, N))
        for agent in range(N)
        if agent != owner
    )


def witness_type(graph):
    neighbor_sets = tuple(
        frozenset(row for row in range(N - 1) if graph[row][bundle])
        for bundle in range(N - 1)
    )
    if any(not neighbors for neighbors in neighbor_sets):
        return "zero_bundle"
    if any(
        len(neighbor_sets[left] | neighbor_sets[right]) < 2
        for left, right in itertools.combinations(range(N - 1), 2)
    ):
        return "pair_witness"
    if len(frozenset().union(*neighbor_sets)) < N - 1:
        return "full_witness"
    raise AssertionError("rank-deficient graph has no Hall witness")


def profile_census(path):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema")
        != "common-favorite-threshold-pass-hall-cpsat-v1"
        or payload.get("status") != "THRESHOLD_PASS_WITHOUT_SINGLETON_EFX"
        or payload.get("values") is None
    ):
        raise ValueError("profile source metadata changed")
    values = tuple(tuple(row) for row in payload["values"])
    if (
        len(values) != N
        or any(len(row) != M or row[0] <= max(row[1:]) for row in values)
        or any(value < 1 or value > payload["upper"] for row in values for value in row)
    ):
        raise AssertionError("profile left the positive strict-favorite domain")

    passes = []
    singleton_support = 0
    for partition in residual_partitions():
        full = ((FAVORITE,),) + partition
        singleton_support += matching_rank(feasible_graph(values, full)) == N
        for owner in range(N):
            if threshold_passes(values, owner, partition):
                graph = resident_graph(values, owner, partition)
                passes.append({
                    "rank": matching_rank(graph),
                    "edges": sum(map(sum, graph)),
                    "type": witness_type(graph),
                })
    if singleton_support or not passes:
        raise AssertionError("profile left the mixed branch")
    maximum_rank = max(item["rank"] for item in passes)
    rank_maximal = [item for item in passes if item["rank"] == maximum_rank]
    maximum_edges = max(item["edges"] for item in rank_maximal)
    edge_maximal = [item for item in rank_maximal if item["edges"] == maximum_edges]
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "selected_residual_shape": payload["selected_residual_shape"],
        "threshold_pass_count": len(passes),
        "favorite_singleton_supporting_partition_count": 0,
        "maximum_resident_rank": maximum_rank,
        "maximum_rank_pass_count": len(rank_maximal),
        "maximum_rank_type_count": dict(sorted(Counter(
            item["type"] for item in rank_maximal
        ).items())),
        "maximum_edge_count": maximum_edges,
        "maximum_edge_pass_type_count": dict(sorted(Counter(
            item["type"] for item in edge_maximal
        ).items())),
    }


def selection_motifs(values, motif):
    found = []
    for partition_index, partition in enumerate(residual_partitions()):
        for owner in range(N):
            if not threshold_passes(values, owner, partition):
                continue
            graph = resident_graph(values, owner, partition)
            if matching_rank(graph) != N - 2:
                continue
            if motif == "rank_two":
                found.append((owner, partition_index, None))
            else:
                for bundle in range(N - 1):
                    if not any(row[bundle] for row in graph):
                        found.append((owner, partition_index, bundle))
    return found


def audit_search(
    path,
    motif,
    upper=20,
    require_pairwise_nonproportional_rows=False,
):
    payload = json.loads(path.read_text())
    accepted_schemas = {
        "common-favorite-mixed-zero-neighbor-cegar-v1",
        "common-favorite-mixed-selection-cegar-v1",
    }
    if (
        payload.get("schema") not in accepted_schemas
        or payload.get("status") not in {"MASTER_UNKNOWN", "ITERATION_LIMIT"}
        or payload.get("upper") != upper
        or payload.get("selected_residual_shape") != "332"
        or (payload.get("selection_motif") or "zero_neighbor_rank_two") != motif
        or payload.get("require_pairwise_nonproportional_rows", False)
        != require_pairwise_nonproportional_rows
        or payload.get("values") is not None
    ):
        raise ValueError("selection-search metadata changed")
    proto = Path(payload["proto"])
    if not proto.is_file() or sha256(proto) != payload["proto_sha256"]:
        raise AssertionError("selection-search proto changed")

    residual = tuple(residual_partitions())
    learned = set()
    for imported in payload.get("seed_imports", []):
        seed_path = Path(imported["source"])
        if (
            not seed_path.is_file()
            or sha256(seed_path) != imported["source_sha256"]
        ):
            raise AssertionError("selection seed changed")
        learned.update(
            reconstruct_seed_motifs(seed_path, motif, upper, residual)
        )
    initial_learned_count = len(learned)
    motif_sequence = []
    for index, record in enumerate(payload["trace"]):
        values = tuple(tuple(row) for row in record["values"])
        if (
            record["iteration"] != index + 1
            or record["learned_motif_count_before"] != len(learned)
            or any(
                type(value) is not int or not 1 <= value <= upper
                for row in values
                for value in row
            )
            or any(row[0] <= max(row[1:]) for row in values)
            or not threshold_passes(values, 0, SHAPES["332"])
        ):
            raise AssertionError("selection trace left the target cell")
        if require_pairwise_nonproportional_rows and any(
            proportional_rows(values[left], values[right])
            for left in range(N)
            for right in range(left + 1, N)
        ):
            raise AssertionError("selection trace gained proportional rows")
        if any(
            matching_rank(feasible_graph(values, ((FAVORITE,),) + partition)) == N
            for partition in residual_partitions()
        ):
            raise AssertionError("selection trace gained singleton EFX")
        motifs = [item for item in selection_motifs(values, motif) if item not in learned]
        recorded_count = record.get(
            "unlearned_selection_motif_count",
            record.get("unlearned_zero_neighbor_rank_two_motif_count"),
        )
        if len(motifs) != recorded_count:
            raise AssertionError("selection motif census changed")
        motif_sequence.append(len(motifs))
        target_size = (
            payload["trace"][index + 1]["learned_motif_count_before"]
            if index + 1 < len(payload["trace"])
            else payload["learned_motif_count"]
        )
        add_count = target_size - len(learned)
        if not 0 <= add_count <= len(motifs):
            raise AssertionError("selection learned-count transition changed")
        learned.update(motifs[:add_count])
    if len(learned) != payload["learned_motif_count"]:
        raise AssertionError("learned selection pool changed")
    reconstructed = reconstruct_seed_motifs(path, motif, upper, residual)
    if learned != reconstructed:
        raise AssertionError("serialized selection pool disagrees with replay")
    result = {
        "source": str(path),
        "source_sha256": sha256(path),
        "motif": motif,
        "endpoint": payload["status"],
        "solver_status": payload["solver_status"],
        "iterations": len(payload["trace"]),
        "unlearned_motif_count_sequence": motif_sequence,
        "reconstructed_learned_motif_count": len(learned),
        "proto_sha256": payload["proto_sha256"],
    }
    if payload.get("seed_imports"):
        result["initial_learned_motif_count"] = initial_learned_count
    return result


def run(profile_paths, zero_path, rank_path, output):
    if len(profile_paths) != 3 or output.exists():
        raise ValueError("three profiles and a new output are required")
    profiles = [profile_census(path) for path in profile_paths]
    for profile, expected in zip(profiles, EXPECTED_PROFILE_CENSUS):
        observed = {key: profile[key] for key in expected}
        if observed != expected:
            raise AssertionError("rank-maximal profile census changed")
    searches = [
        audit_search(zero_path, "zero_neighbor_rank_two"),
        audit_search(rank_path, "rank_two"),
    ]
    result = {
        "schema": SCHEMA,
        "status": "MIXED_SELECTION_GATE_OPEN",
        "n": N,
        "m": M,
        "domain": "positive additive valuations",
        "strict_common_favorite": FAVORITE,
        "profile_census": profiles,
        "bounded_searches": searches,
        "candidate_lemma": (
            "Every mixed profile has a threshold-passing owner/partition "
            "whose resident graph has matching rank two; a stronger version "
            "also asks for a zero-neighbor bundle."
        ),
        "evidence": (
            "All three exact shortcut-refuting profiles attain resident rank "
            "two, and each has a rank-two pass with a zero-neighbor bundle."
        ),
        "claim_boundary": (
            "The CEGAR searches found neither a selector counterexample nor "
            "an UNSAT certificate. Their timeout and iteration-limit endpoints "
            "are computational boundaries, not proofs of either selection claim."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, action="append", required=True)
    parser.add_argument("--zero-search", type=Path, required=True)
    parser.add_argument("--rank-search", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.profile, args.zero_search, args.rank_search, args.output)


if __name__ == "__main__":
    main()
