"""Focused regression for the exact two-by-two Hall classification."""

from pathlib import Path

try:
    from .audit_two_by_two_response_hall_normal_form import run
except ImportError:
    from audit_two_by_two_response_hall_normal_form import run


ROOT = Path(__file__).resolve().parents[2]


def test_two_by_two_hall_normal_form_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["relation_count"] == 16
    assert result["classification_counts"] == {
        "COVERING_MATCHING": 7,
        "EMPTY_TARGET": 7,
        "COMMON_SINGLETON": 2,
    }
    assert result["paired_full_sdr_count"] == 49
    assert result["paired_two_cycle_count"] > 0
    assert result["uncovered_pair_count"] == 0


def test_claim_boundary_keeps_star_elimination_open():
    theorem = (
        ROOT / "results/TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md"
    ).read_text()
    assert "two-owner response cycle" in theorem
    assert "single-source two-target star" in theorem
    assert "does not eliminate the empty-target" in theorem
    assert "lower-dimensional pivot" in theorem
