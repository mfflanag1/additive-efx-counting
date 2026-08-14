"""Regression tests for four-placement singleton response transport."""

import json
from pathlib import Path

from .audit_four_placement_singleton_response_transport import run


ROOT = Path(__file__).resolve().parents[2]


def test_four_placement_transport_replays():
    expected = json.loads(
        (ROOT / "results/four_placement_singleton_response_transport_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_four_placement_claim_boundary_remains_open():
    result = run(ROOT)
    assert result["status"] == "CAP_FREE_TRANSPORT_PROVED"
    assert all(result["desire_transport_checks"].values())
    assert all(result["safety_floor_checks"].values())
    assert result["parking_band_forced"]
    assert "remain open" in result["claim_boundary"]
