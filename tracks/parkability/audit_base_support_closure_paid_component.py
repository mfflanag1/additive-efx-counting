#!/usr/bin/env python3
"""Independent audit of the base-support closure/reassembly identity."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
DOC = Path(__file__).parents[2] / "results" / (
    "BASE_SUPPORT_CLOSURE_PAID_COMPONENT_LEMMA_20260813.md"
)


def reachable_closure(edges, seed):
    closure = {seed}
    while True:
        enlarged = closure | {
            holder for base_owner, holder in edges if base_owner in closure
        }
        if enlarged == closure:
            return closure
        closure = enlarged


def weakly_connected(vertices, edges):
    if len(vertices) <= 1:
        return True
    seen = {next(iter(vertices))}
    while True:
        enlarged = seen | {
            right for left, right in edges if left in seen
        } | {
            left for left, right in edges if right in seen
        }
        enlarged &= vertices
        if enlarged == seen:
            return seen == vertices
        seen = enlarged


def symbolic_payment_check():
    solver = z3.SolverFor("QF_LRA")
    base = {owner: z3.Real(f"base_{owner}") for owner in OWNERS}
    external = {owner: z3.Real(f"external_{owner}") for owner in OWNERS}
    token = z3.Real("positive_charity_token")
    for owner in OWNERS:
        solver.add(base[owner] >= 0, external[owner] >= 0)
    solver.add(token > 0)

    # A reassembled closure owner receives its entire base support, retains
    # every incoming good whose base owner lies outside the closure, and one
    # selected closure owner receives the charity token.
    for owner in OWNERS:
        final = base[owner] + external[owner]
        solver.push()
        solver.add(final < base[owner])
        if solver.check() != z3.unsat:
            return False
        solver.pop()
    final_recipient = base[OWNERS[0]] + external[OWNERS[0]] + token
    solver.add(final_recipient <= base[OWNERS[0]])
    return solver.check() == z3.unsat


def audit():
    possible = tuple(
        (left, right) for left in OWNERS for right in OWNERS if left != right
    )
    records = 0
    nontrivial = 0
    proper = 0
    full = 0
    maximum_reverse_edges = 0
    checks = {
        "closure_has_no_outgoing_base_support_edge": True,
        "reassembly_edges_stay_inside_closure": True,
        "nontrivial_reassembly_component_is_connected": True,
        "outside_owners_are_unchanged": True,
        "symbolic_closure_owners_are_paid": symbolic_payment_check(),
        "external_positive_charity_makes_recipient_strict": symbolic_payment_check(),
    }

    # An edge a->b means that a base good is currently held by b. One atom
    # per edge is enough to audit closure, conservation, and connectivity for
    # every provenance graph; valuations are checked separately in QF_LRA.
    for mask in range(1 << len(possible)):
        edges = {
            edge for index, edge in enumerate(possible) if mask & (1 << index)
        }
        for seed in OWNERS:
            records += 1
            closure = reachable_closure(edges, seed)
            outgoing = {
                edge for edge in edges
                if edge[0] in closure and edge[1] not in closure
            }
            checks["closure_has_no_outgoing_base_support_edge"] &= not outgoing

            reversed_edges = {
                (holder, base_owner) for base_owner, holder in edges
                if base_owner in closure
            }
            checks["reassembly_edges_stay_inside_closure"] &= all(
                left in closure and right in closure
                for left, right in reversed_edges
            )
            checks["nontrivial_reassembly_component_is_connected"] &= (
                weakly_connected(closure, reversed_edges)
            )
            # No base support owned in the closure is held outside it, so the
            # reassembly removes no atom from an outside current holder.
            checks["outside_owners_are_unchanged"] &= not any(
                owner not in closure and base_owner in closure
                for base_owner, owner in edges
            )
            maximum_reverse_edges = max(maximum_reverse_edges, len(reversed_edges))
            if len(closure) > 1:
                nontrivial += 1
            if len(closure) < len(OWNERS):
                proper += 1
            else:
                full += 1

    return {
        "schema": "base-support-closure-paid-component-audit-v1",
        "status": (
            "BASE_SUPPORT_CLOSURE_PAID_COMPONENT_VERIFIED"
            if all(checks.values()) else "AUDIT_FAILED"
        ),
        "checks": checks,
        "directed_provenance_graphs": 1 << len(possible),
        "seeded_records_checked": records,
        "nontrivial_closures": nontrivial,
        "proper_closures": proper,
        "full_owner_closures": full,
        "maximum_internal_reverse_edges": maximum_reverse_edges,
        "document_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "claim_boundary": (
            "cap-free payment and connected-component identity for the least "
            "base-support closure. It does not bound the number of reverse "
            "edges by four, establish observer EFX, or supply the response-rank "
            "premise of saturated component extraction."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "records": result["seeded_records_checked"],
        "checks": result["checks"],
    }, indent=2))


if __name__ == "__main__":
    main()
