#!/usr/bin/env python3
"""Find a minimum-radius connected lexicographic EFX escape."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        value,
    )
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        value,
    )
    from analyze_flexible_later_owner_escape_topologies import old_bundles


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve(values, old, radius, timeout_seconds, objective):
    goods = tuple(values[AGENTS[0]])
    index = {recipient: position for position, recipient in enumerate(RECIPIENTS)}
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    owner = {good: z3.Int(f"lex_owner_{radius}_{good}") for good in goods}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for good in goods:
        solver.add(owner[good] >= 0, owner[good] < len(RECIPIENTS))

    def amount(observer, recipient):
        return z3.Sum(*(
            z3.If(
                owner[good] == index[recipient],
                z3.RealVal(str(values[observer][good])),
                0,
            )
            for good in goods
        ))

    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: amount(agent, agent) for agent in AGENTS}
    if objective == "lex":
        solver.add(z3.Or(*(
            z3.And(
                *(own[AGENTS[position]] == z3.RealVal(str(base[AGENTS[position]]))
                  for position in range(index_agent)),
                own[agent] > z3.RealVal(str(base[agent])),
            )
            for index_agent, agent in enumerate(AGENTS)
        )))
    elif objective == "later":
        solver.add(own["r"] >= z3.RealVal(str(base["r"])))
        solver.add(own["q"] > z3.RealVal(str(base["q"])))
    else:
        raise ValueError(f"unknown objective: {objective}")
    for observer in AGENTS:
        own_amount = amount(observer, observer)
        for target in AGENTS:
            total = amount(observer, target)
            for good in goods:
                solver.add(z3.Implies(
                    owner[good] == index[target],
                    own_amount >= total - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(own_amount >= amount(observer, "_"))

    moved = {
        good: owner[good] != index[base_owner[good]] for good in goods
    }
    solver.add(z3.Sum(*(z3.If(moved[good], 1, 0) for good in goods)) <= radius)
    solver.add(z3.Or(*(moved[good] for good in goods)))
    vertices = tuple(RECIPIENTS)
    active = {
        vertex: z3.Or(*(
            z3.And(
                moved[good],
                z3.Or(
                    base_owner[good] == vertex,
                    owner[good] == index[vertex],
                ),
            )
            for good in goods
        ))
        for vertex in vertices
    }
    for size in range(1, len(vertices)):
        for subset in itertools.combinations(vertices, size):
            if vertices[0] not in subset:
                continue
            inside = set(subset)
            outside = set(vertices) - inside
            crossing = []
            for good in goods:
                source_inside = base_owner[good] in inside
                targets = outside if source_inside else inside
                crossing.append(z3.And(
                    moved[good],
                    z3.Or(*(owner[good] == index[target] for target in targets)),
                ))
            solver.add(z3.Implies(
                z3.And(
                    z3.Or(*(active[vertex] for vertex in inside)),
                    z3.Or(*(active[vertex] for vertex in outside)),
                ),
                z3.Or(*crossing),
            ))
    checked = solver.check()
    if checked != z3.sat:
        return checked, None
    model = solver.model()
    allocation = {
        recipient: sorted(
            good for good in goods
            if model.eval(owner[good], model_completion=True).as_long()
            == index[recipient]
        )
        for recipient in RECIPIENTS
    }
    succeeds = lex_endpoint_succeeds if objective == "lex" else endpoint_succeeds
    assert succeeds(values, old, allocation)
    topology = transfer_topology(old, allocation)
    assert len(topology["nontrivial_components"]) == 1
    return checked, allocation


def run(source_path, maximum_radius, timeout_seconds, objective):
    source = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = old_bundles()
    statuses = []
    allocation = None
    for radius in range(1, maximum_radius + 1):
        checked, candidate = solve(values, old, radius, timeout_seconds, objective)
        statuses.append(str(checked))
        if checked == z3.sat:
            allocation = candidate
            break
        if checked == z3.unknown:
            break
    script = Path(__file__).resolve()
    root = script.parents[2]
    result = {
        "schema": "flexible-connected-escape-v1",
        "status": "FOUND" if allocation is not None else statuses[-1].upper(),
        "objective": objective,
        "radius_statuses": statuses,
        "solver": f"Z3 {z3.get_version_string()}",
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }
    if allocation is not None:
        base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
        own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
        result.update({
            "minimum_connected_radius": len(statuses),
            "allocation": allocation,
            "topology": transfer_topology(old, allocation),
            "base_utilities": {agent: str(amount) for agent, amount in base.items()},
            "owner_utilities": {agent: str(amount) for agent, amount in own.items()},
            "claim_boundary": (
                "exact connected lex EFX witness for the frozen profile; "
                "minimality through radius three is supplied by the separate "
                "complete exact census audit"
            ),
        })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-radius", type=int, default=6)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--objective", choices=("lex", "later"), default="lex")
    args = parser.parse_args()
    result = run(
        args.source.resolve(), args.maximum_radius, args.timeout_seconds, args.objective
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "minimum_connected_radius": result.get("minimum_connected_radius"),
        "topology": result.get("topology"),
    }, indent=2))


if __name__ == "__main__":
    main()
