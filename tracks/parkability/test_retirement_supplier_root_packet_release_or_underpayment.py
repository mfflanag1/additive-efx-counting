from .audit_retirement_supplier_root_packet_release_or_underpayment import run


def test_retirement_supplier_root_packet_release_or_underpayment() -> None:
    result = run()
    assert result["status"] == (
        "STRICT_ROOT_PACKET_RELEASE_ADMITTED_EQUALITY_OPEN"
    )
    assert result["release_margin_identity_exact"]
    assert result["strict_payment_keeps_root_above_base"]
    assert result["empty_return_strict_when_packet_below_surplus"]
    assert result["packet_price_no_larger_than_envelope_price"]
    assert result["complete_exterior_support_cases_checked"] > 0
    assert result["historical_recipient_identified"]
    assert not result["historical_return_transition_admitted"]
    assert result["clean_controlled_release_admitted"]
    assert result["return_owner_may_be_sacrificed_if_transition_admitted_and_root_strict"]
    assert not result["full_T_L_times_theorem_closed"]
