"""Focused regression for the captured-bottom compensation chain."""

import json
from pathlib import Path

from .audit_captured_bottom_external_compensation_chain import run


ROOT = Path(__file__).resolve().parents[2]


def test_captured_bottom_compensation_replays():
    expected = json.loads(
        (ROOT / "results/captured_bottom_external_compensation_chain_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_keeps_top_handoffs_open():
    theorem = (
        ROOT / "results/CAPTURED_BOTTOM_EXTERNAL_COMPENSATION_CHAIN_LEMMA_20260811.md"
    ).read_text()
    assert "q -> a -> r" in theorem
    assert "does not terminate" in theorem
