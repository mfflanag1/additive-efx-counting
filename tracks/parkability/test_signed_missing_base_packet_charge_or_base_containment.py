from .audit_signed_missing_base_packet_charge_or_base_containment import run


def test_signed_missing_base_packet_charge_or_base_containment() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_PACKET_BASE_CONTAINED_OR_SIGNED_RETURN_HAS_NAMED_BLOCKER"
    )
    assert result["proper_intersection_strict_margin"]
    assert result["support_cases_checked"] > 0
    assert result["proper_incoming_intersection_cases"] > 0
    assert result["complete_incoming_intersection_cases"] > 0
    assert result["empty_incoming_intersection_cases"] > 0
    assert result["empty_intersection_base_containment_failures"] == 0
    assert not result["failed_return_charge_is_progress_by_itself"]
    assert not result["global_multilabel_well_foundedness_proved"]
    assert not result["base_contained_face_closed"]
    assert not result["full_T_L_times_theorem_closed"]
