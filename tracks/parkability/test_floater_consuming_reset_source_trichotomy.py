"""Focused regression for floater-consuming reset routing."""

from pathlib import Path

try:
    from .audit_floater_consuming_reset_source_trichotomy import run
except ImportError:
    from audit_floater_consuming_reset_source_trichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_floater_reset_trichotomy_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["source_labels_exhaustive"]
    assert len(result["source_cases"]) == 4
    assert set(result["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_routed_branches_open():
    theorem = (
        ROOT / "results/FLOATER_CONSUMING_RESET_SOURCE_TRICHOTOMY_20260811.md"
    ).read_text()
    assert "Floater-free response" in theorem
    assert "Floater-critical response" in theorem
    assert "does not terminate the root, `q`, or external" in theorem
