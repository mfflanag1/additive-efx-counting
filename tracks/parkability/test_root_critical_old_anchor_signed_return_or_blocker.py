from .audit_root_critical_old_anchor_signed_return_or_blocker import run


def test_root_critical_old_anchor_signed_return_or_blocker() -> None:
    result = run()
    assert result["status"] == (
        "CRITICAL_OLD_ANCHOR_PACKET_REDUCED_TO_SIGNED_RETURN_BLOCKER"
    )
    assert result["proper_signed_return_is_strict"]
    assert result["complete_signed_return_is_equality"]
    assert result["support_cases_checked"] > 0
    assert result["proper_signed_return_support_cases"] > 0
    assert result["equality_signed_return_support_cases"] > 0
    assert result["anchor_packet_in_signed_plus_containment_failures"] == 0
    assert not result["historical_reversibility_used"]
    assert not result["global_supplier_star_used"]
    assert not result["repeated_blocker_well_foundedness_proved"]
    assert not result["full_T_L_times_theorem_closed"]
