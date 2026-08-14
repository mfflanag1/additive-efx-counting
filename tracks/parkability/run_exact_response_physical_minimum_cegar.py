#!/usr/bin/env python3
"""CEGAR over a cap-free relaxation with one physical minimum per role/row."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import z3

from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)
from .decide_two_survivor_named_topology_family import canonical
from . import run_fixed_u_full_packet_terminal_cegar as terminal
from . import run_fixed_u_rank_three_relation_cegar as relation


def physical_tail(minimum):
    def tail(value, observer, goods):
        goods = tuple(goods)
        if not goods:
            return z3.RealVal(0)
        least = minimum[goods[0], observer]
        for good in goods[1:]:
            candidate = minimum[good, observer]
            least = z3.If(least <= candidate, least, candidate)
        return terminal.total(value, observer, goods) - least
    return tail


def build_physical_master(form_index):
    minimum = {
        (good, observer): z3.Real(f"physical_min_{good}_{observer}")
        for good in terminal.GOODS
        for observer in terminal.OWNERS
    }
    tail = physical_tail(minimum)
    old_terminal_tail = terminal.tail
    old_relation_tail = relation.tail
    try:
        terminal.tail = tail
        relation.tail = tail
        solver, value = relation.build_rank_three_master(
            exclude_self_responses=True,
            required_owner_cycle_form=True,
            exact_owner_cycle_response_relation=True,
            owner_cycle_form_index=form_index,
        )
    finally:
        terminal.tail = old_terminal_tail
        relation.tail = old_relation_tail
    solver.add(*(
        z3.And(minimum[good, observer] > 0, minimum[good, observer] <= value[good, observer])
        for good in terminal.GOODS
        for observer in terminal.OWNERS
    ))
    # A named role is one common physical packet.  It is either a singleton for
    # every observer, or has at least two positive goods, in which case its total
    # is at least twice its least-good value for every observer.  Conversely,
    # either alternative is physically realizable (two goods suffice in the
    # second case), so this is an exact cap-free totals/minima abstraction.
    solver.add(*(
        z3.Or(
            z3.And(*(minimum[good, observer] == value[good, observer]
                     for observer in terminal.OWNERS)),
            z3.And(*(2 * minimum[good, observer] <= value[good, observer]
                     for observer in terminal.OWNERS)),
        )
        for good in terminal.GOODS
    ))
    return solver, value, minimum


def linear_physical_efx(allocation, value, minimum):
    utility = {
        owner: terminal.total(value, owner, allocation[owner])
        for owner in terminal.OWNERS
    }
    return z3.And(*(
        utility[observer] >= terminal.total(value, observer, allocation[target])
        - minimum[role, observer]
        for observer in terminal.OWNERS
        for target in terminal.OWNERS
        if target != observer
        for role in allocation[target]
    ))


def concrete_physical_efx(values, minima, allocation):
    for observer in terminal.OWNERS:
        own = sum((values[observer][role] for role in allocation[observer]), Fraction())
        for target in terminal.OWNERS:
            if target == observer:
                continue
            target_roles = allocation[target]
            target_total = sum((values[observer][role] for role in target_roles), Fraction())
            least = min(minima[observer][role] for role in target_roles)
            if own < target_total - least:
                return False
    return True


def serialize(model, variables):
    return {
        observer: {
            good: str(Fraction(str(model.eval(variables[good, observer], model_completion=True))))
            for good in terminal.GOODS
        }
        for observer in terminal.OWNERS
    }


def transfer_topology(allocation):
    supplier = provenance_holder(terminal.SUPPORT_STATE)
    return tuple(sorted({
        (supplier[good], recipient)
        for recipient, goods in allocation.items()
        if recipient != "charity"
        for good in goods
        if supplier[good] != recipient
    }))


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output, form_index, maximum_rounds, timeout_seconds, cuts_per_round, random_seed):
    solver, value, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    allocation_menu = tuple(
        allocation
        for allocation in allocations_with_at_most_edges(4, terminal.SUPPORT_STATE)
        if all(allocation[owner] for owner in terminal.OWNERS)
    )
    seen = set()
    result = {
        "schema": "exact-response-physical-minimum-cegar-v2",
        "status": "RUNNING",
        "form_index": form_index,
        "physical_relaxation": (
            "each named role is jointly either a singleton for every observer or "
            "a multi-good packet whose total is at least twice its positive "
            "per-observer minimum; this totals/minima abstraction is exactly "
            "realizable with at most two physical goods per named role"
        ),
        "allocation_menu_count": len(allocation_menu),
        "edge_bound": 4,
        "edge_origin": "support",
        "timeout_seconds_per_master": timeout_seconds,
        "cuts_per_round": cuts_per_round,
        "random_seed": random_seed,
        "rounds": [],
        "claim_boundary": (
            "whole-role complete-EFX decision in a cap-free physical-minimum "
            "relaxation of one exact-response chart. UNSAT would prove that chart "
            "cap-free; SAT/iteration limit is evidence only and may be unrealizable."
        ),
        "provenance": {
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }
    checkpoint(output, result)

    for iteration in range(maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_CAPFREE_ROLE_UNION_THEOREM" if status == z3.unsat else "UNKNOWN"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            checkpoint(output, result)
            return result
        model = solver.model()
        values = {
            owner: {
                good: Fraction(str(model.eval(value[good, owner], model_completion=True)))
                for good in terminal.GOODS
            }
            for owner in terminal.OWNERS
        }
        minima = {
            owner: {
                good: Fraction(str(model.eval(minimum[good, owner], model_completion=True)))
                for good in terminal.GOODS
            }
            for owner in terminal.OWNERS
        }
        by_topology = defaultdict(list)
        for allocation in allocation_menu:
            if concrete_physical_efx(values, minima, allocation):
                by_topology[transfer_topology(allocation)].append(allocation)
        if not by_topology:
            result["status"] = "SAT_RELAXED_PHYSICAL_FOUR_EDGE_OBSTRUCTION"
            result["countermodel_totals"] = serialize(model, value)
            result["countermodel_minima"] = serialize(model, minimum)
            result["countermodel_iteration"] = iteration
            checkpoint(output, result)
            return result

        ordered = sorted(
            by_topology.items(),
            key=lambda item: (len(item[0]), -len(item[1]), item[0]),
        )
        chosen = []
        for _, allocations in ordered:
            fresh = next(
                (allocation for allocation in allocations if canonical(allocation) not in seen),
                None,
            )
            if fresh is not None:
                chosen.append(fresh)
                if len(chosen) == cuts_per_round:
                    break
        if not chosen:
            raise AssertionError("no fresh physical-EFX witness for current model")
        for allocation in chosen:
            seen.add(canonical(allocation))
            solver.add(z3.Not(linear_physical_efx(allocation, value, minimum)))
        result["rounds"].append({
            "iteration": iteration,
            "totals": serialize(model, value),
            "minima": serialize(model, minimum),
            "complete_efx_allocation_count": sum(map(len, by_topology.values())),
            "feasible_topology_count": len(by_topology),
            "minimum_edge_count": min(map(len, by_topology)),
            "chosen_allocations": chosen,
            "chosen_topologies": [
                [list(edge) for edge in transfer_topology(allocation)]
                for allocation in chosen
            ],
        })
        result["blocked_allocation_count"] = len(seen)
        checkpoint(output, result)

    result["status"] = "ITERATION_LIMIT"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--maximum-rounds", type=int, default=20)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--cuts-per-round", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.maximum_rounds,
        args.timeout_seconds, args.cuts_per_round, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
        "blocked": result.get("blocked_allocation_count", 0),
    }, indent=2))


if __name__ == "__main__":
    main()
