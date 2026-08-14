from .audit_retired_packet_charge_anchor_resolution_20260814_independent import run


def test_retired_packet_charge_anchor_resolution_20260814_independent() -> None:
    result = run()
    assert result["status"] == "INDEPENDENT_T_L_TIMES_COMPLETION_REPLAY_PASSED"
    assert result["root_margin_cases_checked"] > 0
    assert result["root_margin_failures"] == 0
    assert result["packet_support_cases_checked"] > 0
    assert result["whole_packet_response_failures"] == 0
    assert result["fixed_priority_lex_cases_checked"] > 0
    assert result["fixed_priority_lex_failures"] == 0
    assert result["minimal_response_deletion_cases_checked"] > 0
    assert result["minimal_response_deletion_failures"] == 0
    assert not result["imports_primary_completion_audit"]
    assert not result["imports_root_closure_audit"]
    assert not result["imports_z3"]
    assert not result["old_later_floors_preserved"]
    assert result["controlled_floor_reset_explicit"]
    assert not result["reset_used_as_progress"]
    assert result["holder_partition_exhaustive"]
    assert result["full_T_L_times_theorem_closed"]
    assert not result["parked_T_L_perp_closed"]
    assert not result["empty_ledger_T0_closed"]
    assert not result["full_GG_closed"]
    assert not result["four_agent_EFX_closed"]
    assert not result["external_expert_reviewed"]
