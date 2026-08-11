"""Focused regression for global root-donation blockers."""

from pathlib import Path

try:
    from .audit_root_donation_global_blocker import run
except ImportError:
    from audit_root_donation_global_blocker import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_donation_blocker_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["scalar_records"].values()) == {"unsat"}
    assert result["wall_localization"]["root_observer_failure"] == "impossible"
    assert result["wall_localization"]["unchanged_observer_targets"] == [
        "enlarged_root_only"
    ]


def test_claim_boundary_keeps_path_termination_open():
    theorem = (
        ROOT / "results/ROOT_DONATION_GLOBAL_BLOCKER_LEMMA_20260811.md"
    ).read_text()
    assert "nonempty root donation" in theorem
    assert "q -> r -> c" in theorem
    assert "does not show that a terminal weighted-Hall packet" in theorem
