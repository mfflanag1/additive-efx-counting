from pathlib import Path

from .audit_target_envelope_protected_pair_or_star import run


ROOT = Path(__file__).resolve().parents[2]


def test_target_envelope_protected_pair_or_star_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "SAFE_PAYMENT_WALL_REDUCED_TO_TWO_HOLE_OR_THREE_OFFER_STAR"
    )
    assert result["protected_packet_pays_floor_and_target_response"]
    assert result["unsafe_center_forces_supplied_two_cycle"]
    assert result["abstract_labels_checked"] == 64
    assert result["route_counts"] == {
        "all_unsafe_PI": 27,
        "protected_pair": 28,
        "distinct_response_pair": 8,
        "same_source_star": 1,
    }
    assert result["sole_new_survivor"] == (
        "safe_center_three_offer_same_source_star"
    )
    assert not result["full_T_L_times_theorem_closed"]
