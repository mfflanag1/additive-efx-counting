"""Regression test for duplicate-omission payment."""

import json
from pathlib import Path

from .audit_missing_supplier_duplicate_omission_four_edge_payment import run


ROOT = Path(__file__).resolve().parents[2]


def test_duplicate_omission_payment_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/missing_supplier_duplicate_omission_four_edge_payment_audit.json").read_text()
    )
    assert result == expected
    assert result["covered_maps"] == 24
    assert result["foreign_supplier_maps"] == 24
    assert result["current_holder_move_count_histogram"] == {"4": 24}
    assert result["represented_source_payment"]
    assert result["missing_source_payment"]
    assert not result["original_supplier_edge_bound_proved"]
    assert not result["observer_safety_proved"]
    assert not result["paid_repeat_closed"]
