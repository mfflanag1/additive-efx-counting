"""Focused regression for the externally-safe connected path lemma."""

from pathlib import Path

try:
    from .audit_externally_safe_connected_path_transfer import run
except ImportError:
    from audit_externally_safe_connected_path_transfer import run


ROOT = Path(__file__).resolve().parents[2]


def test_path_transfer_and_frozen_exemplars():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["scalar_records"].values()) == {"unsat"}
    assert {record["signature"] for record in result["profile_records"]} == {
        "c->r:1",
        "q->r:1;r->c:2",
    }
    for record in result["profile_records"]:
        assert not record["external_safety_failures"]
        assert all(record["paid_non_source"].values())
        assert record["source_direct_efx"]
        assert record["lex_endpoint"]
        assert record["connected"]


def test_claim_boundary_keeps_packet_selection_open():
    theorem = (
        ROOT / "results/EXTERNALLY_SAFE_CONNECTED_PATH_TRANSFER_LEMMA_20260811.md"
    ).read_text()
    assert "externally common-safe" in theorem
    assert "different pivot states" not in theorem
    assert "does not prove that every terminal polarity" in theorem
