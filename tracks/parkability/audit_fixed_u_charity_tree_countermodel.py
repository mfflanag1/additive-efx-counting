#!/usr/bin/env python3
"""Exact replay of the fixed-U source-margin charity-tree countermodel."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_charity_rooted_transfer_tree_release import rooted_trees
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        old_bundles,
        validate_flower_master,
    )
except ImportError:
    from audit_charity_rooted_transfer_tree_release import rooted_trees
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        old_bundles,
        validate_flower_master,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def all_trees():
    for size in range(1, 5):
        for vertices in itertools.combinations(AGENTS, size):
            for root in vertices:
                for parent in rooted_trees(vertices, root):
                    yield vertices, root, parent


def topology_is_unsat(values, old, topology):
    vertices, root, parent = topology
    children = {vertex: [] for vertex in vertices}
    for child, source in parent.items():
        children[source].append(child)
    route = {
        (source, good): z3.Int(f"route_{source}_{good}")
        for source in vertices for good in old[source]
    }
    solver = z3.Solver()
    for source in vertices:
        for good in old[source]:
            solver.add(route[source, good] >= 0)
            solver.add(route[source, good] <= len(children[source]))
    for child, source in parent.items():
        index = children[source].index(child) + 1
        solver.add(z3.Or(*(
            route[source, good] == index for good in old[source]
        )))

    owner = {good: agent for agent in AGENTS for good in old[agent]}
    goods = ("f", *owner)

    def has(good, target):
        if good == "f":
            return z3.BoolVal(target == root)
        source = owner[good]
        if source not in vertices:
            return z3.BoolVal(target == source)
        if target == source:
            return route[source, good] == 0
        if target in children[source]:
            return route[source, good] == children[source].index(target) + 1
        return z3.BoolVal(False)

    utility = {
        (observer, target): z3.Sum(*(
            z3.If(has(good, target), z3.RealVal(str(values[observer][good])), 0)
            for good in goods
        ))
        for observer in AGENTS for target in AGENTS
    }
    strict = []
    for agent in vertices:
        base = z3.RealVal(str(total(values, agent, old[agent])))
        solver.add(
            utility[agent, agent]
            >= base
        )
        strict.append(utility[agent, agent] > base)
    solver.add(z3.Or(*strict))
    for observer in AGENTS:
        for target in AGENTS:
            for good in goods:
                solver.add(z3.Implies(
                    has(good, target),
                    utility[observer, observer]
                    >= utility[observer, target]
                    - z3.RealVal(str(values[observer][good])),
                ))
    return solver.check() == z3.unsat


def source_margin_audit(values, old):
    root = "r"
    source = "q"
    desired = ("ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1", "f")
    pool = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
    root_base = total(values, root, old[root])
    source_base = total(values, source, old[source])
    assert total(values, source, desired) > source_base
    assert set((*pool, *desired[:-1])) == set(old[root])
    assert total(values, root, (*pool, *desired[:-1])) == root_base
    feasible = []
    for captured_bits in itertools.product((False, True), repeat=len(desired)):
        captured = tuple(
            good for good, chosen in zip(desired, captured_bits) if chosen
        )
        source_remainder = tuple(good for good in desired if good not in captured)
        for returned_bits in itertools.product((False, True), repeat=len(pool)):
            returned = tuple(
                good for good, chosen in zip(pool, returned_bits) if chosen
            )
            root_remainder = tuple(good for good in pool if good not in returned)
            root_target = (*root_remainder, *captured)
            source_target = (*source_remainder, *returned)
            if total(values, root, root_target) >= root_base:
                assert total(values, source, source_target) <= source_base
                feasible.append((
                    total(values, source, source_target),
                    captured,
                    returned,
                    root_target,
                    source_target,
                ))
    assert feasible
    optimum = max(record[0] for record in feasible)
    selected = min(record for record in feasible if record[0] == optimum)
    _, captured, returned, root_target, _ = selected
    slack = total(values, root, root_target) - root_base
    root_remainder = tuple(good for good in pool if good not in returned)
    source_remainder = tuple(good for good in desired if good not in captured)
    assert all(values[root][good] > slack for good in (*captured, *root_remainder))
    for c in captured:
        for b in returned:
            if values[root][b] >= values[root][c]:
                assert values[source][b] >= values[source][c]
    for h in source_remainder:
        for g in root_remainder:
            if values[root][h] >= values[root][g]:
                assert values[source][h] >= values[source][g]
    return {
        "exchange_pairs_checked": 2 ** (len(desired) + len(pool)),
        "root_feasible_exchange_count": len(feasible),
        "maximum_source_target_value": str(optimum),
        "source_base_value": str(source_base),
        "selected_captured": list(captured),
        "selected_returned": list(returned),
        "selected_root_slack": str(slack),
        "frontier_inequalities": "ALL_FORCED",
    }


def run(source_path):
    payload = json.loads(source_path.read_text())
    assert payload["status"] == "sat_countermodel"
    assert payload["topology_count"] == 116
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    old = validate_flower_master(values)
    margin = source_margin_audit(values, old)
    counts = {str(size): 0 for size in range(1, 5)}
    checked = 0
    for topology in all_trees():
        assert topology_is_unsat(values, old, topology)
        counts[str(len(topology[0]))] += 1
        checked += 1
    assert counts == {"1": 4, "2": 12, "3": 36, "4": 64}
    assert checked == 116
    script = Path(__file__).resolve()
    root = script.parents[2]
    try:
        displayed_source = str(source_path.resolve().relative_to(root))
    except ValueError:
        displayed_source = str(source_path)
    return {
        "schema": "fixed-u-charity-tree-countermodel-audit-v1",
        "status": "VERIFIED_COUNTERMODEL",
        "positive_additive": True,
        "frozen_flower_master": "VERIFIED",
        "source_margin_frontier": margin,
        "charity_rooted_topologies": {
            "count": checked,
            "by_owner_count": counts,
            "arbitrary_packet_encoding": True,
            "all_efx_improving_packet_systems": "UNSAT",
        },
        "claim_boundary": (
            "exact positive-rational countermodel showing that the frozen two-atom "
            "fixed-U flower premises plus the complete q-source/r-root exchange-stable "
            "margin certificate do not force an EFX Pareto-improving charity-rooted "
            "transfer tree. This refutes certificate sufficiency, not GG or additive EFX."
        ),
        "provenance": {
            "source": displayed_source,
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "topology_count": result["charity_rooted_topologies"]["count"],
    }, indent=2))


if __name__ == "__main__":
    main()
