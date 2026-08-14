#!/usr/bin/env python3
"""Form-specific CEGAR with an ITE-free exact complete-EFX encoding."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)
from .decide_two_survivor_named_topology_family import canonical, serialize_values
from .run_fixed_u_full_packet_terminal_cegar import (
    OWNERS,
    SUPPORT_STATE,
    fractions,
    total,
)
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master


def linear_complete_efx(allocation, value):
    """Exact EFX: check every possible deleted target good directly."""
    utility = {owner: total(value, owner, allocation[owner]) for owner in OWNERS}
    return z3.And(*(
        utility[observer] >= total(
            value, observer, tuple(g for g in allocation[target] if g != deleted)
        )
        for observer in OWNERS
        for target in OWNERS
        if target != observer
        for deleted in allocation[target]
    ))


def transfer_topology(allocation):
    supplier = provenance_holder(SUPPORT_STATE)
    return tuple(sorted({
        (supplier[good], recipient)
        for recipient, goods in allocation.items()
        if recipient != "charity"
        for good in goods
        if supplier[good] != recipient
    }))


def seed_allocations(path):
    payload = json.loads(path.read_text())
    records = payload.get("rounds", payload.get("iterations", []))
    seen = set()
    allocations = []
    for record in records:
        candidates = record.get("blocking_allocations")
        if candidates is None:
            candidates = record.get("chosen_allocations")
        if candidates is None:
            one = record.get("blocking_allocation")
            candidates = [] if one is None else [one]
        for allocation in candidates:
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            allocations.append(allocation)
    return allocations


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output, seed, form_index, maximum_rounds, timeout_seconds, cuts_per_round, random_seed):
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    seeds = seed_allocations(seed)
    seen = {canonical(allocation) for allocation in seeds}
    for allocation in seeds:
        solver.add(z3.Not(linear_complete_efx(allocation, value)))

    allocation_menu = tuple(
        allocation
        for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in OWNERS)
    )
    supplier = provenance_holder(SUPPORT_STATE)
    result = {
        "schema": "exact-response-linear-allocation-cegar-v1",
        "status": "RUNNING",
        "form_index": form_index,
        "seed": f"results/{seed.name}",
        "seed_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
        "seed_allocation_count": len(seeds),
        "allocation_menu_count": len(allocation_menu),
        "edge_bound": 4,
        "edge_origin": "support",
        "timeout_seconds_per_master": timeout_seconds,
        "cuts_per_round": cuts_per_round,
        "random_seed": random_seed,
        "rounds": [],
        "claim_boundary": (
            "form-specific topology-diverse allocation CEGAR in the exact "
            "twelve-atom necessary-premise cell. The linear deletion encoding "
            "is exactly complete EFX. UNSAT is bounded only; SAT obstruction "
            "still lacks the full saturated signed recurrence premises."
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
                "UNSAT_BOUNDED_FOUR_EDGE_THEOREM" if status == z3.unsat else "UNKNOWN"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            checkpoint(output, result)
            return result

        values = fractions(solver.model(), value)
        by_topology = defaultdict(list)
        for allocation in allocation_menu:
            if complete_efx(values, allocation):
                by_topology[transfer_topology(allocation)].append(allocation)
        if not by_topology:
            result["status"] = "SAT_BOUNDED_FOUR_EDGE_OBSTRUCTION"
            result["countermodel"] = serialize_values(values)
            result["countermodel_iteration"] = iteration
            checkpoint(output, result)
            return result

        ordered = sorted(
            by_topology.items(),
            key=lambda item: (len(item[0]), -len(item[1]), item[0]),
        )
        chosen = []
        for topology, allocations in ordered:
            fresh = next(
                (allocation for allocation in allocations if canonical(allocation) not in seen),
                None,
            )
            if fresh is not None:
                chosen.append(fresh)
                if len(chosen) == cuts_per_round:
                    break
        if not chosen:
            raise AssertionError("model defeats all cuts but has no fresh EFX witness")
        for allocation in chosen:
            seen.add(canonical(allocation))
            solver.add(z3.Not(linear_complete_efx(allocation, value)))
        result["rounds"].append({
            "iteration": iteration,
            "values": serialize_values(values),
            "complete_efx_allocation_count": sum(map(len, by_topology.values())),
            "feasible_topology_count": len(by_topology),
            "minimum_edge_count": min(map(len, by_topology)),
            "chosen_allocations": chosen,
            "chosen_topologies": [
                [list(edge) for edge in transfer_topology(allocation)]
                for allocation in chosen
            ],
        })
        result["total_blocked_allocation_count"] = len(seen)
        checkpoint(output, result)

    result["status"] = "ITERATION_LIMIT"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--maximum-rounds", type=int, default=8)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--cuts-per-round", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.output, args.seed, args.form_index, args.maximum_rounds,
        args.timeout_seconds, args.cuts_per_round, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
        "blocked": result.get("total_blocked_allocation_count", result["seed_allocation_count"]),
    }, indent=2))


if __name__ == "__main__":
    main()
