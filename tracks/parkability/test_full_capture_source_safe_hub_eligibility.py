"""Focused regression for source-safe full-capture hub eligibility."""

import json
from pathlib import Path

from .audit_full_capture_source_safe_hub_eligibility import run


ROOT = Path(__file__).resolve().parents[2]


def test_source_safe_hub_eligibility_replays():
    expected = json.loads(
        (ROOT / "results/full_capture_source_safe_hub_eligibility_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_preserves_split_and_open_endpoints():
    theorem = (
        ROOT / "results/FULL_CAPTURE_SOURCE_SAFE_HUB_ELIGIBILITY_LEMMA_20260810.md"
    ).read_text()
    assert "source-safe" in theorem
    assert "strictly separated" in theorem
    assert "remain open" in theorem.replace("\n", " ")
