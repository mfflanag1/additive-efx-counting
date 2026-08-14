from .audit_root_global_exterior_subpacket_sacrifice_independent import run


def test_root_global_exterior_subpacket_sacrifice_independent() -> None:
    result = run()
    assert result["status"] == (
        "INDEPENDENT_INTEGER_REPLAY_CONFIRMS_GLOBAL_ROOT_CUT_AND_BASE_CONTAINMENT"
    )
    assert result["strict_cases"] > 0
    assert result["strict_bad_packet_hits"] == 0
    assert result["equality_cases"] > 0
    assert result["equality_identity_failures"] == 0
    assert result["equality_spread_failures"] == 0
    assert result["underpayment_cases"] > 0
    assert result["fully_underpaid_recurrent_states"] > 0
    assert result["base_containment_failures"] == 0
    assert not result["imports_primary_audit"]
    assert not result["full_T_L_times_theorem_closed"]
