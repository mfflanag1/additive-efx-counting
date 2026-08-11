"""Focused regression for recurrence disjointness or overlap polarity."""

from pathlib import Path

try:
    from .audit_hole_recurrence_disjoint_or_polarity import run
except ImportError:
    from audit_hole_recurrence_disjoint_or_polarity import run


ROOT = Path(__file__).resolve().parents[2]


def test_recurrence_support_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["scalar_records"].values()) == {"unsat"}
    assert {record["length"] for record in result["simple_cycle_records"]} == {2, 3}
    assert result["support_records"][
        "failed_common_safety_routes_to_unsafe_core_augmentation"
    ]


def test_claim_boundary_keeps_dynamic_gate_open():
    theorem = (
        ROOT / "results/HOLE_RECURRENCE_DISJOINT_OR_POLARITY_LEMMA_20260811.md"
    ).read_text()
    assert "release-compatible PI component" in theorem
    assert "different valuation rows" in theorem
    assert "value above base alone" in theorem
    assert "does not prove that every" in theorem
    assert "dynamic pivot sequence preserves" in theorem
