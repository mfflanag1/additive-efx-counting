#!/usr/bin/env python3
"""Audit the two-level terminal path charity selector."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT):
    dq, c_q, p2_q, charity_q = z3.Reals("dq c_q p2_q charity_q")
    q_payment = z3.SolverFor("QF_LRA")
    q_payment.add(z3.Xor(
        dq - c_q + p2_q + charity_q >= 0,
        p2_q >= c_q - dq - charity_q,
    ))

    dx, p2_x, p1_x, charity_x = z3.Reals("dx p2_x p1_x charity_x")
    x_payment = z3.SolverFor("QF_LRA")
    x_payment.add(z3.Xor(
        dx - p2_x + p1_x + charity_x >= 0,
        p1_x >= p2_x - dx - charity_x,
    ))

    dy, p1_y, charity_y = z3.Reals("dy p1_y charity_y")
    y_payment = z3.SolverFor("QF_LRA")
    y_payment.add(z3.Xor(
        dy - p1_y + charity_y >= 0,
        p1_y <= dy + charity_y,
    ))

    fq, bq, c, d2 = z3.Reals("fq bq c d2")
    q_feasible = z3.SolverFor("QF_LRA")
    q_feasible.add(bq >= fq, c >= 0, c <= bq, d2 > bq)
    q_feasible.add(d2 < c - (bq - fq))

    fx, bx, p2, d1 = z3.Reals("fx bx p2 d1")
    x_feasible = z3.SolverFor("QF_LRA")
    x_feasible.add(bx >= fx, p2 >= 0, p2 <= bx, d1 > bx)
    x_feasible.add(d1 < p2 - (bx - fx))

    theorem = root / "results/TERMINAL_PATH_TWO_LEVEL_CHARITY_SELECTOR_LEMMA_20260814.md"
    parent = root / "results/TERMINAL_PATH_CHARITY_PLACEMENT_BICRITERIA_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Exact dynamic selector" in text
    assert "Phi_q" in text
    assert "Phi_x" in text
    assert "Phi_y" in text

    return {
        "schema": "terminal-path-two-level-charity-selector-audit-v1",
        "status": "PAID_FOUR_EDGE_OR_THREE_PLACEMENT_TWO_LEVEL_SEPARATOR",
        "q_payment_equivalence": q_payment.check() == z3.unsat,
        "x_payment_equivalence": x_payment.check() == z3.unsat,
        "y_payment_equivalence": y_payment.check() == z3.unsat,
        "full_d2_meets_q_threshold": q_feasible.check() == z3.unsat,
        "full_d1_meets_x_threshold": x_feasible.check() == z3.unsat,
        "current_holder_edge_bound": 4,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "three_placement_separator_eliminated": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "all terminal maps have a two-level four-edge selector; only the "
            "three charity-placement cost separator remains at owner payment"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
