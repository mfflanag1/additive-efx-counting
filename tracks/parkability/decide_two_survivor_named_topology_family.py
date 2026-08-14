#!/usr/bin/env python3
"""Decide the union of the named four-edge R2/R3 completion topologies.

The cap-free lemmas reduce the corrected exact response relation to two
survivor forms.  They exhibit Hamiltonian-path, branching, and full-cycle
completion topologies.  This script asks whether those topology families,
with completely unrestricted packet contents, already contain a complete
EFX allocation throughout the declared twelve-atom necessary-premise cell.

SAT refutes only this named-topology selector (and returns an exact profile).
UNSAT proves the selector only for the declared atomization.  Neither result
alone proves or refutes the cap-free saturated theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, SUPPORT_STATE, allocation_formula,
        fractions,
    )
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from .run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )
except ImportError:  # Permit direct replay from the script path.
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, SUPPORT_STATE, allocation_formula,
        fractions,
    )
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )


R2_TOPOLOGIES = (
    # Reverse s -> d -> r -> q, then charity to endpoint q.
    (("d", "s"), ("r", "d"), ("q", "r"), ("charity", "q")),
    # Reverse s -> d -> q -> r, then charity to endpoint r.
    (("d", "s"), ("q", "d"), ("r", "q"), ("charity", "r")),
    # Rotate r <-> q, pay d from r or q, charity to retained s.
    (("q", "r"), ("r", "q"), ("r", "d"), ("charity", "s")),
    (("q", "r"), ("r", "q"), ("q", "d"), ("charity", "s")),
    # Rotate r <-> q, pay s from d, charity to sacrificed d.
    (("q", "r"), ("r", "q"), ("d", "s"), ("charity", "d")),
)


R3_CYCLE_RESPONSES = (("r", "q"), ("q", "s"), ("s", "r"))


def transfer_topology_for_responses(responses, charity_recipient):
    """Reverse response arrows into physical supplier -> recipient arrows."""
    return tuple((target, source) for source, target in responses) + (
        ("charity", charity_recipient),
    )


R3_BRANCH_TOPOLOGIES = tuple(
    transfer_topology_for_responses(
        tuple(edge for edge in R3_CYCLE_RESPONSES if edge[0] != omitted)
        + (("d", d_target),),
        omitted,
    )
    for d_target in ("r", "q")
    for omitted in ("r", "q", "s")
)


R3_TOPOLOGIES = (
    # Reverse d -> r -> q -> s and d -> q -> s -> r.
    (("r", "d"), ("q", "r"), ("s", "q"), ("charity", "s")),
    (("q", "d"), ("s", "q"), ("r", "s"), ("charity", "r")),
    *R3_BRANCH_TOPOLOGIES,
    # Rotate the whole paid cycle, charity to sacrificed d.
    (("q", "r"), ("s", "q"), ("r", "s"), ("charity", "d")),
)


ROOT_REASSEMBLY_TOPOLOGIES = tuple(
    (("r", "d"), ("d", "r"), ("charity", recipient))
    for recipient in OWNERS
)


ALL_D_BILATERAL_TOPOLOGIES = tuple(
    ((owner, "d"), ("d", owner), ("charity", recipient))
    for owner in OWNERS if owner != "d" for recipient in OWNERS
)


def supplier_map():
    return {
        good: supplier
        for supplier, goods in SUPPORT_STATE.items()
        for good in goods
    }


def allocations_supported_by(topology):
    """Enumerate all complete allocations using a subset of ``topology``.

    Packet sizes and retained residuals are unrestricted.  Allowing topology
    edges to be empty enlarges the named selector, so a SAT result remains a
    valid selector refutation.
    """
    supplier = supplier_map()
    allowed = set(topology)
    choices = []
    for good in GOODS:
        source = supplier[good]
        outgoing = tuple(
            target for edge_source, target in topology if edge_source == source
        )
        choices.append(outgoing if source == "charity" else (source, *outgoing))
    for targets in itertools.product(*choices):
        actual = {
            (supplier[good], target)
            for good, target in zip(GOODS, targets, strict=True)
            if supplier[good] != target
        }
        if not actual <= allowed:
            continue
        allocation = {recipient: [] for recipient in RECIPIENTS}
        for good, target in zip(GOODS, targets, strict=True):
            allocation[target].append(good)
        if any(not allocation[owner] for owner in OWNERS):
            continue
        yield allocation


def canonical(allocation):
    return tuple(tuple(allocation[recipient]) for recipient in RECIPIENTS)


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def run(output, form_index, timeout_seconds, random_seed, ordinary_pi_free=False,
        include_root_reassembly=False, include_all_d_bilateral=False,
        generalized_self_pi_free=False):
    if form_index not in (0, 2):
        raise ValueError("the corrected exact relation survives only in forms 0 and 2")
    topologies = R2_TOPOLOGIES if form_index == 0 else R3_TOPOLOGIES
    if include_root_reassembly:
        topologies = (*topologies, *ROOT_REASSEMBLY_TOPOLOGIES)
    if include_all_d_bilateral:
        topologies = (*topologies, *ALL_D_BILATERAL_TOPOLOGIES)
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    if ordinary_pi_free:
        solver.add(*ordinary_pi_free_constraints(value, BASE))
    if generalized_self_pi_free:
        solver.add(*generalized_self_pi_free_constraints(value, BASE))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    seen = set()
    counts = []
    started = time.monotonic()
    for topology in topologies:
        before = len(seen)
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        counts.append(len(seen) - before)
    build_seconds = time.monotonic() - started
    status = solver.check()
    result = {
        "schema": "two-survivor-named-topology-family-decision-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "topologies": [[list(edge) for edge in topology] for topology in topologies],
        "new_allocation_counts_by_topology": counts,
        "distinct_allocation_count": len(seen),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "ordinary_pi_free": ordinary_pi_free,
        "include_root_reassembly": include_root_reassembly,
        "include_all_d_bilateral": include_all_d_bilateral,
        "generalized_self_pi_free": generalized_self_pi_free,
        "build_seconds": build_seconds,
        "solve_seconds": time.monotonic() - started - build_seconds,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "direct decision for the union of every named Hamiltonian-path, "
            "branching, and full-cycle topology in the declared twelve-atom "
            "corrected exact-response cell, with unrestricted packet contents"
            + (" and complete ordinary PI-freeness. " if ordinary_pi_free else ". ")
            + ("All generalized one-edge PI self-cycles are excluded. "
               if generalized_self_pi_free else "")
            + ("The menu also includes every bilateral r-d reassembly with "
               "charity sent to any owner. " if include_root_reassembly else "")
            + ("The menu also includes every bilateral exchange between d and "
               "one represented owner, with charity sent to any owner. "
               if include_all_d_bilateral else "")
            +
            "SAT refutes only this enlarged named-topology selector and is not a "
            "full saturated-state countermodel. UNSAT is only a bounded-atom theorem."
        ),
    }
    if status == z3.sat:
        result["values"] = serialize_values(fractions(solver.model(), value))
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--ordinary-pi-free", action="store_true")
    parser.add_argument("--include-root-reassembly", action="store_true")
    parser.add_argument("--include-all-d-bilateral", action="store_true")
    parser.add_argument("--generalized-self-pi-free", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.timeout_seconds, args.random_seed,
        args.ordinary_pi_free, args.include_root_reassembly,
        args.include_all_d_bilateral,
        args.generalized_self_pi_free,
    )
    print(json.dumps({
        key: result[key] for key in (
            "status", "form_name", "distinct_allocation_count",
            "build_seconds", "solve_seconds",
        )
    }, indent=2))


if __name__ == "__main__":
    main()
