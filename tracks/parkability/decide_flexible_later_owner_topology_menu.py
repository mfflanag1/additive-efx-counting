#!/usr/bin/env python3
"""Decide the mined flexible later-owner topology menu in one flower cell."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        OLD_COMPONENTS,
        RECIPIENTS,
        atom_names,
        old_bundles,
        solve_at_radius,
        transfer_topology,
        validate,
    )
    from .decide_three_nonsingleton_flower_one_unpaid_cover import (
        BASE,
        candidate_covers,
    )
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        OLD_COMPONENTS,
        RECIPIENTS,
        atom_names,
        old_bundles,
        solve_at_radius,
        transfer_topology,
        validate,
    )
    from decide_three_nonsingleton_flower_one_unpaid_cover import (
        BASE,
        candidate_covers,
    )


COMPONENT_BUNDLES = {
    "A_q": ("aq_tq", "aq_br"),
    "A_r": ("ar_tr", "ar_bq"),
    "D_r": ("aq_tq", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": OLD_COMPONENTS["r"],
    "X_q": OLD_COMPONENTS["q"],
    "X_c": OLD_COMPONENTS["c"],
    "Z": ("z",),
}
MINED_SIGNATURES = (
    "_->q:1;q->_:1",
    "_->q:1;q->_:2",
    "_->q:1;q->_:3",
    "_->q:1;q->c:1;q->s:1",
    "c->_:1;c->q:1;q->c:1",
    "c->q:1;q->_:1",
    "c->q:1;q->_:2",
    "c->q:1;q->_:3",
    "c->q:1;q->_:1;q->c:1",
    "c->q:1;q->c:1",
    "c->q:1;q->c:2",
    "q->r:1;r->c:1;r->q:1",
    "q->r:1;r->_:1;r->q:1",
    "q->r:1;r->q:1;r->s:1",
)


def minimum(entries):
    result = entries[0]
    for entry in entries[1:]:
        result = z3.If(result <= entry, result, entry)
    return result


def true_tail(entries):
    if len(entries) <= 1:
        return z3.RealVal(0)
    return z3.Sum(*entries) - minimum(entries)


def build_master():
    components = tuple(dict.fromkeys(
        component for parts in COMPONENT_BUNDLES.values() for component in parts
    ))
    atoms = tuple(good for component in components for good in atom_names(component))
    bundles = {
        name: tuple(good for component in parts for good in atom_names(component))
        for name, parts in COMPONENT_BUNDLES.items()
    }
    old = old_bundles()
    value = {
        (good, agent): z3.Real(f"menu_{good}_{agent}")
        for good in atoms for agent in AGENTS
    }
    total = {
        (name, agent): z3.Sum(*(value[good, agent] for good in goods))
        for name, goods in bundles.items() for agent in AGENTS
    }
    tail = {
        (name, agent): true_tail([value[good, agent] for good in goods])
        for name, goods in bundles.items() for agent in AGENTS
    }
    base = {agent: total[BASE[agent], agent] for agent in AGENTS}
    solver = z3.SolverFor("QF_LRA")
    for good in atoms:
        for agent in AGENTS:
            solver.add(value[good, agent] > 0)
    for agent in AGENTS:
        for name in bundles:
            solver.add(tail[name, agent] <= base[agent])
        solver.add(value["f", agent] <= base[agent])
        solver.add(total["X_c", agent] <= base[agent])
    for name, source in {
        "D_r": "r",
        "D_q": "q",
        "D_c": "r",
        "Z": "c",
        "A_q": "c",
        "A_r": "c",
    }.items():
        solver.add(total[name, source] > base[source])
    covers = candidate_covers("r", "c", "c", "c", tuple(AGENTS))
    for cover in (record for record in covers if record["unpaid_agent"] is not None):
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS if target != unpaid
        )))
    solver.add(z3.Or(*(value["f", "q"] > value[good, "q"] for good in old["q"])))
    return solver, atoms, old, value, base


def parse_signature(signature):
    edges = []
    for entry in signature.split(";"):
        direction, count = entry.split(":")
        source, target = direction.split("->")
        edges.extend((source, target) for _ in range(int(count)))
    return tuple(edges)


def allocations_for_signature(signature, atoms, old):
    base = {agent: list(old[agent]) for agent in AGENTS}
    base["_"] = ["f"]
    by_source = defaultdict(list)
    for source, target in parse_signature(signature):
        by_source[source].append(target)
    source_choices = []
    for source, targets in sorted(by_source.items()):
        choices = []
        for goods in itertools.permutations(base[source], len(targets)):
            choices.append(tuple(zip(goods, targets)))
        source_choices.append(choices)

    allocations = {}
    for selected in itertools.product(*source_choices):
        allocation = {recipient: list(base[recipient]) for recipient in RECIPIENTS}
        for moves in selected:
            for good, target in moves:
                source = next(
                    recipient for recipient in RECIPIENTS if good in allocation[recipient]
                )
                allocation[source].remove(good)
                allocation[target].append(good)
        key = tuple(tuple(sorted(allocation[recipient])) for recipient in RECIPIENTS)
        allocations[key] = {
            recipient: sorted(allocation[recipient]) for recipient in RECIPIENTS
        }
    return tuple(allocations.values())


def completion_formula(allocation, value, base):
    own = {
        agent: z3.Sum(*(value[good, agent] for good in allocation[agent]))
        for agent in AGENTS
    }
    conditions = [own["r"] >= base["r"], own["q"] > base["q"]]
    for observer in AGENTS:
        for target in AGENTS:
            conditions.append(own[observer] >= true_tail([
                value[good, observer] for good in allocation[target]
            ]))
        conditions.append(
            own[observer]
            >= z3.Sum(*(value[good, observer] for good in allocation["_"]))
        )
    return z3.And(*conditions)


def fractions(model, atoms, value):
    return {
        agent: {
            good: Fraction(str(model.eval(value[good, agent], model_completion=True)))
            for good in atoms
        }
        for agent in AGENTS
    }


def run(maximum_escape_radius=6):
    solver, atoms, old, value, base = build_master()
    menu = []
    signature_counts = {}
    for signature in MINED_SIGNATURES:
        allocations = allocations_for_signature(signature, atoms, old)
        signature_counts[signature] = len(allocations)
        menu.extend(allocations)
    unique = {
        tuple(tuple(allocation[recipient]) for recipient in RECIPIENTS): allocation
        for allocation in menu
    }
    menu = tuple(unique.values())
    for allocation in menu:
        solver.add(z3.Not(completion_formula(allocation, value, base)))
    checked = solver.check()
    result = {
        "schema": "flexible-later-owner-topology-menu-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "signatures": list(MINED_SIGNATURES),
        "signature_allocation_counts": signature_counts,
        "unique_allocation_count": len(menu),
        "claim_boundary": (
            "bounded two-atom representative full-capture flower decision for "
            "the mined slot-topology menu; UNSAT would cover this bounded cell "
            "only, while SAT identifies a missing topology"
        ),
    }
    if checked == z3.sat:
        model = solver.model()
        values = fractions(model, atoms, value)
        result["values"] = {
            agent: {good: str(amount) for good, amount in row.items()}
            for agent, row in values.items()
        }
        for radius in range(maximum_escape_radius + 1):
            escape_status, allocation = solve_at_radius(values, old, radius)
            if escape_status == z3.sat:
                result["nearest_flexible_escape"] = {
                    "minimum_moved_goods": radius,
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
    parser.add_argument("--maximum-escape-radius", type=int, default=6)
    args = parser.parse_args()
    result = run(args.maximum_escape_radius)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "unique_allocations": result["unique_allocation_count"],
        "signature_counts": result["signature_allocation_counts"],
        "nearest_topology": result.get("nearest_flexible_escape", {}).get("topology"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
