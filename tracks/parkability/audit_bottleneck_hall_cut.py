#!/usr/bin/env python3
"""Exhaustively audit the bottleneck Hall-cut normal form on small graphs."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "bottleneck-hall-cut-audit-v1"


def neighborhood(rows: tuple[int, ...], agents: int) -> int:
    result = 0
    for agent, row in enumerate(rows):
        if agents & (1 << agent):
            result |= row
    return result


def is_matching(rows: tuple[int, ...], permutation: tuple[int, ...]) -> bool:
    return all(rows[agent] & (1 << bundle) for agent, bundle in enumerate(permutation))


def subset_has_matching(rows: tuple[int, ...], agents: int, bundles: int) -> bool:
    agent_list = [agent for agent in range(len(rows)) if agents & (1 << agent)]
    bundle_list = [bundle for bundle in range(len(rows)) if bundles & (1 << bundle)]
    if len(agent_list) != len(bundle_list):
        return False
    return any(
        all(rows[agent] & (1 << bundle) for agent, bundle in zip(agent_list, image))
        for image in itertools.permutations(bundle_list)
    )


def minimal_deficient_sets(rows: tuple[int, ...]) -> tuple[int, ...]:
    n = len(rows)
    deficient = []
    for agents in range(1, 1 << n):
        if neighborhood(rows, agents).bit_count() >= agents.bit_count():
            continue
        if any((prior & agents) == prior for prior in deficient):
            continue
        deficient.append(agents)
    return tuple(deficient)


def audit(n: int) -> dict:
    full = (1 << n) - 1
    permutations = tuple(itertools.permutations(range(n)))
    strict_graph_count = 0
    witness_count = 0
    full_witness_count = 0
    weak_matching_checks = 0
    residual_factorization_count = 0
    residual_expansion_count = 0

    for encoded in range(1 << (n * n)):
        rows = tuple((encoded >> (agent * n)) & full for agent in range(n))
        if any(is_matching(rows, permutation) for permutation in permutations):
            continue
        strict_graph_count += 1
        witnesses = minimal_deficient_sets(rows)
        if not witnesses:
            raise AssertionError("nonmatchable graph has no minimal Hall witness")
        for agents in witnesses:
            witness_count += 1
            size = agents.bit_count()
            neighbors = neighborhood(rows, agents)
            if neighbors.bit_count() != size - 1:
                raise AssertionError("minimal Hall witness has wrong deficiency")
            for removed in range(n):
                if not agents & (1 << removed):
                    continue
                remainder = agents & ~(1 << removed)
                if not any(
                    all(
                        not remainder & (1 << agent)
                        or rows[agent] & (1 << permutation[agent])
                        for agent in range(n)
                    )
                    for permutation in permutations
                ):
                    raise AssertionError("proper witness subset lacks strict matching")

            # It suffices to audit each possible weak perfect matching: every
            # weak supergraph contains at least one such matching.
            for permutation in permutations:
                weak_matching_checks += 1
                crossing = [
                    agent
                    for agent in range(n)
                    if agents & (1 << agent)
                    and not neighbors & (1 << permutation[agent])
                ]
                if not crossing:
                    raise AssertionError("weak matching does not cross critical cut")
                weak_rows = tuple(
                    row | (1 << permutation[agent])
                    for agent, row in enumerate(rows)
                )
                outside_agents = full & ~agents
                outside_bundles = full & ~neighbors
                for crossing_agent in crossing:
                    residual_agents = outside_agents | (1 << crossing_agent)
                    if subset_has_matching(
                        weak_rows, residual_agents, outside_bundles
                    ):
                        residual_factorization_count += 1
                        continue
                    residual_expansion_count += 1
                    residual_witness = next(
                        subset
                        for subset in range(1, 1 << n)
                        if (subset & ~residual_agents) == 0
                        and (
                            neighborhood(weak_rows, subset) & outside_bundles
                        ).bit_count()
                        < subset.bit_count()
                    )
                    added_agents = residual_witness & outside_agents
                    if not added_agents:
                        raise AssertionError(
                            "residual obstruction does not expand deficient set"
                        )
                    expanded = agents | added_agents
                    if neighborhood(rows, expanded).bit_count() >= expanded.bit_count():
                        raise AssertionError(
                            "residual obstruction does not induce strict expansion"
                        )

            if agents == full:
                full_witness_count += 1
                missing = full & ~neighbors
                if missing.bit_count() != 1:
                    raise AssertionError("full witness does not miss one bundle")
                if not any(
                    sum(not (rows[a] & (1 << permutation[a])) for a in range(n)) == 1
                    and any(
                        permutation[a] == missing.bit_length() - 1
                        and not (rows[a] & (1 << permutation[a]))
                        for a in range(n)
                    )
                    for permutation in permutations
                ):
                    raise AssertionError("full witness lacks one-equality normal form")

    return {
        "schema": SCHEMA,
        "status": "EXHAUSTIVE_AUDIT_PASSED",
        "meaning": (
            "Exhaustive unlabeled-edge audit of every strict bipartite graph "
            f"on {n}+{n} vertices without a perfect matching."
        ),
        "n": n,
        "strict_graph_count": strict_graph_count,
        "minimal_witness_count": witness_count,
        "full_witness_count": full_witness_count,
        "weak_matching_checks": weak_matching_checks,
        "residual_factorization_count": residual_factorization_count,
        "residual_expansion_count": residual_expansion_count,
        "claim_boundary": (
            "This audits the graph normal form, not the valuation-dependent "
            "exchange needed for EFX completion."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(1, 2, 3, 4), default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    result = audit(args.n)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
