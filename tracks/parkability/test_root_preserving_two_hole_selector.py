"""Focused regression for the root-preserving two-hole selector."""

from pathlib import Path

try:
    from .audit_root_preserving_two_hole_selector import run
except ImportError:
    from audit_root_preserving_two_hole_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_preserving_selector_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_conversion_open():
    theorem = (
        ROOT / "results/ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md"
    ).read_text()
    assert "eliminates root-facing J-exhaustion as a priority exception" in theorem
    assert "does not prove that" in theorem
