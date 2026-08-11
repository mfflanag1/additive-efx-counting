"""Focused regression for the dual-anchor root-paid selector."""

import json
from pathlib import Path

from .audit_flower_dual_anchor_root_paid_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_dual_anchor_selector_replays():
    expected = json.loads(
        (ROOT / "results/flower_dual_anchor_root_paid_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in expected["records"])


def test_claim_boundary_keeps_terminal_branches_open():
    theorem = (
        ROOT / "results/FLOWER_DUAL_ANCHOR_ROOT_PAID_SELECTOR_LEMMA_20260811.md"
    ).read_text()
    assert "dual-pool deficit" in theorem
    assert "does not pay the root" in theorem
    assert "does not" in theorem
