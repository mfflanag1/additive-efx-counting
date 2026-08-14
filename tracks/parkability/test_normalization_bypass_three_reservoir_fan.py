from pathlib import Path

from .audit_normalization_bypass_three_reservoir_fan import run


ROOT = Path(__file__).resolve().parents[2]


def test_normalization_bypass_three_reservoir_fan_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ALL_UNSAFE_FAN_ALWAYS_HAS_SUPPLIER_CLOSED_PI_CYCLE"
    )
    assert result["source_assignments_checked"] == 324
    assert result["supplier_cycle_assignments"] == 324
    assert result["full_source_route"] == "rank_four_current_response_EFX"
    assert result["cycle_route"] == "release_compatible_PI_cycle"
    assert result["survivor"] == "safe_threshold_payment_branch_only"
    assert not result["full_T_L_times_theorem_closed"]
