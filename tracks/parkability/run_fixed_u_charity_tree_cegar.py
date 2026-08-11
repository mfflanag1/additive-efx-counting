#!/usr/bin/env python3
"""Decide EFX-improving charity-rooted trees in the frozen fixed-U flower."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_charity_rooted_transfer_tree_release import rooted_trees
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        old_bundles,
    )
    from .decide_flexible_later_owner_topology_menu import (
        COMPONENT_BUNDLES,
        build_master,
        fractions,
    )
except ImportError:
    from audit_charity_rooted_transfer_tree_release import rooted_trees
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        old_bundles,
    )
    from decide_flexible_later_owner_topology_menu import (
        COMPONENT_BUNDLES,
        build_master,
        fractions,
    )


def q(value: Fraction):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def tree_topologies():
    records = []
    for size in range(1, len(AGENTS) + 1):
        for vertices in itertools.combinations(AGENTS, size):
            for root in vertices:
                for parent in rooted_trees(vertices, root):
                    records.append((vertices, root, parent))
    assert len(records) == 116
    return tuple(records)


def packet_oracle(values, old, topology):
    vertices, root, parent = topology
    children = {vertex: [] for vertex in vertices}
    for child, source in parent.items():
        children[source].append(child)
    sent = {
        (good, child): z3.Bool(f"send_{source}_{good}_{child}")
        for source in vertices
        for good in old[source]
        for child in children[source]
    }
    solver = z3.Solver()
    for source in vertices:
        for good in old[source]:
            choices = [sent[good, child] for child in children[source]]
            if choices:
                solver.add(z3.AtMost(*choices, 1))
    for child, source in parent.items():
        solver.add(z3.Or(*(sent[good, child] for good in old[source])))

    def membership(good, target):
        if good == "f":
            return z3.BoolVal(target == root)
        source = next(agent for agent in AGENTS if good in old[agent])
        if source not in vertices:
            return z3.BoolVal(target == source)
        outgoing = [sent[good, child] for child in children[source]]
        if target == source:
            return z3.Not(z3.Or(*outgoing)) if outgoing else z3.BoolVal(True)
        if target in children[source]:
            return sent[good, target]
        return z3.BoolVal(False)

    goods = ("f", *(good for agent in AGENTS for good in old[agent]))
    utility = {}
    for observer in AGENTS:
        for target in AGENTS:
            utility[observer, target] = z3.Sum(*(
                z3.If(membership(good, target), q(values[observer][good]), 0)
                for good in goods
            ))
    strict = []
    for agent in vertices:
        base = sum((values[agent][good] for good in old[agent]), Fraction(0))
        solver.add(utility[agent, agent] >= q(base))
        strict.append(utility[agent, agent] > q(base))
    solver.add(z3.Or(*strict))
    for observer in AGENTS:
        own = utility[observer, observer]
        for target in AGENTS:
            target_total = utility[observer, target]
            for good in goods:
                solver.add(z3.Implies(
                    membership(good, target),
                    own >= target_total - q(values[observer][good]),
                ))
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    allocation = {recipient: [] for recipient in RECIPIENTS}
    for good in goods:
        owners = [
            target for target in AGENTS
            if z3.is_true(model.eval(membership(good, target), model_completion=True))
        ]
        assert len(owners) == 1
        allocation[owners[0]].append(good)
    for recipient in allocation:
        allocation[recipient].sort()
    return allocation


def endpoint_formula(allocation, participants, value, old):
    own = {
        agent: z3.Sum(*(value[good, agent] for good in allocation[agent]))
        for agent in AGENTS
    }
    conditions = []
    strict = []
    for agent in participants:
        base = z3.Sum(*(value[good, agent] for good in old[agent]))
        conditions.append(own[agent] >= base)
        strict.append(own[agent] > base)
    conditions.append(z3.Or(*strict))
    for observer in AGENTS:
        for target in AGENTS:
            goods = allocation[target]
            for removed in goods:
                conditions.append(
                    own[observer]
                    >= z3.Sum(*(value[good, observer] for good in goods if good != removed))
                )
    return z3.And(*conditions)


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def add_source_margin_blockade(master, symbolic_value, old):
    source = "q"
    root = "r"
    desired = ("ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1", "f")
    pool = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
    root_base = z3.Sum(*(symbolic_value[good, root] for good in old[root]))
    source_base = z3.Sum(*(symbolic_value[good, source] for good in old[source]))
    count = 0
    for captured_bits in itertools.product((False, True), repeat=len(desired)):
        captured = tuple(
            good for good, selected in zip(desired, captured_bits) if selected
        )
        source_remainder = tuple(good for good in desired if good not in captured)
        for returned_bits in itertools.product((False, True), repeat=len(pool)):
            returned = tuple(
                good for good, selected in zip(pool, returned_bits) if selected
            )
            root_remainder = tuple(good for good in pool if good not in returned)
            root_target = z3.Sum(*(
                symbolic_value[good, root] for good in (*root_remainder, *captured)
            ))
            source_target = z3.Sum(*(
                symbolic_value[good, source] for good in (*source_remainder, *returned)
            ))
            master.add(z3.Implies(
                root_target >= root_base,
                source_target <= source_base,
            ))
            count += 1
    assert set(COMPONENT_BUNDLES["D_q"]) == {"ar_tr", "tr_rest", "f"}
    return {
        "root": root,
        "source": source,
        "desired_core": desired,
        "root_pool": pool,
        "exchange_implication_count": count,
    }


def run(output, maximum_iterations, timeout_seconds):
    master, atoms, old, symbolic_value, _ = build_master()
    certificate = add_source_margin_blockade(master, symbolic_value, old)
    master.set(timeout=timeout_seconds * 1000)
    topologies = tree_topologies()
    iterations = []
    result = {
        "schema": "fixed-u-charity-tree-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "topology_count": len(topologies),
        "topology_count_by_owner_count": {
            str(size): sum(len(vertices) == size for vertices, _, _ in topologies)
            for size in range(1, 5)
        },
        "source_margin_certificate": certificate,
        "iterations": iterations,
        "claim_boundary": (
            "exact CEGAR over every labeled charity-rooted tree through four owners "
            "and arbitrary nonempty disjoint one-edge packets in the frozen two-atom "
            "fixed-U flower; a SAT terminal refutes sufficiency in this exact flower "
            "cell, while UNSAT proves only the bounded flower conditional"
        ),
    }
    checkpoint(output, result)
    for iteration in range(maximum_iterations):
        status = master.check()
        record = {"iteration": iteration, "master_status": str(status)}
        iterations.append(record)
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            checkpoint(output, result)
            return result
        model = master.model()
        values = fractions(model, atoms, symbolic_value)
        found = None
        checked = 0
        for topology in topologies:
            checked += 1
            allocation = packet_oracle(values, old, topology)
            if allocation is not None:
                found = (topology, allocation)
                break
        record["topologies_checked"] = checked
        if found is None:
            result["status"] = "sat_countermodel"
            result["countermodel_iteration"] = iteration
            result["values"] = {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            }
            checkpoint(output, result)
            return result
        (vertices, root, parent), allocation = found
        record["blocking_cut"] = {
            "participants": list(vertices),
            "root": root,
            "parent": parent,
            "allocation": allocation,
        }
        master.add(z3.Not(endpoint_formula(
            allocation, vertices, symbolic_value, old
        )))
        checkpoint(output, result)
        print(json.dumps({
            "iteration": iteration,
            "topologies_checked": checked,
            "participants": vertices,
            "root": root,
        }), flush=True)
    result["status"] = "iteration_limit"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(args.output, args.maximum_iterations, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
    }, indent=2))


if __name__ == "__main__":
    main()
