#!/usr/bin/env python3
"""Audit the coupled two-packet charity selector payment identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT):
    floor_m, retained_m, c0_m, h_m, subsidy_m = z3.Reals(
        "floor_m retained_m c0_m h_m subsidy_m"
    )
    missing = z3.SolverFor("QF_LRA")
    missing.add(z3.Xor(
        retained_m + c0_m + h_m + subsidy_m >= floor_m,
        h_m >= floor_m - retained_m - c0_m - subsidy_m,
    ))

    floor_q, retained_q, p_q, subsidy_q = z3.Reals(
        "floor_q retained_q p_q subsidy_q"
    )
    terminal = z3.SolverFor("QF_LRA")
    terminal.add(z3.Xor(
        retained_q + p_q + subsidy_q >= floor_q,
        p_q >= floor_q - retained_q - subsidy_q,
    ))

    delta_x, e0_x, overlap_x, h_x, p_x, subsidy_x = z3.Reals(
        "delta_x e0_x overlap_x h_x p_x subsidy_x"
    )
    predecessor = z3.SolverFor("QF_LRA")
    predecessor.add(z3.Xor(
        delta_x + e0_x + overlap_x - h_x - p_x + subsidy_x >= 0,
        h_x + p_x <= delta_x + e0_x + overlap_x + subsidy_x,
    ))

    fm, rm, c0, overlap = z3.Reals("fm rm c0 overlap")
    missing_feasible = z3.SolverFor("QF_LRA")
    missing_feasible.add(rm >= 0, c0 + overlap > fm)
    missing_feasible.add(overlap < fm - rm - c0)

    fq, rq, union_q, d_q = z3.Reals("fq rq union_q d_q")
    terminal_feasible = z3.SolverFor("QF_LRA")
    terminal_feasible.add(rq >= 0, union_q >= 0)
    terminal_feasible.add(rq + union_q >= fq)
    terminal_feasible.add(d_q > rq + union_q)
    terminal_feasible.add(d_q < fq - rq)

    theorem = root / "results/PREDECESSOR_TERMINAL_TWO_PACKET_CHARITY_SELECTOR_LEMMA_20260814.md"
    parent_overlap = root / "results/PREDECESSOR_CROSS_EXCHANGE_OVERLAP_BICRITERIA_LEMMA_20260814.md"
    parent_charity = root / "results/TERMINAL_PATH_CHARITY_PLACEMENT_BICRITERIA_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Exact three-corner failure separator" in text
    assert "charity to m" in text
    assert "charity to q" in text
    assert "charity to x" in text

    return {
        "schema": "predecessor-terminal-two-packet-charity-selector-audit-v1",
        "status": "PAID_FOUR_EDGE_OR_THREE_CORNER_SEPARATOR",
        "missing_payment_equivalence": missing.check() == z3.unsat,
        "terminal_payment_equivalence": terminal.check() == z3.unsat,
        "predecessor_payment_equivalence": predecessor.check() == z3.unsat,
        "full_overlap_meets_missing_threshold": missing_feasible.check() == z3.unsat,
        "full_path_core_meets_terminal_threshold": terminal_feasible.check() == z3.unsat,
        "current_holder_edge_bound": 4,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "three_corner_separator_eliminated": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent_overlap, parent_charity, script)
        },
        "claim_boundary": (
            "two predecessor terminal maps close unless all three charity "
            "subsidy corners miss the predecessor-cost packet frontier"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
