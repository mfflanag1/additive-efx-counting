#!/usr/bin/env python3
"""Topology-level CEGAR for the corrected exact-response twelve-atom cell.

Each refinement adds an entire transfer-topology family with unrestricted
packets, rather than one EFX allocation.  This is strictly stronger per
iteration than allocation-level CEGAR and tests whether a small flexible
topology basis explains the observed four-edge closure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_fixed_u_support_edge_three_no_go import complete_efx
    from .decide_exact_response_functional_cover_family import (
        FUNCTIONAL_COVER_TOPOLOGIES,
    )
    from .decide_fixed_u_rank_three_four_edge_complete_efx import (
        allocations_with_at_most_edges,
    )
    from .decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from .run_fixed_u_full_packet_terminal_cegar import (
        GOODS, OWNERS, SUPPORT_STATE, allocation_formula, fractions,
    )
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
except ImportError:
    from audit_fixed_u_support_edge_three_no_go import complete_efx
    from decide_exact_response_functional_cover_family import (
        FUNCTIONAL_COVER_TOPOLOGIES,
    )
    from decide_fixed_u_rank_three_four_edge_complete_efx import (
        allocations_with_at_most_edges,
    )
    from decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from run_fixed_u_full_packet_terminal_cegar import (
        GOODS, OWNERS, SUPPORT_STATE, allocation_formula, fractions,
    )
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master


def normalize(topology):
    return tuple(sorted(tuple(edge) for edge in topology))


def transfer_topology(allocation):
    supplier = {
        good: source for source, goods in SUPPORT_STATE.items() for good in goods
    }
    return tuple(sorted({
        (supplier[good], recipient)
        for recipient, goods in allocation.items() if recipient != "charity"
        for good in goods if supplier[good] != recipient
    }))


def functional(topology):
    return len({source for source, _ in topology}) == len(topology)


def add_topology(solver, value, topology, globally_seen):
    added = 0
    for allocation in allocations_supported_by(topology):
        key = canonical(allocation)
        if key in globally_seen:
            continue
        globally_seen.add(key)
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        added += 1
    return added


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output, form_index, maximum_iterations, timeout_seconds, random_seed,
        maximum_new_topologies, resume):
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    prior = json.loads(output.read_text()) if resume and output.exists() else None
    selected = [normalize(t) for t in (
        prior["selected_topologies"] if prior else FUNCTIONAL_COVER_TOPOLOGIES
    )]
    rounds = list(prior.get("rounds", [])) if prior else []
    globally_seen = set()
    topology_allocation_counts = {}
    for topology in selected:
        topology_allocation_counts[str(topology)] = add_topology(
            solver, value, topology, globally_seen
        )

    result = {
        "schema": "exact-response-topology-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "timeout_seconds_per_master": timeout_seconds,
        "random_seed": random_seed,
        "maximum_new_topologies_per_round": maximum_new_topologies,
        "selected_topologies": [[list(edge) for edge in t] for t in selected],
        "distinct_blocked_allocation_count": len(globally_seen),
        "rounds": rounds,
        "claim_boundary": (
            "topology-level CEGAR in one corrected exact-response twelve-atom "
            "necessary-premise cell. UNSAT proves only the bounded theorem; a "
            "profile with no <=4 witness is a bounded obstruction, not a full "
            "saturated-state countermodel. Iteration limit/UNKNOWN is evidence only."
        ),
        "provenance": {
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }
    checkpoint(output, result)

    allocation_menu = tuple(allocations_with_at_most_edges(4, SUPPORT_STATE))
    start = len(rounds)
    for iteration in range(start, maximum_iterations):
        status = solver.check()
        if status == z3.unsat:
            result["status"] = "UNSAT_BOUNDED_FOUR_EDGE_THEOREM"
            checkpoint(output, result)
            return result
        if status == z3.unknown:
            result["status"] = "UNKNOWN"
            result["reason_unknown"] = solver.reason_unknown()
            checkpoint(output, result)
            return result

        values = fractions(solver.model(), value)
        by_topology = defaultdict(list)
        for allocation in allocation_menu:
            if any(not allocation[owner] for owner in OWNERS):
                continue
            if complete_efx(values, allocation):
                by_topology[transfer_topology(allocation)].append(allocation)

        if not by_topology:
            result["status"] = "SAT_BOUNDED_FOUR_EDGE_OBSTRUCTION"
            result["countermodel"] = serialize_values(values)
            result["countermodel_iteration"] = iteration
            checkpoint(output, result)
            return result

        candidates = [
            (topology, allocations) for topology, allocations in by_topology.items()
            if topology not in selected
        ]
        # A four-edge topology contains every packet allocation supported by
        # each of its subgraphs, so larger functional witnesses eliminate a
        # strictly broader family per refinement than a minimal-edge witness.
        candidates.sort(key=lambda pair: (
            not functional(pair[0]), -len(pair[0]), -len(pair[1]), pair[0]
        ))
        chosen = [topology for topology, _ in candidates[:maximum_new_topologies]]
        if not chosen:
            raise AssertionError("current model should defeat every selected topology")
        counts = []
        for topology in chosen:
            selected.append(topology)
            counts.append(add_topology(solver, value, topology, globally_seen))
        rounds.append({
            "iteration": iteration,
            "values": serialize_values(values),
            "complete_efx_allocation_count": sum(map(len, by_topology.values())),
            "feasible_topology_count": len(by_topology),
            "minimum_edge_count": min(map(len, by_topology)),
            "chosen_topologies": [[list(edge) for edge in t] for t in chosen],
            "new_blocked_allocation_counts": counts,
        })
        result["rounds"] = rounds
        result["selected_topologies"] = [
            [list(edge) for edge in topology] for topology in selected
        ]
        result["distinct_blocked_allocation_count"] = len(globally_seen)
        checkpoint(output, result)

    result["status"] = "ITERATION_LIMIT"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--maximum-iterations", type=int, default=20)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-new-topologies", type=int, default=4)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.maximum_iterations,
        args.timeout_seconds, args.random_seed, args.maximum_new_topologies,
        args.resume,
    )
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
        "selected_topologies": len(result["selected_topologies"]),
        "blocked_allocations": result["distinct_blocked_allocation_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
