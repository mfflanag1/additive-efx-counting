from .audit_protected_floor_whole_hit_currentization_or_path_hall import run


def test_protected_floor_whole_hit_currentization_or_path_hall() -> None:
    result = run()
    assert result["status"] == (
        "PROTECTED_WHOLE_HIT_REDUCED_TO_SOURCE_INACTIVE_DEBT_OR_CURRENT_PATH_HALL"
    )
    assert result["source_inactive_debt_exact"]
    assert result["inactive_excludes_current_subset"]
    assert result["path_sink_identity_exact_with_empty_residual"]
    assert result["whole_hit_support_cases_checked"] > 0
    assert result["empty_residual_cases_checked"] > 0
    assert result["five_path_cut_reused_exactly"]
    assert not result["full_T_L_times_theorem_closed"]
