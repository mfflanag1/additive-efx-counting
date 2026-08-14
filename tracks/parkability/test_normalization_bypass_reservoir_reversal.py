from pathlib import Path

from .audit_normalization_bypass_reservoir_reversal import run


ROOT = Path(__file__).resolve().parents[2]


def test_normalization_bypass_reservoir_reversal_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "BYPASS_REDUCED_TO_COLLISION_OR_SAFE_PAYMENT_WALL"
    )
    assert result["selector_nonempty_from_current_safety"]
    assert result["safe_packet_pays_response_threshold"]
    assert result["unsafe_reversal_packet_paid_by_original_response"]
    assert result["collision_routes"] == [
        "proper_K_reduction", "whole_K_atomic_collision"
    ]
    assert result["ledger_free_routes"] == [
        "rank_or_PI_closure", "safe_threshold_payment_wall"
    ]
    assert not result["full_T_L_times_theorem_closed"]
