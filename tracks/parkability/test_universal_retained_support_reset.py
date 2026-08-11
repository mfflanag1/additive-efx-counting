"""Focused regression for universal retained-support resets."""

from pathlib import Path

try:
    from .audit_universal_retained_support_reset import run
except ImportError:
    from audit_universal_retained_support_reset import run


ROOT = Path(__file__).resolve().parents[2]


def test_universal_reset_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["support_partition_valid"]
    assert set(result["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_two_reset_gates_open():
    theorem = (
        ROOT / "results/UNIVERSAL_RETAINED_SUPPORT_RESET_LEMMA_20260811.md"
    ).read_text()
    assert "no such reset decreases the retained" in theorem
    assert "retained core consuming the shared floater" in theorem
    assert "does not eliminate floater-consuming cores" in theorem
