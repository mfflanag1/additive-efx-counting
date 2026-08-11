#!/usr/bin/env python3
"""Decide connected at-most-three-good later-owner flower transfers."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict, deque
from pathlib import Path

import z3

try:
    from .analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        RECIPIENTS,
        old_bundles,
        solve_at_radius,
        transfer_topology,
        validate,
    )
    from .decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        RECIPIENTS,
        old_bundles,
        solve_at_radius,
        transfer_topology,
        validate,
    )
    from decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )


def connected(edges: tuple[tuple[str, str], ...]) -> bool:
    adjacency = defaultdict(set)
    for source, target in edges:
        adjacency[source].add(target)
        adjacency[target].add(source)
    if not adjacency:
        return False
    root = next(iter(adjacency))
    seen = {root}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(adjacency)


def base_allocation(old):
    allocation = {agent: list(old[agent]) for agent in AGENTS}
    allocation["_"] = ["f"]
    return allocation


def allocation_key(allocation):
    return tuple(tuple(sorted(allocation[recipient])) for recipient in RECIPIENTS)


def moved_allocation(base, moves):
    allocation = {recipient: list(goods) for recipient, goods in base.items()}
    for good, source, target in moves:
        allocation[source].remove(good)
        allocation[target].append(good)
    return {recipient: sorted(goods) for recipient, goods in allocation.items()}


def enumerate_connected(old, radius=3, rooted=False):
    base = base_allocation(old)
    base_owner = {
        good: recipient for recipient, goods in base.items() for good in goods
    }
    goods = tuple(sorted(base_owner))
    allocations = {}
    for count in range(1, radius + 1):
        for selected in itertools.combinations(goods, count):
            sources = tuple(base_owner[good] for good in selected)
            choices = tuple(
                tuple(recipient for recipient in RECIPIENTS if recipient != source)
                for source in sources
            )
            for targets in itertools.product(*choices):
                moves = tuple(zip(selected, sources, targets))
                edges = tuple((source, target) for _, source, target in moves)
                if not connected(edges):
                    continue
                incoming = {target for _, target in edges}
                outgoing = {source for source, _ in edges}
                # Positivity makes these necessary for the required utility
                # signs, independently of the cardinal values.
                if "q" not in incoming:
                    continue
                if "r" in outgoing and "r" not in incoming:
                    continue
                if "s" in outgoing and "s" not in incoming:
                    continue
                if rooted:
                    if count < 2 or ("f", "_", "q") not in moves:
                        continue
                    if not any(source == "q" and target == "_" for _, source, target in moves):
                        continue
                allocation = moved_allocation(base, moves)
                allocations[allocation_key(allocation)] = allocation
    return tuple(allocations.values())


def completion_formula(allocation, old, value, base):
    base_allocation = base_allocation_for(old)
    changed = {
        recipient
        for recipient in RECIPIENTS
        if tuple(allocation[recipient]) != tuple(sorted(base_allocation[recipient]))
    }
    own = {
        agent: z3.Sum(*(value[good, agent] for good in allocation[agent]))
        for agent in AGENTS
    }
    conditions = [own["r"] >= base["r"], own["q"] > base["q"]]
    for observer in AGENTS:
        for target in AGENTS:
            if observer in changed or target in changed:
                conditions.append(own[observer] >= true_tail([
                    value[good, observer] for good in allocation[target]
                ]))
        if observer in changed or "_" in changed:
            conditions.append(
                own[observer]
                >= z3.Sum(*(value[good, observer] for good in allocation["_"]))
            )
    return z3.And(*conditions)


def base_allocation_for(old):
    return {
        **{agent: sorted(old[agent]) for agent in AGENTS},
        "_": ["f"],
    }


def run(radius=3, rooted=False, maximum_escape_radius=6):
    solver, atoms, old, value, base = build_master()
    allocations = enumerate_connected(old, radius=radius, rooted=rooted)
    for allocation in allocations:
        solver.add(z3.Not(completion_formula(allocation, old, value, base)))
    checked = solver.check()
    result = {
        "schema": "flexible-later-owner-connected-transfer-gate-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "radius": radius,
        "rooted_at_selected_replacement": rooted,
        "candidate_allocation_count": len(allocations),
        "claim_boundary": (
            "bounded two-atom representative full-capture flower decision; "
            "UNSAT excludes a valuation blocking every listed connected transfer "
            "but does not by itself prove the arbitrary-packet flower lemma"
        ),
    }
    if checked == z3.sat:
        model = solver.model()
        values = fractions(model, atoms, value)
        result["values"] = {
            agent: {good: str(amount) for good, amount in row.items()}
            for agent, row in values.items()
        }
        for escape_radius in range(maximum_escape_radius + 1):
            escape_status, allocation = solve_at_radius(values, old, escape_radius)
            if escape_status == z3.sat:
                result["nearest_flexible_escape"] = {
                    "minimum_moved_goods": escape_radius,
                    "allocation": allocation,
                    "utilities": validate(values, old, allocation),
                    "topology": transfer_topology(old, allocation),
                }
                break
        else:
            result["nearest_flexible_escape"] = {"status": "not_found"}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--rooted", action="store_true")
    parser.add_argument("--maximum-escape-radius", type=int, default=6)
    args = parser.parse_args()
    result = run(args.radius, args.rooted, args.maximum_escape_radius)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_allocation_count": result["candidate_allocation_count"],
        "nearest_topology": result.get("nearest_flexible_escape", {}).get("topology"),
    }, indent=2))


if __name__ == "__main__":
    main()
