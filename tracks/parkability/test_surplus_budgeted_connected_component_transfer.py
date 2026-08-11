"""Focused regression for the surplus-budgeted connected-component lemma."""

from pathlib import Path

try:
    from .audit_surplus_budgeted_connected_component_transfer import run
except ImportError:
    from audit_surplus_budgeted_connected_component_transfer import run


ROOT = Path(__file__).resolve().parents[2]


def test_branching_component_endpoint():
    result = run(ROOT)
    assert result["status"] == "VERIFIED"
    assert result["base_efx"] and result["final_efx"]
    assert all(result["weakly_paid"].values())
    assert all(result["strictly_paid"].values())
    assert len(result["positive_threshold_overshoots"]) == 5
    assert not result["surplus_budget_failures"]
    assert result["topology"]["signature"] == "_->r:1;c->s:1;r->c:1;r->q:1"
    assert len(result["topology"]["nontrivial_components"]) == 1


def test_claim_boundary_keeps_packet_selection_open():
    theorem = (
        ROOT / "results/SURPLUS_BUDGETED_CONNECTED_COMPONENT_TRANSFER_LEMMA_20260811.md"
    ).read_text()
    assert "arbitrary connected transfer" in theorem
    assert "does not prove that every" in theorem
    assert "close `GG`" in theorem
