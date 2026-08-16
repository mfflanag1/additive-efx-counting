#!/usr/bin/env python3
"""Census connected transfer graphs among exact eligible EFX improvers."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states, profile_records
except ImportError:
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states, profile_records


BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8


def owner_vector(masks: tuple[int, ...], floater: int) -> tuple[int, ...]:
    owners = [-1] * 9
    for owner, mask in enumerate(masks):
        for good in range(9):
            if mask & (1 << good):
                owners[good] = owner
    owners[floater] = -1
    return tuple(owners)


def transfers(
    base: tuple[int, ...], target: tuple[int, ...]
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (good, base[good], target[good])
        for good in range(9)
        if base[good] != target[good]
    )


def component_count(edges: tuple[tuple[int, int, int], ...]) -> int:
    adjacency: dict[int, set[int]] = {}
    for _, source, destination in edges:
        adjacency.setdefault(source, set()).add(destination)
        adjacency.setdefault(destination, set()).add(source)
    unseen = set(adjacency)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return count


def transfer_components(
    edges: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    adjacency: dict[int, set[int]] = {}
    for _, source, destination in edges:
        adjacency.setdefault(source, set()).add(destination)
        adjacency.setdefault(destination, set()).add(source)
    unseen = set(adjacency)
    components = []
    while unseen:
        vertices = {unseen.pop()}
        stack = list(vertices)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    vertices.add(neighbor)
                    stack.append(neighbor)
        components.append(
            tuple(
                good
                for good, source, destination in edges
                if source in vertices and destination in vertices
            )
        )
    return tuple(sorted(components))


def owners_key(owners: tuple[int, ...]) -> tuple[int, tuple[int, ...]] | None:
    if owners.count(-1) != 1:
        return None
    masks = tuple(
        sum(1 << good for good, owner in enumerate(owners) if owner == agent)
        for agent in range(4)
    )
    if any(mask == 0 for mask in masks):
        return None
    return owners.index(-1), masks


def component_state_properties(
    values: tuple[tuple[int, ...], ...], owners: tuple[int, ...]
) -> tuple[bool, bool]:
    floater = owners.index(-1)
    bundles = tuple(
        tuple(good for good, owner in enumerate(owners) if owner == agent)
        for agent in range(4)
    )
    efx = True
    parked = True
    for agent in range(4):
        own = sum(values[agent][good] for good in bundles[agent])
        parked &= own >= values[agent][floater]
        for target in range(4):
            if target == agent:
                continue
            for removed in bundles[target]:
                residual = sum(
                    values[agent][good]
                    for good in bundles[target]
                    if good != removed
                )
                efx &= own >= residual
    return efx, parked


def first_efx_violation(
    values: tuple[tuple[int, ...], ...], owners: tuple[int, ...]
) -> dict | None:
    bundles = tuple(
        tuple(good for good, owner in enumerate(owners) if owner == agent)
        for agent in range(4)
    )
    for agent in range(4):
        own = sum(values[agent][good] for good in bundles[agent])
        for target in range(4):
            if target == agent:
                continue
            for removed in bundles[target]:
                residual = sum(
                    values[agent][good]
                    for good in bundles[target]
                    if good != removed
                )
                if own < residual:
                    return {
                        "agent": agent,
                        "target": target,
                        "removed_good": removed,
                        "own_value": own,
                        "residual_value": residual,
                    }
    return None


def has_directed_cycle(edges: list[tuple[int, int]], vertex_count: int) -> bool:
    adjacency = {vertex: [] for vertex in range(vertex_count)}
    for source, destination in edges:
        adjacency[source].append(destination)
    for start in range(vertex_count):
        stack = [(start, frozenset())]
        while stack:
            vertex, path = stack.pop()
            if vertex in path:
                return True
            next_path = path | {vertex}
            stack.extend((neighbor, next_path) for neighbor in adjacency[vertex])
    return False


def shortest_directed_cycle_length(
    edges: list[tuple[int, int]], vertex_count: int
) -> int | None:
    adjacency = {vertex: [] for vertex in range(vertex_count)}
    for source, destination in edges:
        adjacency[source].append(destination)
    best = None
    for start in range(vertex_count):
        queue = [(start, 0)]
        seen = {start: 0}
        while queue:
            vertex, distance = queue.pop(0)
            for neighbor in adjacency[vertex]:
                if neighbor == start:
                    length = distance + 1
                    best = length if best is None else min(best, length)
                elif neighbor not in seen:
                    seen[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))
    return best


def public_fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def state_record(
    state: dict,
    base_owner: tuple[int, ...],
    gain: Fraction,
) -> dict:
    target_owner = owner_vector(state["masks"], state["floater"])
    edges = transfers(base_owner, target_owner)
    indegree = {vertex: 0 for vertex in range(-1, 4)}
    outdegree = {vertex: 0 for vertex in range(-1, 4)}
    for _, source, destination in edges:
        outdegree[source] += 1
        indegree[destination] += 1
    vertices = {endpoint for _, source, destination in edges for endpoint in (source, destination)}
    components = component_count(edges)
    return {
        "owner_distance": len(edges),
        "component_count": components,
        "transfer_vertex_count": len(vertices),
        "cycle_rank": len(edges) - len(vertices) + components,
        "floater": state["floater"],
        "masks": list(state["masks"]),
        "utilities": list(state["utilities"]),
        "potential_gain": public_fraction(gain),
        "transfers": [
            {"good": good, "source": source, "destination": destination}
            for good, source, destination in edges
        ],
        "indegree": {str(vertex): indegree[vertex] for vertex in range(-1, 4)},
        "outdegree": {str(vertex): outdegree[vertex] for vertex in range(-1, 4)},
    }


def run(paths: list[Path], output: Path) -> dict:
    base_owner = owner_vector(BASE_MASKS, BASE_FLOATER)
    records = []
    for path in paths:
        profiles = profile_records(path)
        if len(profiles) != 1:
            raise AssertionError(f"expected one primary profile in {path}")
        values = profiles[0]["values"]
        row_totals = tuple(map(sum, values))
        base_utilities = tuple(
            sum(values[agent][good] for good in range(9) if BASE_MASKS[agent] & (1 << good))
            for agent in range(4)
        )
        base_score = sum(
            (Fraction(base_utilities[agent], row_totals[agent]) for agent in range(4)),
            Fraction(),
        )
        states = enumerate_states(values)
        eligible = {
            (state["floater"], tuple(state["masks"])): state for state in states
        }
        improving = []
        connected = []
        disconnected_count = 0
        component_reducible_count = 0
        first_component_irreducible = None
        positive_component_failure_histogram: dict[str, int] = {}
        all_component_efx_failure_count = 0
        dependency_cycle_length_histogram: dict[str, int] = {}
        all_failure_gain_pattern_histogram: dict[str, int] = {}
        all_component_efx_failure_records = []
        component_histogram: dict[str, int] = {}
        connected_cycle_rank_histogram: dict[str, int] = {}
        for state in states:
            gain = sum(state["normalized"], Fraction()) - base_score
            if gain <= 0:
                continue
            record = state_record(state, base_owner, gain)
            improving.append(record)
            key = str(record["component_count"])
            component_histogram[key] = component_histogram.get(key, 0) + 1
            if record["component_count"] == 1:
                connected.append(record)
                rank = str(record["cycle_rank"])
                connected_cycle_rank_histogram[rank] = (
                    connected_cycle_rank_histogram.get(rank, 0) + 1
                )
            else:
                disconnected_count += 1
                target_owner = owner_vector(state["masks"], state["floater"])
                edges = transfers(base_owner, target_owner)
                components = transfer_components(edges)
                vertex_component = {}
                for component_index, goods in enumerate(components):
                    for good, source, destination in edges:
                        if good in goods:
                            vertex_component[source] = component_index
                            vertex_component[destination] = component_index
                positive_components = []
                component_checks = []
                component_gain_sum = Fraction()
                dependency_edges = []
                for component_index, goods in enumerate(components):
                    component_vertices = sorted(
                        {
                            endpoint
                            for good, source, destination in edges
                            if good in goods
                            for endpoint in (source, destination)
                        }
                    )
                    intermediate = list(base_owner)
                    for good in goods:
                        intermediate[good] = target_owner[good]
                    key = owners_key(tuple(intermediate))
                    if key is None:
                        raise AssertionError("a transfer component is not a valid state")
                    component_state = eligible.get(key) if key is not None else None
                    component_efx, component_parked = component_state_properties(
                        values, tuple(intermediate)
                    )
                    violation = (
                        None
                        if component_efx
                        else first_efx_violation(values, tuple(intermediate))
                    )
                    if violation is not None:
                        agent_component = vertex_component.get(violation["agent"])
                        target_component = vertex_component.get(violation["target"])
                        if (
                            agent_component is None
                            or target_component is None
                            or agent_component == target_component
                            or component_index
                            not in {agent_component, target_component}
                        ):
                            raise AssertionError(
                                "component EFX failure is not cross-component"
                            )
                        dependency = (
                            target_component
                            if agent_component == component_index
                            else agent_component
                        )
                        dependency_edges.append((component_index, dependency))
                        violation = {
                            **violation,
                            "agent_component": agent_component,
                            "target_component": target_component,
                            "dependency_component": dependency,
                        }
                    component_utilities = tuple(
                        sum(
                            values[agent][good]
                            for good, owner in enumerate(intermediate)
                            if owner == agent
                        )
                        for agent in range(4)
                    )
                    component_gain = sum(
                        (
                            Fraction(component_utilities[agent], row_totals[agent])
                            for agent in range(4)
                        ),
                        Fraction(),
                    ) - base_score
                    component_gain_sum += component_gain
                    check = {
                        "goods": list(goods),
                        "vertices": component_vertices,
                        "valid_one_floater_state": key is not None,
                        "partial_efx": component_efx,
                        "floater_nonenvy": component_parked,
                        "eligible_partial_efx": component_state is not None,
                        "first_efx_violation": violation,
                        "utilities": list(component_utilities),
                        "potential_gain": public_fraction(component_gain),
                    }
                    component_checks.append(check)
                    if component_state is not None and component_gain > 0:
                        positive_components.append(
                            {
                                "goods": list(goods),
                                "potential_gain": public_fraction(component_gain),
                                "floater": component_state["floater"],
                                "masks": list(component_state["masks"]),
                            }
                        )
                    elif component_gain > 0:
                        failure = (
                            "efx_and_floater_nonenvy"
                            if not component_efx and not component_parked
                            else "efx"
                            if not component_efx
                            else "floater_nonenvy"
                        )
                        positive_component_failure_histogram[failure] = (
                            positive_component_failure_histogram.get(failure, 0) + 1
                        )
                if component_gain_sum != gain:
                    raise AssertionError("component gains do not sum to total gain")
                if all(not check["partial_efx"] for check in component_checks):
                    all_component_efx_failure_count += 1
                    positive_count = sum(
                        check["potential_gain"]["numerator"] > 0
                        for check in component_checks
                    )
                    gain_pattern = (
                        f"{len(components)}_components_{positive_count}_positive"
                    )
                    all_failure_gain_pattern_histogram[gain_pattern] = (
                        all_failure_gain_pattern_histogram.get(gain_pattern, 0) + 1
                    )
                    if not has_directed_cycle(dependency_edges, len(components)):
                        raise AssertionError("component dependencies have no cycle")
                    cycle_length = shortest_directed_cycle_length(
                        dependency_edges, len(components)
                    )
                    if cycle_length is None:
                        raise AssertionError("dependency cycle length is missing")
                    cycle_key = str(cycle_length)
                    dependency_cycle_length_histogram[cycle_key] = (
                        dependency_cycle_length_histogram.get(cycle_key, 0) + 1
                    )
                    splices = []
                    if len(components) == 2:
                        for left_good in components[0]:
                            for right_good in components[1]:
                                splice_owner = list(target_owner)
                                splice_owner[left_good] = target_owner[right_good]
                                splice_owner[right_good] = target_owner[left_good]
                                splice_key = owners_key(tuple(splice_owner))
                                if splice_key is None:
                                    continue
                                splice_edges = transfers(base_owner, tuple(splice_owner))
                                splice_state = eligible.get(splice_key)
                                splice_utilities = tuple(
                                    sum(
                                        values[agent][good]
                                        for good, owner in enumerate(splice_owner)
                                        if owner == agent
                                    )
                                    for agent in range(4)
                                )
                                splice_gain = sum(
                                    (
                                        Fraction(
                                            splice_utilities[agent],
                                            row_totals[agent],
                                        )
                                        for agent in range(4)
                                    ),
                                    Fraction(),
                                ) - base_score
                                splices.append(
                                    {
                                        "left_good": left_good,
                                        "right_good": right_good,
                                        "connected": component_count(splice_edges) == 1,
                                        "eligible_partial_efx": splice_state is not None,
                                        "improving": splice_gain > 0,
                                        "potential_gain": public_fraction(splice_gain),
                                        "floater": splice_key[0],
                                        "masks": list(splice_key[1]),
                                    }
                                )
                    successful_splices = [
                        splice
                        for splice in splices
                        if splice["connected"]
                        and splice["eligible_partial_efx"]
                        and splice["improving"]
                    ]
                    splice_outcomes: dict[str, int] = {}
                    for splice in splices:
                        outcome = (
                            "disconnected"
                            if not splice["connected"]
                            else "connected_ineligible"
                            if not splice["eligible_partial_efx"]
                            else "connected_eligible_nonimproving"
                            if not splice["improving"]
                            else "connected_eligible_improving"
                        )
                        splice_outcomes[outcome] = splice_outcomes.get(outcome, 0) + 1
                    reroutes = []
                    for good in range(9):
                        for destination in range(-1, 4):
                            if destination == target_owner[good]:
                                continue
                            reroute_owner = list(target_owner)
                            reroute_owner[good] = destination
                            reroute_key = owners_key(tuple(reroute_owner))
                            if reroute_key is None:
                                continue
                            reroute_edges = transfers(base_owner, tuple(reroute_owner))
                            reroute_state = eligible.get(reroute_key)
                            reroute_gain = (
                                sum(reroute_state["normalized"], Fraction()) - base_score
                                if reroute_state is not None
                                else None
                            )
                            reroutes.append(
                                {
                                    "good": good,
                                    "destination": destination,
                                    "connected": component_count(reroute_edges) == 1,
                                    "eligible_partial_efx": reroute_state is not None,
                                    "improving": (
                                        reroute_gain is not None and reroute_gain > 0
                                    ),
                                    "potential_gain": (
                                        public_fraction(reroute_gain)
                                        if reroute_gain is not None
                                        else None
                                    ),
                                    "floater": reroute_key[0],
                                    "masks": list(reroute_key[1]),
                                }
                            )
                    successful_reroutes = [
                        reroute
                        for reroute in reroutes
                        if reroute["connected"]
                        and reroute["eligible_partial_efx"]
                        and reroute["improving"]
                    ]
                    all_component_efx_failure_records.append(
                        {
                            "rival": record,
                            "components": component_checks,
                            "dependency_edges": [
                                {"source": source, "destination": destination}
                                for source, destination in dependency_edges
                            ],
                            "shortest_dependency_cycle_length": cycle_length,
                            "two_edge_splice_count": len(splices),
                            "successful_two_edge_splice_count": len(
                                successful_splices
                            ),
                            "two_edge_splice_outcome_histogram": dict(
                                sorted(splice_outcomes.items())
                            ),
                            "best_successful_two_edge_splice": max(
                                successful_splices,
                                key=lambda splice: Fraction(
                                    splice["potential_gain"]["numerator"],
                                    splice["potential_gain"]["denominator"],
                                ),
                                default=None,
                            ),
                            "successful_one_good_reroute_count": len(
                                successful_reroutes
                            ),
                            "best_successful_one_good_reroute": max(
                                successful_reroutes,
                                key=lambda reroute: Fraction(
                                    reroute["potential_gain"]["numerator"],
                                    reroute["potential_gain"]["denominator"],
                                ),
                                default=None,
                            ),
                        }
                    )
                if positive_components:
                    component_reducible_count += 1
                elif first_component_irreducible is None:
                    first_component_irreducible = {
                        "rival": record,
                        "component_checks": component_checks,
                    }
        if not improving:
            raise AssertionError(f"{path} has no improving eligible EFX state")
        order = lambda item: (
            item["owner_distance"],
            -Fraction(
                item["potential_gain"]["numerator"],
                item["potential_gain"]["denominator"],
            ),
            item["floater"],
            item["masks"],
        )
        improving.sort(key=order)
        connected.sort(key=order)
        for failure in all_component_efx_failure_records:
            rival = failure["rival"]
            rival_owner = owner_vector(
                tuple(rival["masks"]), rival["floater"]
            )
            bridged = min(
                connected,
                key=lambda item: (
                    sum(
                        left != right
                        for left, right in zip(
                            rival_owner,
                            owner_vector(tuple(item["masks"]), item["floater"]),
                        )
                    ),
                    order(item),
                ),
            )
            bridge_owner = owner_vector(
                tuple(bridged["masks"]), bridged["floater"]
            )
            failure["nearest_connected_bridge"] = {
                "owner_distance_from_disconnected_rival": sum(
                    left != right
                    for left, right in zip(rival_owner, bridge_owner)
                ),
                "connected_rival": bridged,
            }
        records.append(
            {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "eligible_efx_improver_count": len(improving),
                "connected_improver_count": len(connected),
                "disconnected_improver_count": disconnected_count,
                "component_reducible_disconnected_improver_count": (
                    component_reducible_count
                ),
                "first_component_irreducible_disconnected_improver": (
                    first_component_irreducible
                ),
                "positive_component_failure_histogram": dict(
                    sorted(positive_component_failure_histogram.items())
                ),
                "all_component_efx_failure_disconnected_improver_count": (
                    all_component_efx_failure_count
                ),
                "dependency_cycle_length_histogram": dict(
                    sorted(dependency_cycle_length_histogram.items())
                ),
                "all_failure_gain_pattern_histogram": dict(
                    sorted(all_failure_gain_pattern_histogram.items())
                ),
                "all_component_efx_failure_records": (
                    all_component_efx_failure_records
                ),
                "component_count_histogram": dict(sorted(component_histogram.items())),
                "connected_cycle_rank_histogram": dict(
                    sorted(connected_cycle_rank_histogram.items())
                ),
                "nearest_improver": improving[0],
                "nearest_connected_improver": connected[0] if connected else None,
            }
        )
    artifact = {
        "schema": "partial-hall-augmenting-exchange-topology-audit-v1",
        "status": "AUDITED",
        "meaning": (
            "Finite-profile census of normalized-utilitarian-improving eligible "
            "one-floater EFX states, classified by weak connectivity of their "
            "changed-good transfer graph. This is hypothesis evidence, not a cover."
        ),
        "base_masks": list(BASE_MASKS),
        "base_floater": BASE_FLOATER,
        "profile_count": len(records),
        "all_profiles_have_connected_improver": all(
            record["nearest_connected_improver"] is not None for record in records
        ),
        "component_potential_decomposition_verified": True,
        "component_efx_failure_localization_verified": True,
        "records": records,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
