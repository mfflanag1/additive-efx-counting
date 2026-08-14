"""Regression test for the liquidated-root response frontier."""

import json
from pathlib import Path

from .audit_fixed_u_liquidated_root_three_placement_response_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_liquidated_root_response_frontier_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/fixed_u_liquidated_root_three_placement_response_frontier_audit.json").read_text()
    )
    assert result == expected
    assert result["maximum_edge_count"] <= 4
    assert result["root_payment_equivalence"]
    assert not result["controlled_floor_reset_used"]
    assert not result["root_capture_eliminated"]
    assert not result["decorated_recurrence_closed"]
