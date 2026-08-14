from .audit_nonroot_safe_whole_hit_envelope_descent import run


def test_nonroot_safe_whole_hit_envelope_descent() -> None:
    result = run()
    assert result["status"] == "ALL_COMMON_SAFE_NONROOT_WHOLE_HITS_TERMINATE"
    assert result["support_cases_checked"] > 0
    assert result["strict_nested_steps_checked"] > 0
    assert result["singleton_terminal_threshold_zero"]
    assert not result["current_desire_required"]
    assert not result["arbitrary_recipient_allowed"]
    assert result["named_typed_recipient_required"]
    assert result["protected_floor_source_inactive_branch_covered"]
    assert not result["full_T_L_times_theorem_closed"]
