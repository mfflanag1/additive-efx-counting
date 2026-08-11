"""Regression tests for q-source residual reassignment."""

import json
from pathlib import Path

from .audit_q_closing_source_residual_reassignment import run


ROOT = Path(__file__).resolve().parents[2]


def test_q_source_residual_reassignment_audit_replays():
    expected = json.loads(
        (ROOT / "results/q_closing_source_residual_reassignment_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_all_six_q_source_pivots_are_covered():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["q_source_pivot_count"] == 6
    assert result["cycle_length_counts"] == {"2": 2, "3": 2, "4": 2}
    assert result["old_q_target_counts"] == {
        "external_owner": 4,
        "charity": 2,
    }
    assert all(result["checks"].values())


def test_q_source_claim_boundary_stays_open():
    result = run(ROOT)
    assert "mixed-margin closure" in result["claim_boundary"]
    assert "remain open" in result["claim_boundary"]
