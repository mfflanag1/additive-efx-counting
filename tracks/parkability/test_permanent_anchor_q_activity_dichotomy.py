"""Focused regression for permanent-anchor q representation."""

from pathlib import Path

try:
    from .audit_permanent_anchor_q_activity_dichotomy import run
except ImportError:
    from audit_permanent_anchor_q_activity_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_every_active_q_is_anchor_representable():
    result = run(ROOT)
    counts = result["counts"]
    assert result["status"] == "ALL_CLASSIFIED"
    assert counts["relations"] == 1 << 14
    assert counts["q_active"] == counts["active_q_anchor_maximum_representable"]
    assert counts["uncovered"] == 0


def test_rank_gap_does_not_break_q_representation():
    result = run(ROOT)
    counts = result["counts"]
    assert counts["anchor_rank_gap"] > 0
    assert counts["anchor_rank_gap_q_active"] > 0
    assert all(
        not example["q_active"] or example["q_anchor_maximum_representable"]
        for example in result["rank_gap_examples"]
    )


def test_claim_boundary_keeps_source_inactive_closure_open():
    result = run(ROOT)
    assert "degree-zero source-inactive closure" in result["claim_boundary"]
    assert "GG closure" in result["claim_boundary"]
