#!/usr/bin/env python3
"""Decide the exact external-Hall star/fork topology menu in the 12-atom cell.

This is deliberately a bounded-atom decision.  It combines the cap-free
signed-edge classifications of the 2x1 star and 3x2 fork, then permits every
nonempty-owner allocation supported by any surviving topology.  Enlarging a
signed pattern to every allocation on its topology makes a SAT result a
strong selector refutation; an UNSAT result remains only a theorem for the
declared twelve-atom necessary-premise cell.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .audit_three_target_external_source_fork_edge_cancellation import (
        FORMS, enumerate_records,
    )
    from .decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from .run_fixed_u_full_packet_terminal_cegar import BASE, allocation_formula, fractions
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from .run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )
except ImportError:  # Permit direct replay from the script path.
    from audit_three_target_external_source_fork_edge_cancellation import (
        FORMS, enumerate_records,
    )
    from decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from run_fixed_u_full_packet_terminal_cegar import BASE, allocation_formula, fractions
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )


OWNERS = ("r", "q", "d", "s")
FORM_NAME = {0: "R2", 2: "R3"}


def canonical_topology(edges):
    return tuple(sorted(edges))


def star_topologies(form_name):
    """Return every topology admitted by the exact 2x1 support frontier."""
    matching = FORMS[form_name]  # response source -> physical target/supplier
    topologies = set()
    records = []
    for target in matching:  # only represented targets have an incoming packet
        incoming_supplier = matching[target]
        for external in OWNERS:
            if external == target:
                continue
            if external == incoming_supplier:
                cases = (("partial", False), ("whole", False), ("whole", True))
            else:
                cases = (("whole", False),)
            for incoming_state, residual_used in cases:
                destinations = {owner: {owner} for owner in OWNERS}
                for source, supplier in matching.items():
                    destinations[supplier].discard(supplier)
                    destinations[supplier].add(source)
                if incoming_state == "whole":
                    destinations[incoming_supplier].discard(target)
                destinations[incoming_supplier].add(external)
                if residual_used:
                    destinations[target].add(external)
                edges = {
                    (supplier, recipient)
                    for supplier, recipients in destinations.items()
                    for recipient in recipients if supplier != recipient
                }
                edges.add(("charity", target))
                assert len(edges) <= 4
                topology = canonical_topology(edges)
                topologies.add(topology)
                records.append({
                    "target": target,
                    "external": external,
                    "incoming_supplier": incoming_supplier,
                    "incoming_state": incoming_state,
                    "residual_used": residual_used,
                    "topology": [list(edge) for edge in topology],
                })
    return topologies, records


def fork_topologies(form_name):
    records = [
        record for record in enumerate_records()
        if record["form"] == form_name and record["within_four"]
    ]
    topologies = {
        canonical_topology(tuple(edge) for edge in record["final_edges"])
        for record in records
    }
    return topologies, records


def menu(form_index):
    form_name = FORM_NAME[form_index]
    star, star_records = star_topologies(form_name)
    fork, fork_records = fork_topologies(form_name)
    return star | fork, star, fork, star_records, fork_records


def run(output, form_index, timeout_seconds, random_seed,
        generalized_self_pi_free=False):
    topologies, star, fork, star_records, fork_records = menu(form_index)
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.add(*ordinary_pi_free_constraints(value, BASE))
    if generalized_self_pi_free:
        solver.add(*generalized_self_pi_free_constraints(value, BASE))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    # Fail closed against a vacuous menu theorem.  This exact atomization is
    # known to force a generalized self response in both surviving forms.
    # Check the premise cell before adding any negated EFX endpoints.
    premise_status = solver.check()

    seen = set()
    counts = []
    started = time.monotonic()
    if premise_status == z3.sat:
        for topology in sorted(topologies):
            before = len(seen)
            for allocation in allocations_supported_by(topology):
                key = canonical(allocation)
                if key in seen:
                    continue
                seen.add(key)
                solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
            counts.append(len(seen) - before)
    build_seconds = time.monotonic() - started
    status = solver.check() if premise_status == z3.sat else premise_status
    script = Path(__file__).resolve()
    result = {
        "schema": "external-hall-star-fork-twelve-atom-decision-v1",
        "status": (
            "vacuous_premise_unsat" if premise_status == z3.unsat else str(status)
        ),
        "premise_only_status": str(premise_status),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": FORM_NAME[form_index],
        "star_signature_count": len(star_records),
        "fork_signature_count": len(fork_records),
        "star_topology_count": len(star),
        "fork_topology_count": len(fork),
        "union_topology_count": len(topologies),
        "distinct_allocation_count": len(seen),
        "new_allocation_counts_by_topology": counts,
        "ordinary_pi_free": True,
        "generalized_self_pi_free": generalized_self_pi_free,
        "global_lex_maximality_fully_encoded": False,
        "full_signed_saturation_fully_encoded": False,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "build_seconds": build_seconds,
        "solve_seconds": time.monotonic() - started - build_seconds,
        "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "claim_boundary": (
            "direct decision for every nonempty-owner allocation supported by "
            "the exact 2x1 star or 3x2 fork edge-compatible topology in one "
            "corrected twelve-atom rank-three necessary-premise cell, with "
            "ordinary and generalized-self PI excluded. SAT refutes this enlarged "
            "Hall-menu selector only; UNSAT proves only the bounded-atom menu "
            "theorem. Global lex maximality, full signed-record reachability, all "
            "saturation exits, and the cap-free lift are not encoded."
        ),
    }
    if premise_status == z3.unsat:
        result["calibration_failure"] = (
            "the declared premise cell is already UNSAT before any Hall-menu "
            "endpoint is negated; no selector theorem follows"
        )
    elif status == z3.sat:
        result["values"] = serialize_values(fractions(solver.model(), value))
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--generalized-self-pi-free", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.timeout_seconds, args.random_seed,
        args.generalized_self_pi_free,
    )
    print(json.dumps({
        key: result[key] for key in (
            "status", "premise_only_status", "form_name", "star_signature_count",
            "fork_signature_count", "union_topology_count",
            "distinct_allocation_count", "build_seconds", "solve_seconds",
        )
    }, indent=2))


if __name__ == "__main__":
    main()
