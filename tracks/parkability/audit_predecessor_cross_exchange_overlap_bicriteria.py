#!/usr/bin/env python3
"""Audit the exact shared-overlap split and critical-packet alternative."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    floor_m, residual_m, charity_m, c0_m, h_m = z3.Reals(
        "floor_m residual_m charity_m c0_m h_m"
    )
    alpha = floor_m - residual_m - charity_m - c0_m
    missing_payment = z3.SolverFor("QF_LRA")
    missing_payment.add(z3.Xor(
        residual_m + charity_m + c0_m + h_m >= floor_m,
        h_m >= alpha,
    ))

    floor_x, residual_x, e0_x, overlap_x, h_x = z3.Reals(
        "floor_x residual_x e0_x overlap_x h_x"
    )
    gamma = residual_x + e0_x + overlap_x - floor_x
    predecessor_payment = z3.SolverFor("QF_LRA")
    predecessor_payment.add(z3.Xor(
        residual_x + e0_x + overlap_x - h_x >= floor_x,
        h_x <= gamma,
    ))

    c0, overlap, floor, residual, charity = z3.Reals(
        "c0 overlap floor residual charity"
    )
    full_overlap_exists = z3.SolverFor("QF_LRA")
    full_overlap_exists.add(c0 + overlap > floor)
    full_overlap_exists.add(residual >= 0, charity > 0)
    full_overlap_exists.add(z3.Not(overlap >= floor - residual - charity - c0))

    theorem = root / "results/PREDECESSOR_CROSS_EXCHANGE_OVERLAP_BICRITERIA_LEMMA_20260814.md"
    parent = root / "results/TERMINAL_PATH_OMITTED_CORE_CROSS_EXCHANGE_FRONTIER_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Critical-overlap alternative" in text
    assert "frozen-supplier compression" in text

    return {
        "schema": "predecessor-cross-exchange-overlap-bicriteria-audit-v1",
        "status": "PAID_FOUR_EDGE_SPLIT_OR_MINIMAL_CRITICAL_OVERLAP",
        "missing_payment_equivalence": missing_payment.check() == z3.unsat,
        "predecessor_payment_equivalence": predecessor_payment.check() == z3.unsat,
        "full_overlap_always_meets_missing_threshold": full_overlap_exists.check() == z3.unsat,
        "current_holder_edge_bound": 4,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "critical_overlap_eliminated": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "shared capture in predecessor-duplicate terminal maps is a paid "
            "split or one minimal two-row overlap packet; signed closure remains"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
