from pathlib import Path

from .audit_retired_packet_collision_atomic_normal_form import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_collision_atomic_normal_form_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "T_L_TIMES_REDUCED_TO_THREE_ATOMIC_SURVIVORS"
    assert result["recipient_capture_identity"]
    assert result["holder_payment_identity"]
    assert result["response_intersection_trichotomy"]
    assert len(result["typed_failure_routes"]) == 16
    assert result["atomic_survivors"] == [
        "atomwise_critical_whole_packet_bilateral_deadlock",
        "root_facing_anchor_critical_packet",
        "safe_center_three_offer_same_source_star",
    ]
    assert not result["full_T_L_times_theorem_closed"]
