"""Regression tests for the four-owner minimal Hall-defect classification."""

import json
from pathlib import Path

from .audit_four_owner_nonself_minimal_hall_defect_cycle import run


ROOT = Path(__file__).resolve().parents[2]


def test_four_owner_hall_defect_replays():
    expected = json.loads(
        (ROOT / "results/four_owner_nonself_minimal_hall_defect_cycle_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_all_internal_defects_have_short_cycles():
    result = run(ROOT)
    assert result["status"] == "ALL_MINIMAL_DEFECTS_CLASSIFIED"
    assert result["graphs_checked"] == 4096
    assert result["internal_defect_cycle_lengths"] == [2, 3]
    assert set(result["shape_counts"]) <= {"2x1", "3x2", "4x3"}
    assert "remain open" in result["claim_boundary"]
