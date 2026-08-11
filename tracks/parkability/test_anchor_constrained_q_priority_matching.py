"""Focused regression for anchor-constrained q-priority matching."""

from pathlib import Path

from .audit_anchor_constrained_q_priority_matching import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchor_matching_graphs_are_exhausted():
    result = run(ROOT)
    assert result["status"] == "ALL_CLASSIFIED"
    assert result["counts"]["relations"] == 1 << 14
    assert result["counts"]["uncovered"] == 0


def test_claim_boundary_keeps_analytic_handoffs_open():
    result = run(ROOT)
    assert "anchor-rank-gap" in result["claim_boundary"]
    assert "source-inactive reset recurrence" in result["claim_boundary"]
