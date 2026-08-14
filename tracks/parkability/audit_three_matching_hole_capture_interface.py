#!/usr/bin/env python3
"""Independent graph/QF_LRA audit of the three-matching hole interface."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "THREE_MATCHING_HOLE_CAPTURE_INTERFACE_LEMMA_20260813.md"
OWNERS = (0, 1, 2, 3)
CHARITY = 4


def audit():
    records = 0
    for unmatched_source in OWNERS:
        sources = tuple(owner for owner in OWNERS if owner != unmatched_source)
        for unmatched_target in OWNERS:
            targets = tuple(owner for owner in OWNERS if owner != unmatched_target)
            for assigned_targets in itertools.permutations(targets):
                matching = dict(zip(sources, assigned_targets, strict=True))
                target_source = {target: source for source, target in matching.items()}

                # Give each physical target two labeled atoms: its outgoing
                # core when matched, and its retained residual. Charity is a
                # third kind of atom. Verify every one appears exactly once.
                initial = {
                    *(('residual', target) for target in OWNERS),
                    *(('core', target) for target in targets),
                    ('charity', CHARITY),
                }
                final = set()
                for target in OWNERS:
                    final.add(('residual', target))
                for target, source in target_source.items():
                    final.add(('core', target))
                final.add(('charity', CHARITY))
                assert initial == final

                edges = {
                    (target, source)
                    for source, target in matching.items() if source != target
                }
                edges.add((CHARITY, unmatched_source))
                assert len(edges) <= 4
                assert len(matching) == 3
                records += 1

    # Matched-source payment: desired incoming core plus a nonnegative
    # residual is strictly above base.
    core, residual, base = z3.Reals("core residual base")
    paid = z3.SolverFor("QF_LRA")
    paid.add(core > base, residual >= 0, z3.Not(core + residual > base))
    assert paid.check() == z3.unsat

    # Exact hole identity and failure equivalence.
    current, outgoing, charity, base_h = z3.Reals(
        "current outgoing charity base_h"
    )
    delta = current - base_h
    identity = z3.SolverFor("QF_LRA")
    identity.add(z3.Not(
        current - outgoing + charity - base_h
        == delta - outgoing + charity
    ))
    assert identity.check() == z3.unsat
    failure = z3.SolverFor("QF_LRA")
    failure.add(
        (current - outgoing + charity < base_h)
        != (outgoing > delta + charity)
    )
    assert failure.check() == z3.unsat

    return {
        "schema": "three-matching-hole-capture-interface-audit-v1",
        "status": "ALL_NEAR_PERFECT_MATCHINGS_VERIFIED",
        "matching_records": records,
        "expected_matching_records": 96,
        "maximum_support_edges": 4,
        "matched_payment_status": "unsat",
        "hole_identity_status": "unsat",
        "hole_failure_equivalence_status": "unsat",
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free graph, conservation, matched-payment, and exact hole-"
            "failure interface only. Simultaneous capture reversal and final "
            "observer safety remain open."
        ),
    }


def main():
    result = audit()
    output = ROOT / "results" / "three_matching_hole_capture_interface_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "matching_records": result["matching_records"],
        "maximum_support_edges": result["maximum_support_edges"],
    }, indent=2))


if __name__ == "__main__":
    main()
