from .audit_root_equality_base_restoration_packet_spread_admission import run


def test_root_equality_base_restoration_packet_spread_admission() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_PACKET_PRICE_EQUALITY_ELIMINATED_STRICT_UNDERPAYMENT_REMAINS"
    )
    assert result["leave_one_strict_identity"]
    assert result["singleton_offpacket_root_gain"]
    assert result["packet_spread_cases_checked"] > 0
    assert result["proper_split_whole_packet_hits"] == 0
    assert result["singleton_offpacket_cases_checked"] > 0
    assert result["strict_atomwise_charge_exact"]
    assert result["other_retired_label_may_change"]
    assert not result["global_multilabel_well_foundedness_proved"]
    assert not result["full_T_L_times_theorem_closed"]
