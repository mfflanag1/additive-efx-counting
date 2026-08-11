"""Focused regression for minimal dual-pool extraction."""

import json
from pathlib import Path

from .audit_dual_pool_minimal_core_extraction import run


ROOT = Path(__file__).resolve().parents[2]


def test_minimal_dual_core_extraction_replays():
    expected = json.loads(
        (ROOT / "results/dual_pool_minimal_core_extraction_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_keeps_source_compensation_open():
    theorem = (
        ROOT / "results/DUAL_POOL_MINIMAL_CORE_EXTRACTION_LEMMA_20260811.md"
    ).read_text()
    assert "two-row captured packet" in theorem
    assert "does not compensate" in theorem
