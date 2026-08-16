#!/usr/bin/env python3
"""Replay adaptive Hall-hole exchange paths on the frozen row-merge corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import minimal_hall_witnesses
    from .decide_row_merge_single_wall_radius import literal_graph, matching_count
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import minimal_hall_witnesses
    from decide_row_merge_single_wall_radius import literal_graph, matching_count


SCHEMA = "row-merge-q4-adaptive-hall-path-analysis-v1"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7, 8))
N = 4
PERTURBED_GOOD = 2
FIXED_WALL_GRAPH = (
    (True, True, True, False),
    (False, True, False, True),
    (False, True, True, False),
    (False, True, False, True),
)
FIXED_POST_GRAPH = (
    (False, True, True, False),
    (False, True, False, True),
    (False, True, True, False),
    (False, True, False, True),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def values_sha256(values) -> str:
    payload = json.dumps(values, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def load_trace_model(path: Path, round_index: int) -> tuple[list, list]:
    trace = json.loads(path.read_text())
    if tuple(tuple(bundle) for bundle in trace.get("wall_partition", ())) != BASE:
        raise AssertionError(f"wall partition changed in {path}")
    if trace.get("schema") == "row-merge-q4-exchange-chain-cegar-v1":
        records = [
            record
            for record in trace["rounds"]
            if record.get("round") == round_index
            and record.get("solver_status") == "sat"
        ]
        if len(records) != 1:
            raise AssertionError(f"SAT round {round_index} is not unique in {path}")
        record = records[0]
        return record["wall_values"], record["post_wall_values"]
    if (
        trace.get("schema") == "row-merge-q4-cycle023-gate-v1"
        and round_index == 0
        and trace.get("solver_status") == "sat"
    ):
        return trace["wall_values"], trace["post_wall_values"]
    raise AssertionError(f"unsupported exact trace schema in {path}")


def changed_edges(wall_values, post_values) -> tuple[tuple, ...]:
    wall_graph = literal_graph(wall_values, BASE)
    post_graph = literal_graph(post_values, BASE)
    return tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(N)
        for bundle in range(N)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )


def is_generic_model(wall_values, post_values) -> bool:
    if literal_graph(wall_values, BASE) != FIXED_WALL_GRAPH:
        return False
    if literal_graph(post_values, BASE) != FIXED_POST_GRAPH:
        return False
    if changed_edges(wall_values, post_values) != ((0, 0, True, False),):
        return False
    changed_values = tuple(
        (agent, good)
        for agent in range(N)
        for good in range(len(wall_values[agent]))
        if wall_values[agent][good] != post_values[agent][good]
    )
    return changed_values == ((0, PERTURBED_GOOD),)


def collect_models(
    analysis_path: Path,
    ranked_paths: tuple[Path, ...],
) -> tuple[list[dict], list[dict], list[dict]]:
    analysis = json.loads(analysis_path.read_text())
    if (
        analysis.get("schema") != "row-merge-q4-chain-trace-analysis-v1"
        or analysis.get("status") != "EXACT_TRACE_MOTIFS_CLASSIFIED"
    ):
        raise AssertionError("topology analysis is not the frozen exact trace")

    raw = []
    sources = {str(analysis_path): sha256(analysis_path)}
    for model in analysis["models"]:
        path = Path(model["trace"])
        if sha256(path) != model["trace_sha256"]:
            raise AssertionError(f"trace hash changed: {path}")
        wall_values, post_values = load_trace_model(path, model["round"])
        raw.append(
            {
                "wall_values": wall_values,
                "post_values": post_values,
                "provenance": {
                    "source": str(path),
                    "source_sha256": sha256(path),
                    "round": model["round"],
                    "corpus": "topology_mining",
                },
            }
        )
        sources[str(path)] = sha256(path)

    for path in ranked_paths:
        trace = json.loads(path.read_text())
        if (
            trace.get("schema") != "row-merge-q4-ranked-path-cegar-v1"
            or tuple(tuple(bundle) for bundle in trace.get("wall_partition", ()))
            != BASE
        ):
            raise AssertionError(f"ranked-path trace changed: {path}")
        sources[str(path)] = sha256(path)
        for record in trace["rounds"]:
            if record.get("solver_status") != "sat":
                continue
            raw.append(
                {
                    "wall_values": record["wall_values"],
                    "post_values": record["post_wall_values"],
                    "provenance": {
                        "source": str(path),
                        "source_sha256": sha256(path),
                        "round": record["round"],
                        "corpus": "ranked_path",
                    },
                }
            )

    grouped = {}
    non_generic = []
    for record in raw:
        wall_values = record["wall_values"]
        post_values = record["post_values"]
        if not is_generic_model(wall_values, post_values):
            non_generic.append(
                {
                    "provenance": record["provenance"],
                    "wall_graph": [list(row) for row in literal_graph(wall_values, BASE)],
                    "post_graph": [list(row) for row in literal_graph(post_values, BASE)],
                    "changed_edges": [list(edge) for edge in changed_edges(wall_values, post_values)],
                }
            )
            continue
        key = (values_sha256(wall_values), values_sha256(post_values))
        if key not in grouped:
            grouped[key] = {
                "wall_values": wall_values,
                "post_values": post_values,
                "wall_values_sha256": key[0],
                "post_values_sha256": key[1],
                "provenance": [],
            }
        grouped[key]["provenance"].append(record["provenance"])
    generic = [grouped[key] for key in sorted(grouped)]
    source_records = [
        {"path": path, "sha256": digest} for path, digest in sorted(sources.items())
    ]
    return generic, non_generic, source_records


def move_good(partition, source: int, target: int, good: int) -> tuple:
    moved = [list(bundle) for bundle in partition]
    moved[source].remove(good)
    moved[target].append(good)
    return tuple(tuple(sorted(bundle)) for bundle in moved)


def search_hall_hole_paths(values) -> dict:
    successes = {}
    visited_states = set()
    terminal_failures = Counter()

    def visit(partition, hole, used_sources, moves, blocker_sizes):
        state = (partition, hole, used_sources)
        visited_states.add(state)
        feasible = literal_graph(values, partition)
        count = matching_count(feasible)
        if count:
            move_key = tuple((move["source"], move["target"], move["good"]) for move in moves)
            successes[move_key] = {
                "moves": moves,
                "partition": [list(bundle) for bundle in partition],
                "matching_count": count,
                "blocker_size_sequence": blocker_sizes,
            }
            return
        if len(moves) == N - 1:
            terminal_failures["depth_limit"] += 1
            return

        witnesses = [
            (agents, neighbors)
            for agents, neighbors in minimal_hall_witnesses(feasible)
            if hole not in neighbors
        ]
        transitions = defaultdict(set)
        for agents, neighbors in witnesses:
            for source in neighbors:
                if (
                    source == hole
                    or source in used_sources
                    or len(partition[source]) <= 1
                ):
                    continue
                for good in partition[source]:
                    transitions[(source, good)].add((agents, neighbors))
        if not transitions:
            terminal_failures["no_hall_neighborhood_move"] += 1
            return
        for source, good in sorted(transitions):
            witness = min(transitions[(source, good)])
            move = {
                "source": source,
                "target": hole,
                "good": good,
                "hall_agents": list(witness[0]),
                "hall_neighbors": list(witness[1]),
            }
            visit(
                move_good(partition, source, hole, good),
                source,
                used_sources | frozenset((source,)),
                [*moves, move],
                [*blocker_sizes, len(witness[0])],
            )

    # The initial hole is the endpoint of the simple path and cannot later be
    # used as a source. Subsequent sources are likewise never reused.
    visit(BASE, 0, frozenset((0,)), [], [])
    records = list(successes.values())
    depth_histogram = Counter(len(record["moves"]) for record in records)
    partition_count = len(
        {tuple(tuple(bundle) for bundle in record["partition"]) for record in records}
    )
    return {
        "adaptive_path_count": len(records),
        "supporting_partition_count": partition_count,
        "minimum_success_depth": min(depth_histogram) if depth_histogram else None,
        "success_depth_histogram": {
            str(depth): depth_histogram[depth] for depth in sorted(depth_histogram)
        },
        "visited_state_count": len(visited_states),
        "terminal_failure_histogram": {
            key: terminal_failures[key] for key in sorted(terminal_failures)
        },
        "sample_success": records[0] if records else None,
    }


def run(
    analysis_path: Path,
    ranked_paths: tuple[Path, ...],
    output_path: Path,
) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    generic, non_generic, sources = collect_models(analysis_path, ranked_paths)
    model_records = []
    for model in generic:
        analysis = search_hall_hole_paths(model["post_values"])
        model_records.append(
            {
                "wall_values_sha256": model["wall_values_sha256"],
                "post_values_sha256": model["post_values_sha256"],
                "provenance": model["provenance"],
                **analysis,
            }
        )

    covered = sum(record["adaptive_path_count"] > 0 for record in model_records)
    result = {
        "schema": SCHEMA,
        "status": (
            "ADAPTIVE_HALL_HOLE_PATH_COVERS_FROZEN_GENERIC_CORPUS"
            if covered == len(model_records) and model_records
            else "ADAPTIVE_HALL_HOLE_PATH_HAS_FROZEN_COUNTERMODEL"
        ),
        "domain": "frozen exact integer models in one generic q=4 row-merge cell",
        "wall_partition": [list(bundle) for bundle in BASE],
        "initial_hole_bundle": 0,
        "maximum_transfer_depth": N - 1,
        "move_rule": (
            "At an unmatched labeled partition, choose an inclusion-minimal Hall-"
            "deficient agent set whose neighborhood omits the current hole; move one "
            "good from a non-singleton bundle in that neighborhood into the hole, "
            "then make the source the new hole. Sources are distinct, and the "
            "initial hole is never used as a source."
        ),
        "fixed_wall_graph": [list(row) for row in FIXED_WALL_GRAPH],
        "fixed_post_graph": [list(row) for row in FIXED_POST_GRAPH],
        "raw_model_count": sum(
            len(model["provenance"]) for model in generic
        )
        + len(non_generic),
        "generic_model_occurrence_count": sum(
            len(model["provenance"]) for model in generic
        ),
        "distinct_generic_model_count": len(generic),
        "covered_distinct_generic_model_count": covered,
        "non_generic_model_occurrence_count": len(non_generic),
        "non_generic_models": non_generic,
        "sources": sources,
        "models": model_records,
        "interpretation": (
            "This is exact finite-trace evidence for an adaptive Hall-guided exchange "
            "mechanism. Coverage means every frozen generic adversarial valuation has "
            "at least one such path of at most three transfers."
        ),
        "claim_boundary": (
            "The selector is existential and recomputes a Hall blocker after each "
            "move. Finite-corpus coverage is not a universal lemma, does not prove the "
            "row-merge continuation claim, and does not prove complete additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--ranked", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.analysis, tuple(args.ranked), args.output)


if __name__ == "__main__":
    main()
