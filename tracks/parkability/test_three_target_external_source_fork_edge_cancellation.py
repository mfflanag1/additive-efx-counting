"""Regression tests for the exact 3x2 fork signed-support census."""

import json
from pathlib import Path

from .audit_three_target_external_source_fork_edge_cancellation import run


ROOT = Path(__file__).resolve().parents[2]


def test_three_target_fork_census_replays():
    expected = json.loads(
        (ROOT / "results/three_target_external_source_fork_edge_cancellation_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_three_target_fork_frontier_is_exact():
    result = run(ROOT)
    assert result["status"] == "EXACT_3X2_SUPPORT_CENSUS_COMPLETE"
    assert result["patterns_checked"] == 720
    assert result["form_counts"]["R2"]["within_four"] == 78
    assert result["form_counts"]["R3"]["within_four"] == 78
    assert result["edge_distribution"]["4"] == 128
    assert len(result["feasible_patterns"]) == 156
    assert "remain open" in result["claim_boundary"]
