"""Regression test for the liquidated-root full-source swap."""

import json
from pathlib import Path

from .audit_liquidated_root_response_full_source_swap_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_full_source_swap_frontier_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/liquidated_root_response_full_source_swap_frontier_audit.json").read_text()
    )
    assert result == expected
    assert result["maximum_edge_count"] <= 4
    assert result["root_payment_equivalence"]
    assert result["failure_implies_strict_direct_safety"]
    assert not result["direct_safety_contradicted"]
    assert not result["decorated_recurrence_closed"]
