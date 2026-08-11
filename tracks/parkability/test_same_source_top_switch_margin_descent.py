"""Focused regression for same-source top-switch margin descent."""

import json
from pathlib import Path

from .audit_same_source_top_switch_margin_descent import run


ROOT = Path(__file__).resolve().parents[2]


def test_same_source_margin_descent_replays():
    expected = json.loads(
        (ROOT / "results/same_source_top_switch_margin_descent_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_names_exact_reuse_gate():
    theorem = (
        ROOT / "results/SAME_SOURCE_TOP_SWITCH_MARGIN_DESCENT_LEMMA_20260811.md"
    ).read_text()
    assert "K\\subseteqU" in theorem.replace(" ", "")
    assert "does not eliminate a reused packet" in theorem.replace("\n", " ")
