"""Focused regression for the removed-top retention potential."""

import json
from pathlib import Path

from .audit_flower_removed_top_retention_potential import run


ROOT = Path(__file__).resolve().parents[2]


def test_removed_top_retention_replays():
    expected = json.loads(
        (ROOT / "results/flower_removed_top_retention_potential_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_keeps_capture_conversion_open():
    theorem = (
        ROOT / "results/FLOWER_REMOVED_TOP_RETENTION_POTENTIAL_LEMMA_20260811.md"
    ).read_text()
    assert "persistent potential" in theorem
    assert "does not convert" in theorem.replace("\n", " ")
