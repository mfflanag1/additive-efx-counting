"""Regression tests for the 2x1 Hall-star support frontier."""

import json
from pathlib import Path

from .audit_two_target_external_source_four_edge_support_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_two_target_support_frontier_replays():
    expected = json.loads(
        (ROOT / "results/two_target_external_source_four_edge_support_frontier_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_two_target_support_frontier_is_exact():
    result = run(ROOT)
    assert result["status"] == "EXACT_SUPPORT_FRONTIER_PROVED"
    assert result["no_incoming_packet_edge_count"] == 5
    assert result["feasible_case_count"] > 0
    assert any(not record["within_four"] for record in result["records"])
    assert "remain open" in result["claim_boundary"]
