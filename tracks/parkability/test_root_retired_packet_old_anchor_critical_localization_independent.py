from .audit_root_retired_packet_old_anchor_critical_localization_independent import run


def test_root_retired_packet_old_anchor_critical_localization_independent() -> None:
    result = run()
    assert result["status"] == "INDEPENDENT_CRITICAL_ANCHOR_FORK_REPLAY_PASSED"
    assert result["cases_checked"] > 0
    assert result["removable_cases"] > 0
    assert result["critical_cases"] > 0
    assert result["equality_cases_excluded_by_nondegeneracy"] > 0
    assert result["failures"] == 0
    assert result["current_target_cases"] > 0
    assert result["current_target_critical_cases"] > 0
    assert result["current_target_implication_failures"] == 0
    assert not result["imports_primary_audit"]
    assert not result["imports_z3"]
    assert not result["full_T_L_times_theorem_closed"]
