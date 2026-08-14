from .audit_base_contained_signed_reset_one_good_root_normal_form import run


def test_base_contained_signed_reset_one_good_root_normal_form() -> None:
    result = run()
    assert result["status"] == (
        "BASE_CONTAINED_PACKET_NORMALIZED_TO_ONE_GOOD_ON_OFF_RESPONSE"
    )
    assert result["reset_root_strict"]
    assert result["loss_band_equivalence_forward"]
    assert result["support_cases_checked"] > 0
    assert result["whole_packet_response_cases_checked"] > 0
    assert result["bad_residual_support_cases"] == 0
    assert result["on_good_whole_response_cases"] > 0
    assert result["off_good_whole_response_cases"] > 0
    assert result["exact_base_response_cases"] > 0
    assert result["new_label_or_exact_one_good_repeat"]
    assert not result["on_good_loss_band_closed"]
    assert not result["off_good_base_response_closed"]
    assert not result["global_multilabel_well_foundedness_proved"]
    assert not result["full_T_L_times_theorem_closed"]
