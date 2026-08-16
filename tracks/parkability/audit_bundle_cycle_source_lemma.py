#!/usr/bin/env python3
"""Audit the bundle-cycle improvement and source-host blocker lemmas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
except ImportError:
    import core
    import independent
    from anneal import atomic_json


SCHEMA = "bundle-cycle-source-lemma-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbolic_checks() -> tuple[dict, tuple[str, str, str]]:
    old_own, new_own, old_target, old_own_remainder, floater = z3.Reals(
        "old_own new_own old_target old_own_remainder floater"
    )
    weak = z3.SolverFor("QF_LRA")
    weak.add(
        old_own > 0,
        new_own >= old_own,
        old_target <= old_own,
        old_own_remainder <= old_own,
        floater <= old_own,
        z3.Or(
            new_own < old_target,
            new_own < old_own_remainder,
            new_own < floater,
        ),
    )
    weak_status = str(weak.check())
    if weak_status != "unsat":
        raise AssertionError("bundle-cycle EFX/floater implication failed")

    old = z3.Reals("old_0 old_1 old_2 old_3")
    new = z3.Reals("new_0 new_1 new_2 new_3")
    nash = z3.SolverFor("QF_NRA")
    nash.add(
        *(utility > 0 for utility in old),
        *(new[index] >= old[index] for index in range(4)),
        z3.Or(*(new[index] > old[index] for index in range(4))),
        z3.Not(z3.Product(*new) > z3.Product(*old)),
    )
    nash_status = str(nash.check())
    if nash_status != "unsat":
        raise AssertionError("bundle-cycle strict Nash increase failed")

    host_total, removed, blocker_floater, observer_own = z3.Reals(
        "host_total removed blocker_floater observer_own"
    )
    source = z3.SolverFor("QF_LRA")
    source.add(
        host_total >= 0,
        removed >= 0,
        blocker_floater >= 0,
        observer_own >= host_total,
        observer_own < host_total - removed + blocker_floater,
        z3.Not(blocker_floater > removed),
    )
    source_status = str(source.check())
    if source_status != "unsat":
        raise AssertionError("source-host blocker band failed")

    return (
        {
            "negated_bundle_cycle_efx_status": weak_status,
            "negated_strict_nash_increase_status": nash_status,
            "negated_source_host_floater_ranking_status": source_status,
            "solver": {
                "name": "z3",
                "version": z3.get_version_string(),
                "logics": ["QF_LRA", "QF_NRA"],
            },
        },
        (weak.to_smt2(), nash.to_smt2(), source.to_smt2()),
    )


def directed_cycles(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        cycle
        for length in range(2, n + 1)
        for cycle in itertools.permutations(range(n), length)
        if cycle[0] == min(cycle)
    )


def has_directed_cycle(n: int, edges: set[tuple[int, int]]) -> bool:
    for cycle in directed_cycles(n):
        if all(
            (cycle[index], cycle[(index + 1) % len(cycle)]) in edges
            for index in range(len(cycle))
        ):
            return True
    return False


def graph_source_audit() -> dict:
    n = 4
    possible = tuple(
        (left, right)
        for left in range(n)
        for right in range(n)
        if left != right
    )
    acyclic_count = 0
    for mask in range(1 << len(possible)):
        edges = {
            edge
            for index, edge in enumerate(possible)
            if mask & (1 << index)
        }
        if has_directed_cycle(n, edges):
            continue
        acyclic_count += 1
        sources = tuple(
            vertex
            for vertex in range(n)
            if not any(right == vertex for _, right in edges)
        )
        if not sources:
            raise AssertionError("an acyclic four-vertex graph lacked a source")
    return {
        "status": "EXHAUSTIVE_FOUR_VERTEX_DIGRAPH_AUDIT_PASSED",
        "irreflexive_digraph_count": 1 << len(possible),
        "acyclic_digraph_count": acyclic_count,
        "property": "every acyclic strict-envy digraph has an unenvied bundle",
    }


def bundle_value(
    values: tuple[tuple[int, ...], ...],
    bundle: tuple[int, ...] | list[int],
    observer: int,
) -> int:
    return sum(values[observer][good] for good in bundle)


def exhaustive_literal_audit() -> dict:
    n = 3
    m = 4
    cycles = directed_cycles(n)
    profile_count = 0
    eligible_base_count = 0
    cycle_premise_count = 0
    strict_cycle_count = 0
    for flat in itertools.product((1, 2), repeat=n * m):
        values = tuple(
            tuple(flat[agent * m:(agent + 1) * m])
            for agent in range(n)
        )
        profile_count += 1
        for floater in range(m):
            for base in core.iter_efx_bases(values, floater):
                owner = tuple(base["base_owner"])
                old_utilities = tuple(base["own_values"])
                if not all(
                    old_utilities[agent] >= values[agent][floater]
                    for agent in range(n)
                ):
                    continue
                eligible_base_count += 1
                bundles = tuple(tuple(bundle) for bundle in base["bundles"])
                for cycle in cycles:
                    successor_values = tuple(
                        bundle_value(
                            values,
                            bundles[cycle[(index + 1) % len(cycle)]],
                            agent,
                        )
                        for index, agent in enumerate(cycle)
                    )
                    if any(
                        successor < old_utilities[agent]
                        for agent, successor in zip(cycle, successor_values)
                    ):
                        continue
                    cycle_premise_count += 1
                    owner_map = {
                        cycle[(index + 1) % len(cycle)]: cycle[index]
                        for index in range(len(cycle))
                    }
                    rotated = tuple(
                        None if assigned is None else owner_map.get(assigned, assigned)
                        for assigned in owner
                    )
                    if not independent.is_removed_good_efx0(
                        values,
                        rotated,
                        floater,
                    ):
                        raise AssertionError(
                            (values, floater, owner, cycle, "EFX")
                        )
                    new_utilities = tuple(
                        bundle_value(
                            values,
                            tuple(
                                good
                                for good, assigned in enumerate(rotated)
                                if assigned == agent
                            ),
                            agent,
                        )
                        for agent in range(n)
                    )
                    if any(
                        new_utilities[agent] < values[agent][floater]
                        for agent in range(n)
                    ):
                        raise AssertionError("bundle cycle lost floater nonenvy")
                    old_nash = new_nash = 1
                    for old_utility, new_utility in zip(
                        old_utilities, new_utilities
                    ):
                        old_nash *= old_utility
                        new_nash *= new_utility
                    if new_nash < old_nash:
                        raise AssertionError("bundle cycle reduced Nash welfare")
                    if any(
                        successor > old_utilities[agent]
                        for agent, successor in zip(cycle, successor_values)
                    ):
                        strict_cycle_count += 1
                        if new_nash <= old_nash:
                            raise AssertionError(
                                "strict bundle cycle failed to increase Nash"
                            )
    if not cycle_premise_count or not strict_cycle_count:
        raise AssertionError("literal grid did not exercise cycle cases")
    return {
        "status": "EXHAUSTIVE_LITERAL_AUDIT_PASSED",
        "n": n,
        "m": m,
        "value_domain": [1, 2],
        "profile_count": profile_count,
        "eligible_base_count": eligible_base_count,
        "directed_cycle_count": len(cycles),
        "cycle_premise_count": cycle_premise_count,
        "strict_cycle_count": strict_cycle_count,
        "verifier": "independent literal removed-good EFX expansion",
    }


def run(
    output: Path,
    weak_smt2: Path,
    nash_smt2: Path,
    source_smt2: Path,
) -> dict:
    symbolic, formulas = symbolic_checks()
    paths = (weak_smt2, nash_smt2, source_smt2)
    for path, formula in zip(paths, formulas):
        path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": "PROVED_BUNDLE_CYCLE_AND_SOURCE_HOST_REDUCTION",
        "bundle_cycle_lemma": (
            "Rotating bundles around a cycle of agents that each weakly prefer "
            "the next bundle preserves EFX and floater nonenvy; if one "
            "preference is strict, Nash welfare strictly increases."
        ),
        "source_host_corollary": (
            "The strict-envy graph of a maximum-Nash eligible state is acyclic. "
            "It has an unenvied host bundle. If floater insertion at that host "
            "is blocked, every blocking removed-good witness uses an old host "
            "good that the observer values strictly below the floater."
        ),
        "symbolic": symbolic,
        "literal": exhaustive_literal_audit(),
        "graph": graph_source_audit(),
        "formulas": [
            {"path": path.name, "sha256": sha256(path)} for path in paths
        ],
        "claim_boundary": (
            "The reduction forces a floater-support edge but does not yet prove "
            "that repeated support edges close into an improving exchange."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--weak-smt2", type=Path, required=True)
    parser.add_argument("--nash-smt2", type=Path, required=True)
    parser.add_argument("--source-smt2", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.output,
        args.weak_smt2,
        args.nash_smt2,
        args.source_smt2,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
