from .audit_base_contained_retired_packet_exterior_donation_split import run


def test_base_contained_retired_packet_exterior_donation_split() -> None:
    result = run()
    assert result["status"] == (
        "EXTERIOR_DONATION_STRICT_ADMITTED_DOMINANCE_REMAINS"
    )
    assert result["support_cases_checked"] > 0
    assert result["singleton_root_target_ledger_hits"] == 0
    assert result["exact_charge_cases_checked"] == 6
    assert result["admissible_transition_proved"]
    assert not result["full_T_L_times_theorem_closed"]
