"""Regression test for the predecessor overlap bicriteria frontier."""

import json
from pathlib import Path

from .audit_predecessor_cross_exchange_overlap_bicriteria import run


ROOT = Path(__file__).resolve().parents[2]


def test_predecessor_overlap_bicriteria_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/predecessor_cross_exchange_overlap_bicriteria_audit.json").read_text()
    )
    assert result == expected
    assert result["missing_payment_equivalence"]
    assert result["predecessor_payment_equivalence"]
    assert result["full_overlap_always_meets_missing_threshold"]
    assert result["current_holder_edge_bound"] == 4
    assert not result["frozen_supplier_edge_bound_proved"]
    assert not result["observer_safety_proved"]
    assert not result["critical_overlap_eliminated"]
    assert not result["fixed_u_theorem_proved"]
