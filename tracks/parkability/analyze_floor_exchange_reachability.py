#!/usr/bin/env python3
"""Analyze reachability of EFX by local exchanges from owner-floor states."""

from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import (
        FAVORITE,
        balanced_state_universe,
    )
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import (
        FAVORITE,
        balanced_state_universe,
    )


SCHEMA = "floor-exchange-reachability-analysis-v1"
N = 4

Allocation = tuple[tuple[int, ...], ...]


def bundle_value(row: tuple[int, ...], bundle: tuple[int, ...]) -> int:
    return sum(row[good] for good in bundle)


def is_floor(values: tuple[tuple[int, ...], ...], allocation: Allocation) -> bool:
    return all(
        bundle_value(values[agent], allocation[agent])
        >= values[agent][FAVORITE]
        for agent in range(N)
    )


def is_efx(values: tuple[tuple[int, ...], ...], allocation: Allocation) -> bool:
    for observer in range(N):
        own = bundle_value(values[observer], allocation[observer])
        for target in range(N):
            if target == observer:
                continue
            bundle = allocation[target]
            if any(
                bundle_value(
                    values[observer],
                    tuple(good for good in bundle if good != removed),
                )
                > own
                for removed in bundle
            ):
                return False
    return True


def floor_allocations(
    values: tuple[tuple[int, ...], ...],
) -> tuple[Allocation, ...]:
    allocations = []
    for partition in balanced_state_universe():
        for triple_owner in range(N):
            triple = next(bundle for bundle in partition if len(bundle) == 3)
            pairs = tuple(bundle for bundle in partition if len(bundle) == 2)
            other_agents = tuple(
                agent for agent in range(N) if agent != triple_owner
            )
            for pair_order in itertools.permutations(pairs):
                by_agent = [()] * N
                by_agent[triple_owner] = triple
                for agent, pair in zip(other_agents, pair_order):
                    by_agent[agent] = pair
                allocation = tuple(by_agent)
                if is_floor(values, allocation):
                    allocations.append(allocation)
    return tuple(allocations)


def exchange_successors(
    values: tuple[tuple[int, ...], ...],
    allocation: Allocation,
) -> tuple[Allocation, ...]:
    host = next(agent for agent, bundle in enumerate(allocation) if len(bundle) == 3)
    triple = allocation[host]
    successors = set()
    for envier in range(N):
        if envier == host:
            continue
        own_bundle = allocation[envier]
        own_value = bundle_value(values[envier], own_bundle)
        for leftover in triple:
            desired_pair = tuple(good for good in triple if good != leftover)
            if bundle_value(values[envier], desired_pair) <= own_value:
                continue

            host_absorption = tuple(sorted(own_bundle + (leftover,)))
            if (
                bundle_value(values[host], host_absorption)
                >= values[host][FAVORITE]
            ):
                successor = list(allocation)
                successor[envier] = tuple(sorted(desired_pair))
                successor[host] = host_absorption
                successors.add(tuple(successor))

            if (
                bundle_value(values[host], desired_pair)
                >= values[host][FAVORITE]
            ):
                successor = list(allocation)
                successor[host] = tuple(sorted(desired_pair))
                successor[envier] = host_absorption
                successors.add(tuple(successor))
    return tuple(sorted(successors))


def load_values(path: Path) -> tuple[tuple[int, ...], ...]:
    source = json.loads(path.read_text())
    raw = source.get("values")
    if raw is None:
        raw = source["trace"][0]["values"]
    return tuple(tuple(row) for row in raw)


def analyze_profile(path: Path) -> dict:
    values = load_values(path)
    allocations = floor_allocations(values)
    allocation_set = set(allocations)
    efx = {allocation for allocation in allocations if is_efx(values, allocation)}
    predecessors: dict[Allocation, list[Allocation]] = collections.defaultdict(list)
    edge_count = 0
    missing_successor_count = 0
    sink_non_efx = []
    for allocation in allocations:
        successors = exchange_successors(values, allocation)
        if not successors and allocation not in efx:
            sink_non_efx.append(allocation)
        for successor in successors:
            if successor not in allocation_set:
                missing_successor_count += 1
                continue
            predecessors[successor].append(allocation)
            edge_count += 1

    reachable = set(efx)
    queue = collections.deque(efx)
    while queue:
        state = queue.popleft()
        for predecessor in predecessors[state]:
            if predecessor not in reachable:
                reachable.add(predecessor)
                queue.append(predecessor)
    trapped = tuple(allocation for allocation in allocations if allocation not in reachable)
    favorite_pair_starts = tuple(
        allocation
        for allocation in allocations
        if len(next(bundle for bundle in allocation if FAVORITE in bundle)) == 2
    )
    trapped_starts = tuple(
        allocation for allocation in favorite_pair_starts if allocation not in reachable
    )
    return {
        "source": str(path.resolve()),
        "values": [list(row) for row in values],
        "floor_allocation_count": len(allocations),
        "favorite_pair_floor_start_count": len(favorite_pair_starts),
        "efx_floor_allocation_count": len(efx),
        "exchange_edge_count": edge_count,
        "missing_successor_count": missing_successor_count,
        "non_efx_sink_count": len(sink_non_efx),
        "efx_reachable_floor_count": len(reachable),
        "trapped_floor_count": len(trapped),
        "trapped_favorite_pair_start_count": len(trapped_starts),
        "first_non_efx_sink": (
            [list(bundle) for bundle in sink_non_efx[0]]
            if sink_non_efx
            else None
        ),
        "first_trapped_favorite_pair_start": (
            [list(bundle) for bundle in trapped_starts[0]]
            if trapped_starts
            else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profiles = [analyze_profile(path) for path in args.source]
    result = {
        "schema": SCHEMA,
        "profiles": profiles,
        "claim": (
            "Exact finite-state analysis of whether the two direct "
            "triple-envy exchanges can reach an EFX owner-floor allocation. "
            "This is diagnostic evidence, not a universal theorem."
        ),
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
