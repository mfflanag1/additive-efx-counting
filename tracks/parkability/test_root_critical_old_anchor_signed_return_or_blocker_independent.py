from .audit_root_critical_old_anchor_signed_return_or_blocker_independent import run


def test_root_critical_old_anchor_signed_return_or_blocker_independent() -> None:
    result = run()
    assert result["status"] == "INDEPENDENT_SIGNED_RETURN_MARGIN_REPLAY_PASSED"
    assert result["cases_checked"] > 0
    assert result["proper_cases"] > 0
    assert result["equality_cases"] > 0
    assert result["failures"] == 0
    assert not result["imports_primary_audit"]
    assert not result["imports_z3"]
    assert not result["repeated_blocker_well_foundedness_proved"]
    assert not result["full_T_L_times_theorem_closed"]
