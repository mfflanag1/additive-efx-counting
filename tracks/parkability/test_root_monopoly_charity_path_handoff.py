"""Focused regression for the root-monopoly complete-path handoff."""

from pathlib import Path

try:
    from .audit_root_monopoly_charity_path_handoff import run
except ImportError:
    from audit_root_monopoly_charity_path_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_monopoly_handoff_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["support_partition_valid"]
    assert result["permanent_root_anchor_retained"]
    assert set(result["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_sacrificed_q_reset_open():
    theorem = (
        ROOT / "results/ROOT_MONOPOLY_CHARITY_PATH_HANDOFF_LEMMA_20260811.md"
    ).read_text()
    assert "root-monopoly pair is therefore not an additional terminal" in theorem
    assert "does not terminate the resulting root-anchored sacrificed-`q`" in theorem
