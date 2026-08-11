"""Regression tests for the mutual-floater deletion trichotomy."""

import json
from pathlib import Path

from .audit_mutual_floater_deletion_or_double_critical import run


ROOT = Path(__file__).resolve().parents[2]


def test_mutual_floater_audit_replays():
    expected = json.loads(
        (ROOT / "results/mutual_floater_deletion_or_double_critical_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_mutual_floater_trichotomy_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(result["checks"].values())
    assert result["canonical_core_intersection"] == ["f"]
    assert result["root_deletion_is_disjoint"]
    assert result["q_deletion_is_disjoint"]


def test_mutual_floater_claim_boundary_stays_open():
    result = run(ROOT)
    assert "mixed-margin closure" in result["claim_boundary"]
    assert "remain open" in result["claim_boundary"]
