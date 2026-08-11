"""Focused regression for the reused-top canonical-core selector."""

import json
from pathlib import Path

from .audit_reused_top_canonical_core_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_reused_top_selector_replays():
    expected = json.loads(
        (ROOT / "results/reused_top_canonical_core_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_requires_a_real_family_change():
    theorem = (
        ROOT / "results/REUSED_TOP_CANONICAL_CORE_SELECTOR_LEMMA_20260811.md"
    ).read_text()
    assert "cannot cycle" in theorem.replace("\n", " ")
    assert "does not eliminate a change of source" in theorem.replace("\n", " ")
