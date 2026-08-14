from .audit_retired_packet_charge_anchor_checkpoint_20260814 import run


def test_retired_packet_charge_anchor_checkpoint_20260814() -> None:
    result = run()
    assert result["status"] == "CURRENT_WHOLE_HIT_REDUCED_TO_FIVE_PATH_HALL_CUT"
    assert result["conditional_global_candidates_downgraded"]
    assert result["current_response_path_family_exhausted"]
    assert not result["protected_floor_response_closed"]
    assert not result["normalization_bypass_closed"]
    assert not result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]
