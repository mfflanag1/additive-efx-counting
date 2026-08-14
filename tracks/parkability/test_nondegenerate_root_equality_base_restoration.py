from pathlib import Path

from .audit_nondegenerate_root_equality_base_restoration import run


ROOT = Path(__file__).resolve().parents[2]


def test_nondegenerate_root_equality_base_restoration() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ROOT_EQUALITY_COLLAPSES_TO_UNIQUE_BASE_RESTORATION"
    )
    assert result["transfer_equals_current_minus_base"]
    assert result["return_equals_base_minus_current"]
    assert result["retained_packet_equals_packet_intersect_base"]
    assert result["signed_surplus_identity"]
    assert result["retained_positive_makes_full_payment_strictly_larger"]
    assert result["remaining_separator"] == (
        "base_crossing_restoration_hitting_cut_or_root_payment_deficiency"
    )
    assert not result["full_T_L_times_theorem_closed"]
