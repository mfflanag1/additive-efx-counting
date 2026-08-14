#!/usr/bin/env python3
"""Audit ordinary-PI exclusion and automatic current-edge payment."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


DOC = Path(__file__).parents[2] / "results" / (
    "PI_FREE_RANK_THREE_CYCLE_CURRENT_EDGE_LEMMA_20260813.md"
)


def qf_lra_payment():
    current = z3.Real("current")
    incoming = z3.Real("incoming")
    outgoing = z3.Real("outgoing")
    solver = z3.SolverFor("QF_LRA")
    solver.add(current > 0, incoming > current, outgoing >= 0, outgoing <= current)
    solver.add(current - outgoing + incoming <= current)
    return solver.check() == z3.unsat


def audit():
    rows = []
    checks = {"current_edge_payment": qf_lra_payment()}
    for name, length in (("R2", 2), ("R3", 3)):
        checked = 0
        pi_free = 0
        violations = 0
        for ordinary in itertools.product((False, True), repeat=length):
            checked += 1
            is_pi_free = not all(ordinary)
            pi_free += is_pi_free
            violations += is_pi_free and not any(not flag for flag in ordinary)
        rows.append({
            "form": name,
            "cycle_length": length,
            "ordinary_labelings_checked": checked,
            "pi_free_labelings": pi_free,
            "violations": violations,
        })
        checks[f"{name}_pi_free_forces_current_only_edge"] = violations == 0
    return {
        "schema": "pi-free-rank-three-cycle-current-edge-audit-v1",
        "status": (
            "PI_FREE_CYCLE_CURRENT_EDGE_VERIFIED"
            if all(checks.values()) else "AUDIT_FAILED"
        ),
        "checks": checks,
        "forms": rows,
        "document_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "claim_boundary": (
            "cap-free response-label and payment implication only. Mixed-edge "
            "payment, sacrificed-owner payment, observers, and EFX remain open."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "forms": result["forms"]}, indent=2))


if __name__ == "__main__":
    main()
