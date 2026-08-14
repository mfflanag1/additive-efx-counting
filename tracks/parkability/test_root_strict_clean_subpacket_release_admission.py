from .audit_root_strict_clean_subpacket_release_admission import run


def test_root_strict_clean_subpacket_release_admission() -> None:
    result = run()
    assert result["status"] == (
        "STRICT_CLEAN_SUBPACKET_RELEASE_ADMITTED_EQUALITY_OPEN"
    )
    assert result["margin_identity_exact"]
    assert result["strict_test_exact"]
    assert result["physical_support_cases_checked"] > 0
    assert result["proper_split_whole_packet_hits"] == 0
    assert result["full_return_proper_deletions_checked"] > 0
    assert result["singleton_target_never_strongly_envied"]
    assert result["weak_atomwise_charge_exact"]
    assert result["summed_charge_exact"]
    assert not result["historical_reversibility_used"]
    assert not result["root_equality_closed"]
    assert not result["full_T_L_times_theorem_closed"]
