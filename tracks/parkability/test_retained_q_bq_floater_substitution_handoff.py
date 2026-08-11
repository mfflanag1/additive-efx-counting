"""Regression tests for retained-q Bq floater substitution."""

import json
from pathlib import Path

from .audit_retained_q_bq_floater_substitution_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_retained_q_bq_substitution_audit_replays():
    expected = json.loads(
        (ROOT / "results/retained_q_bq_floater_substitution_handoff_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_retained_q_bq_substitution_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(result["checks"].values())
    assert result["root_anchor_and_substituted_q_target_disjoint"]
    assert result["root_anchor_releases_complete_bq"]


def test_retained_q_bq_claim_boundary_stays_open():
    result = run(ROOT)
    assert "mixed-margin closure" in result["claim_boundary"]
    assert "remain open" in result["claim_boundary"]
