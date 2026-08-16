#!/usr/bin/env python3
"""Factored QF_LRA master for a fixed-base radius-one Hall obstruction."""

from __future__ import annotations

import itertools

import z3

try:
    from .decide_partial_hall_radius_one import (
        bundle_value,
        candidate_partitions,
        eligible_constraints,
    )
except ImportError:
    from decide_partial_hall_radius_one import (
        bundle_value,
        candidate_partitions,
        eligible_constraints,
    )


def adjacency_constraints(row, partition, bundle):
    own = bundle_value(row, partition[bundle])
    constraints = []
    for target, target_bundle in enumerate(partition):
        if target == bundle:
            continue
        for removed in target_bundle:
            residual = tuple(good for good in target_bundle if good != removed)
            constraints.append(own >= bundle_value(row, residual))
    return tuple(constraints)


def hall_witnesses_by_size(partition_edges):
    """Return minimal deficient-set witnesses grouped by agent-set size."""
    agents = range(4)
    bundles = range(4)
    groups = []
    for deficient_size in range(1, 5):
        neighborhood_size = deficient_size - 1
        witnesses = []
        for deficient_agents in itertools.combinations(agents, deficient_size):
            for neighborhood in itertools.combinations(bundles, neighborhood_size):
                allowed = set(neighborhood)
                witnesses.append(
                    z3.And(
                        *(
                            z3.Not(partition_edges[agent][bundle])
                            for agent in deficient_agents
                            for bundle in bundles
                            if bundle not in allowed
                        )
                    )
                )
        groups.append(tuple(witnesses))
    return tuple(groups)


def minimal_hall_witnesses(partition_edges):
    """Return the minimal deficient-set witnesses for a 4-by-4 graph."""
    return tuple(
        witness
        for group in hall_witnesses_by_size(partition_edges)
        for witness in group
    )


def build_factored_master(timeout_ms, hall_encoding="matching"):
    n = 4
    m = 9
    floater = 8
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(m)]
        for agent in range(n)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    for row in values:
        solver.add(z3.Sum(row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(*eligible_constraints(values, base, floater))
    partitions = list(candidate_partitions(base, floater))
    edges = []
    for partition_index, move in enumerate(partitions):
        partition = move["partition"]
        partition_edges = []
        for agent in range(n):
            agent_edges = []
            for bundle in range(n):
                edge = z3.Bool(f"edge_{partition_index}_{agent}_{bundle}")
                solver.add(
                    edge
                    == z3.And(
                        *adjacency_constraints(values[agent], partition, bundle)
                    )
                )
                agent_edges.append(edge)
            partition_edges.append(tuple(agent_edges))
        partition_edges = tuple(partition_edges)
        edges.append(partition_edges)
        if hall_encoding == "matching":
            for matching in itertools.permutations(range(n)):
                solver.add(
                    z3.Or(
                        *(
                            z3.Not(partition_edges[agent][matching[agent]])
                            for agent in range(n)
                        )
                    )
                )
        elif hall_encoding == "witness":
            solver.add(
                z3.Or(
                    *(
                        witness
                        for group in hall_witnesses_by_size(partition_edges)[1:]
                        for witness in group
                    )
                )
            )
        else:
            raise ValueError(f"unsupported Hall encoding: {hall_encoding}")
    return solver, values, base, floater, partitions, tuple(edges)
