from .audit_supplier_aligned_base_donation_packet_spread import run


def test_supplier_aligned_base_donation_packet_spread() -> None:
    result = run()
    assert result["status"] == (
        "SUPPORT_SPREAD_GENERAL_ADMISSION_OPEN_EQUALITY_FACE_ADMITTED"
    )
    assert result["multi_surplus_cases_checked"] > 0
    assert result["multi_surplus_whole_target_hits"] == 0
    assert result["singleton_whole_hit_target_cells"] in ([], [0])
    assert result["singleton_proper_whole_packet_response_residuals_checked"] > 0
    assert result["off_packet_donation_cases_checked"] > 0
    assert result["off_packet_whole_target_hits"] == 0
    assert not result["admissible_transition_proved"]
    assert result["equality_face_transition_admitted"]
    assert not result["full_T_L_times_theorem_closed"]
