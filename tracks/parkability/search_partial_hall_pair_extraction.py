#!/usr/bin/env python3
"""Test cap-free pair extraction after all radius-one Hall completions fail."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
except ImportError:
    import core
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json


SCHEMA = "partial-hall-pair-extraction-search-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_for_partition(totals, thresholds, masks):
    graph = []
    for agent in range(4):
        row = []
        for owned in range(4):
            own = totals[agent][masks[owned]]
            if all(
                target == owned or own >= thresholds[agent][masks[target]]
                for target in range(4)
            ):
                row.append(owned)
        graph.append(tuple(row))
    return tuple(graph)


def has_perfect_matching(graph) -> bool:
    return any(
        all(permutation[agent] in graph[agent] for agent in range(4))
        for permutation in itertools.permutations(range(4))
    )


def hall_witnesses(graph):
    witnesses = []
    for size in range(1, 5):
        for agents in itertools.combinations(range(4), size):
            neighbors = {bundle for agent in agents for bundle in graph[agent]}
            if len(neighbors) < size:
                witnesses.append((agents, tuple(sorted(neighbors))))
    return tuple(witnesses)


def candidate_partitions(state, m: int):
    old_owner = {}
    for source, mask in enumerate(state["masks"]):
        for good in range(m):
            if mask & (1 << good):
                old_owner[good] = source
    candidates = {}
    for host in range(4):
        inserted = list(state["masks"])
        inserted[host] |= 1 << state["floater"]
        candidates.setdefault(
            tuple(inserted),
            {"floater_host": host, "moved_good": None},
        )
    for host in range(4):
        inserted = list(state["masks"])
        inserted[host] |= 1 << state["floater"]
        for good, source in old_owner.items():
            for destination in range(4):
                if destination == source:
                    continue
                moved = inserted.copy()
                moved[source] ^= 1 << good
                moved[destination] |= 1 << good
                if all(moved):
                    candidates.setdefault(
                        tuple(moved),
                        {
                            "floater_host": host,
                            "moved_good": good,
                            "move_source": source,
                            "move_destination": destination,
                        },
                    )
    return tuple(candidates.items())


def public_state(state):
    return {
        "floater": state["floater"],
        "base_index": state["base_index"],
        "masks": list(state["masks"]),
        "utilities": list(state["utilities"]),
        "bundle_sizes": [mask.bit_count() for mask in state["masks"]],
    }


def classify_candidate_family(totals, thresholds, candidates):
    pair = None
    obstruction = None
    for masks, operation in candidates:
        graph = graph_for_partition(totals, thresholds, masks)
        if has_perfect_matching(graph):
            return True, pair, obstruction
        witnesses = hall_witnesses(graph)
        if obstruction is None:
            obstruction = (masks, graph, witnesses)
        for agents, neighbors in witnesses:
            if len(agents) == 2 and len(neighbors) == 1 and pair is None:
                pair = (masks, graph, agents, neighbors, operation)
    return False, pair, obstruction


def audit_values(values, source: str, source_sha256: str, max_states: int | None):
    values = core.validate_values(values, expected_n=4, lower=1)
    m = len(values[0])
    totals, thresholds = core._subset_tables(values)
    states = enumerate_states(values)
    states_available = len(states)
    if max_states is not None:
        states = states[:max_states]

    radius_one_completable = 0
    blocked_with_pair = 0
    counterexamples = []
    shapes = Counter()
    witness_sizes = Counter()
    blocked_pair_radii = Counter()
    blocked_pair_relations = Counter()
    candidate_count = 0
    first_blocked_pair = None
    direct_completable = 0
    direct_blocked_with_host_pair = 0
    direct_counterexamples = []
    owner_minimum_completable = 0
    owner_minimum_blocked_with_pair = 0
    owner_minimum_counterexamples = []
    host_minimum_completable = 0
    host_minimum_blocked_with_pair = 0
    host_minimum_counterexamples = []

    for state in states:
        shapes[tuple(sorted(mask.bit_count() for mask in state["masks"]))] += 1
        found_completion = False
        found_pair = None
        representative_obstruction = None
        candidates = candidate_partitions(state, m)
        candidate_count += len(candidates)
        direct_completion = False
        direct_host_pair = None
        direct_obstruction = None
        for masks, operation in candidates[:4]:
            assert operation["moved_good"] is None
            graph = graph_for_partition(totals, thresholds, masks)
            if has_perfect_matching(graph):
                direct_completion = True
                continue
            witnesses = hall_witnesses(graph)
            if direct_obstruction is None:
                direct_obstruction = (masks, graph, witnesses)
            for agents, neighbors in witnesses:
                if (
                    len(agents) == 2
                    and neighbors == (operation["floater_host"],)
                    and direct_host_pair is None
                ):
                    direct_host_pair = (masks, graph, agents, neighbors, operation)
        if direct_completion:
            direct_completable += 1
        elif direct_host_pair is not None:
            direct_blocked_with_host_pair += 1
        elif not direct_counterexamples:
            masks, graph, witnesses = direct_obstruction
            direct_counterexamples.append(
                {
                    **public_state(state),
                    "representative_partition": list(masks),
                    "representative_graph": [list(row) for row in graph],
                    "representative_hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in witnesses
                    ],
                }
            )
        owner_minima = {}
        for source, mask in enumerate(state["masks"]):
            goods = [good for good in range(m) if mask & (1 << good)]
            minimum = min(values[source][good] for good in goods)
            owner_minima[source] = {
                good for good in goods if values[source][good] == minimum
            }
        selected_candidates = [
            candidate
            for candidate in candidates
            if candidate[1]["moved_good"] is None
            or candidate[1]["moved_good"]
            in owner_minima[candidate[1]["move_source"]]
        ]
        selected_completion = False
        selected_pair = None
        selected_obstruction = None
        for masks, operation in selected_candidates:
            graph = graph_for_partition(totals, thresholds, masks)
            if has_perfect_matching(graph):
                selected_completion = True
                break
            witnesses = hall_witnesses(graph)
            if selected_obstruction is None:
                selected_obstruction = (masks, graph, witnesses)
            for agents, neighbors in witnesses:
                if len(agents) == 2 and len(neighbors) == 1 and selected_pair is None:
                    selected_pair = (masks, graph, agents, neighbors, operation)
        if selected_completion:
            owner_minimum_completable += 1
        elif selected_pair is not None:
            owner_minimum_blocked_with_pair += 1
        elif not owner_minimum_counterexamples:
            masks, graph, witnesses = selected_obstruction
            owner_minimum_counterexamples.append(
                {
                    **public_state(state),
                    "selected_candidate_count": len(selected_candidates),
                    "representative_partition": list(masks),
                    "representative_graph": [list(row) for row in graph],
                    "representative_hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in witnesses
                    ],
                }
            )
        host_selected_candidates = [
            candidate
            for candidate in selected_candidates
            if candidate[1]["moved_good"] is None
            or candidate[1]["move_source"] == candidate[1]["floater_host"]
        ]
        host_completion, host_pair, host_obstruction = classify_candidate_family(
            totals, thresholds, host_selected_candidates
        )
        if host_completion:
            host_minimum_completable += 1
        elif host_pair is not None:
            host_minimum_blocked_with_pair += 1
        elif not host_minimum_counterexamples:
            masks, graph, witnesses = host_obstruction
            host_minimum_counterexamples.append(
                {
                    **public_state(state),
                    "selected_candidate_count": len(host_selected_candidates),
                    "representative_partition": list(masks),
                    "representative_graph": [list(row) for row in graph],
                    "representative_hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in witnesses
                    ],
                }
            )
        for masks, operation in candidates:
            graph = graph_for_partition(totals, thresholds, masks)
            if has_perfect_matching(graph):
                found_completion = True
                break
            witnesses = hall_witnesses(graph)
            if representative_obstruction is None:
                representative_obstruction = (masks, graph, witnesses)
            for agents, neighbors in witnesses:
                witness_sizes[(len(agents), len(neighbors))] += 1
                if len(agents) == 2 and len(neighbors) == 1 and found_pair is None:
                    found_pair = (masks, graph, agents, neighbors, operation)
        if found_completion:
            radius_one_completable += 1
        elif found_pair is not None:
            blocked_with_pair += 1
            masks, graph, agents, neighbors, operation = found_pair
            radius = 0 if operation["moved_good"] is None else 1
            blocked_pair_radii[radius] += 1
            host = operation["floater_host"]
            neighbor = neighbors[0]
            relation = (
                radius,
                host in agents,
                neighbor == host,
                neighbor in agents,
            )
            blocked_pair_relations[relation] += 1
            if first_blocked_pair is None:
                first_blocked_pair = {
                    "state": public_state(state),
                    "candidate_masks": list(masks),
                    "candidate_graph": [list(row) for row in graph],
                    "pair_agents": list(agents),
                    "sole_neighbor": neighbor,
                    "operation": operation,
                }
        else:
            masks, graph, witnesses = representative_obstruction
            counterexamples.append(
                {
                    **public_state(state),
                    "candidate_partition_count": len(candidates),
                    "representative_partition": list(masks),
                    "representative_graph": [list(row) for row in graph],
                    "representative_hall_witnesses": [
                        {"agents": list(agents), "neighbors": list(neighbors)}
                        for agents, neighbors in witnesses
                    ],
                }
            )
            break

    return {
        "source": source,
        "source_sha256": source_sha256,
        "m": m,
        "states_available": states_available,
        "states_tested": len(states),
        "candidate_partitions_tested_or_generated": candidate_count,
        "direct_hall_completable_states": direct_completable,
        "direct_hall_blocked_with_host_pair_states": direct_blocked_with_host_pair,
        "direct_host_pair_extraction_counterexample_found": bool(
            direct_counterexamples
        ),
        "first_direct_host_pair_counterexample": (
            direct_counterexamples[0] if direct_counterexamples else None
        ),
        "owner_minimum_hall_completable_states": owner_minimum_completable,
        "owner_minimum_blocked_with_pair_states": owner_minimum_blocked_with_pair,
        "owner_minimum_pair_extraction_counterexample_found": bool(
            owner_minimum_counterexamples
        ),
        "first_owner_minimum_pair_counterexample": (
            owner_minimum_counterexamples[0] if owner_minimum_counterexamples else None
        ),
        "host_minimum_hall_completable_states": host_minimum_completable,
        "host_minimum_blocked_with_pair_states": host_minimum_blocked_with_pair,
        "host_minimum_pair_extraction_counterexample_found": bool(
            host_minimum_counterexamples
        ),
        "first_host_minimum_pair_counterexample": (
            host_minimum_counterexamples[0] if host_minimum_counterexamples else None
        ),
        "radius_one_hall_completable_states": radius_one_completable,
        "hall_blocked_with_pair_extraction_states": blocked_with_pair,
        "pair_extraction_counterexample_found": bool(counterexamples),
        "first_counterexample": counterexamples[0] if counterexamples else None,
        "first_blocked_pair_witness": first_blocked_pair,
        "blocked_pair_move_radius_histogram": {
            str(radius): count for radius, count in sorted(blocked_pair_radii.items())
        },
        "blocked_pair_relation_histogram": {
            (
                f"radius={radius},host_in_pair={host_in_pair},"
                f"neighbor_is_host={neighbor_is_host},"
                f"neighbor_in_pair={neighbor_in_pair}"
            ): count
            for (
                radius,
                host_in_pair,
                neighbor_is_host,
                neighbor_in_pair,
            ), count in sorted(blocked_pair_relations.items())
        },
        "eligible_bundle_shape_histogram": {
            ",".join(map(str, shape)): count for shape, count in sorted(shapes.items())
        },
        "hall_witness_type_histogram": {
            f"{size}:{neighbors}": count
            for (size, neighbors), count in sorted(witness_sizes.items())
        },
    }


def audit_profile(path: Path, max_states: int | None):
    document = json.loads(path.read_text())
    return audit_values(document["values"], str(path), sha256(path), max_states)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profiles", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-states", type=int)
    parser.add_argument("--corpus-record-limit", type=int)
    args = parser.parse_args()
    records = []
    for profile in args.profiles:
        document = json.loads(profile.read_text())
        if "values" in document:
            candidates = [(str(profile), sha256(profile), document["values"])]
        elif "records" in document:
            corpus_records = document["records"][: args.corpus_record_limit]
            candidates = [
                (
                    f"{profile}#records[{index}]",
                    corpus_record["value_sha256"],
                    corpus_record["values"],
                )
                for index, corpus_record in enumerate(corpus_records)
            ]
        else:
            raise ValueError(f"{profile} has neither values nor records")
        for source, source_hash, values in candidates:
            record = audit_values(values, source, source_hash, args.max_states)
            records.append(record)
            if record["pair_extraction_counterexample_found"]:
                break
        if records[-1]["pair_extraction_counterexample_found"]:
            break
    atomic_json(
        args.output,
        {
            "schema": SCHEMA,
            "claim_tested": (
                "Every eligible four-agent one-floater EFX state is radius-one "
                "Hall-completable, or some radius-one candidate partition has a "
                "two-agent Hall witness with exactly one neighbor."
            ),
            "profiles": records,
            "claim_survives_tested_profiles": not any(
                record["pair_extraction_counterexample_found"] for record in records
            ),
        },
    )


if __name__ == "__main__":
    main()
