"""Regression tests for singleton-relay response localization."""

import json
from pathlib import Path

from .audit_singleton_relay_cross_state_response_localization import run


ROOT = Path(__file__).resolve().parents[2]


def test_singleton_relay_localization_replays():
    expected = json.loads(
        (ROOT / "results/singleton_relay_cross_state_response_localization_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_singleton_relay_claim_boundary_remains_open():
    result = run(ROOT)
    assert result["status"] == "CAP_FREE_LOCALIZATION_PROVED"
    assert all(result["checks"].values())
    assert result["isolated_singleton_critical_separator_feasible"]
    assert "remain open" in result["claim_boundary"]
