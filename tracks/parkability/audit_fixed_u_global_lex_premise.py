#!/usr/bin/env python3
"""Exact global-lex audit of the fixed-U charity-tree countermodel."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        old_bundles,
        validate_flower_master,
    )
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        old_bundles,
        validate_flower_master,
    )


RECIPIENTS = (*AGENTS, "_")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction()
    return total(values, observer, goods) - min(values[observer][good] for good in goods)


def is_efx_with_charity(values, allocation):
    return all(
        total(values, observer, allocation[observer])
        >= tail(values, observer, allocation[target])
        for observer in AGENTS
        for target in AGENTS
    ) and all(
        total(values, observer, allocation[observer])
        >= total(values, observer, allocation["_"])
        for observer in AGENTS
    )


def transfer_topology(old, allocation):
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient for recipient in RECIPIENTS for good in allocation[recipient]
    }
    moved = sorted(good for good in new_owner if new_owner[good] != base_owner[good])
    counts = Counter((base_owner[good], new_owner[good]) for good in moved)
    adjacency = defaultdict(set)
    for source, target in counts:
        adjacency[source].add(target)
        adjacency[target].add(source)
    components = []
    unseen = set(adjacency)
    while unseen:
        start = min(unseen)
        seen = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        unseen -= seen
        components.append(sorted(seen))
    directed_edges = sorted(counts)
    return {
        "moved_good_count": len(moved),
        "moved_goods": moved,
        "directed_edges": [
            {"source": source, "target": target, "count": counts[source, target]}
            for source, target in directed_edges
        ],
        "nontrivial_components": sorted(components),
        "has_directed_cycle": any(
            (target, source) in counts for source, target in directed_edges
        ),
    }


def run(source_path: Path) -> dict:
    payload = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    old = validate_flower_master(values)
    goods = ("f", *(good for agent in AGENTS for good in old[agent]))
    base = {agent: total(values, agent, old[agent]) for agent in AGENTS}

    owner = {good: z3.Int(f"owner_{good}") for good in goods}
    solver = z3.Solver()
    solver.set(random_seed=0)
    for good in goods:
        solver.add(owner[good] >= 0, owner[good] < len(RECIPIENTS))
    solver.add(z3.Or(*(owner[good] == 4 for good in goods)))

    utility = {
        (observer, recipient): z3.Sum(*(
            z3.If(owner[good] == recipient_index, q(values[observer][good]), 0)
            for good in goods
        ))
        for observer in AGENTS
        for recipient_index, recipient in enumerate(RECIPIENTS)
    }
    for observer_index, observer in enumerate(AGENTS):
        own = utility[observer, observer]
        for target_index, target in enumerate(AGENTS):
            target_total = utility[observer, target]
            for good in goods:
                solver.add(z3.Implies(
                    owner[good] == target_index,
                    own >= target_total - q(values[observer][good]),
                ))
        solver.add(own >= utility[observer, "_"])

    lex_terms = []
    for position, agent in enumerate(AGENTS):
        prefix = [
            utility[earlier, earlier] == q(base[earlier])
            for earlier in AGENTS[:position]
        ]
        lex_terms.append(z3.And(
            *prefix,
            utility[agent, agent] > q(base[agent]),
        ))
    solver.add(z3.Or(*lex_terms))

    status = solver.check()
    allocation = None
    topology = None
    utility_rows = None
    first_improver = None
    all_agents_strict = None
    strict_pareto_witness_available = False
    if status == z3.sat:
        solver.push()
        solver.add(*(
            utility[agent, agent] > q(base[agent]) for agent in AGENTS
        ))
        if solver.check() == z3.sat:
            strict_pareto_witness_available = True
        else:
            solver.pop()
        # Canonicalize the witness independently of Z3's unconstrained model
        # choice: in goods order, fix the least recipient preserving SAT.
        for good in goods:
            selected = None
            for recipient_index in range(len(RECIPIENTS)):
                solver.push()
                solver.add(owner[good] == recipient_index)
                feasible = solver.check() == z3.sat
                solver.pop()
                if feasible:
                    selected = recipient_index
                    solver.add(owner[good] == recipient_index)
                    break
            assert selected is not None
        assert solver.check() == z3.sat
        model = solver.model()
        allocation = {recipient: [] for recipient in RECIPIENTS}
        for good in goods:
            recipient = RECIPIENTS[model.eval(owner[good]).as_long()]
            allocation[recipient].append(good)
        for recipient in RECIPIENTS:
            allocation[recipient].sort()
        assert allocation["_"]
        assert is_efx_with_charity(values, allocation)
        utility_rows = {
            agent: str(total(values, agent, allocation[agent])) for agent in AGENTS
        }
        for agent in AGENTS:
            amount = total(values, agent, allocation[agent])
            if amount != base[agent]:
                assert amount > base[agent]
                first_improver = agent
                break
        assert first_improver is not None
        all_agents_strict = all(
            total(values, agent, allocation[agent]) > base[agent]
            for agent in AGENTS
        )
        topology = transfer_topology(old, allocation)

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "fixed-u-global-lex-premise-audit-v1",
        "status": "GLOBAL_LEX_COUNTERMODEL" if status == z3.unsat else "BASE_EXCLUDED",
        "solver_status": str(status),
        "priority": list(AGENTS),
        "positive_additive": True,
        "frozen_flower_master": "VERIFIED",
        "noncomplete_required": True,
        "base_utility": {agent: str(base[agent]) for agent in AGENTS},
        "lex_improving_allocation": allocation,
        "lex_improving_utility": utility_rows,
        "first_improver": first_improver,
        "all_agents_strict": all_agents_strict,
        "strict_pareto_witness_available": strict_pareto_witness_available,
        "old_charity": ["f"],
        "new_charity": allocation["_"] if allocation is not None else None,
        "charity_exchange": (
            allocation is not None and allocation["_"] != ["f"]
        ),
        "single_connected_transfer_component": (
            topology is not None and len(topology["nontrivial_components"]) == 1
        ),
        "transfer_topology": topology,
        "claim_boundary": (
            "exact global EFX-with-charity lex-improvement decision for the fixed-U "
            "tree countermodel under priority (r,q,c,s); UNSAT would promote this "
            "profile to the global-lex premise, while SAT exactly excludes it and "
            "identifies a missing non-tree topology"
        ),
        "provenance": {
            "source": str(source_path.resolve().relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "solver_status": result["solver_status"],
        "first_improver": result["first_improver"],
        "transfer_topology": result["transfer_topology"],
    }, indent=2))


if __name__ == "__main__":
    main()
