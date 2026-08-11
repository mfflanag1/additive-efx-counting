"""Focused regression for the GG rank-reset raw-potential refutation."""

from pathlib import Path

from .audit_gg_rank_reset_raw_potential_refutation import run


ROOT = Path(__file__).resolve().parents[2]


def test_exact_scale_refutation():
    result = run(ROOT)
    assert result["status"] == "EXACT_SCALE_REFUTATION"
    assert result["maximum_response_rank_before"] == 3
    assert result["maximum_response_rank_after"] == 3
    assert result["response_relation_unchanged_by_scaling"]


def test_claim_boundary_does_not_claim_gg_closure():
    result = run(ROOT)
    assert "not GG closure" in result["claim_boundary"]
