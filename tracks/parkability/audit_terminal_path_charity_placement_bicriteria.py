#!/usr/bin/env python3
"""Audit the two charity placements at the terminal path endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT):
    delta_q, c_q, packet_q, charity_q = z3.Reals(
        "delta_q c_q packet_q charity_q"
    )
    terminal_payment = z3.SolverFor("QF_LRA")
    terminal_payment.add(z3.Xor(
        delta_q - c_q + packet_q + charity_q >= 0,
        packet_q >= c_q - delta_q - charity_q,
    ))

    delta_x, packet_x, charity_x = z3.Reals("delta_x packet_x charity_x")
    donor_payment = z3.SolverFor("QF_LRA")
    donor_payment.add(z3.Xor(
        delta_x - packet_x + charity_x >= 0,
        packet_x <= delta_x + charity_x,
    ))

    x_q, delta, c, d, p = z3.Reals("x_q delta c d p")
    threshold_existence = z3.SolverFor("QF_LRA")
    threshold_existence.add(
        x_q >= 0,
        delta >= 0,
        c >= 0,
        c <= x_q + delta,
        d > x_q + delta,
        p > 0,
    )
    theta = c - delta
    threshold_existence.add(z3.Or(
        d < theta,
        d < theta - p,
    ))

    theorem = root / "results/TERMINAL_PATH_CHARITY_PLACEMENT_BICRITERIA_LEMMA_20260814.md"
    parent = root / "results/CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Placement Q" in text
    assert "Placement X" in text
    assert "Nested critical-packet failure" in text

    return {
        "schema": "terminal-path-charity-placement-bicriteria-audit-v1",
        "status": "TWO_THREE_EDGE_PLACEMENTS_OR_NESTED_CRITICAL_PACKETS",
        "terminal_payment_equivalence": terminal_payment.check() == z3.unsat,
        "donor_payment_equivalence": donor_payment.check() == z3.unsat,
        "full_path_core_meets_both_thresholds": threshold_existence.check() == z3.unsat,
        "current_holder_edge_bound": 3,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "critical_system_eliminated": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "terminal charity can subsidize q or x; joint failure leaves "
            "nested two-corner critical packets, with physical provenance open"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
