from .audit_root_safe_whole_hit_complete_pool_reduction import run


def test_root_safe_whole_hit_complete_pool_reduction() -> None:
    result = run()
    assert result["status"] == (
        "ALL_TYPED_SAFE_WHOLE_HITS_REDUCED_TO_ROOT_POOL_UNDERPAYMENT_OR_EQUALITY"
    )
    assert result["response_side_above_surplus"]
    assert result["complement_side_above_surplus"]
    assert result["pool_margin_identity_exact"]
    assert result["strict_pool_is_root_strict"]
    assert result["equality_pool_is_root_base"]
    assert not result["current_desire_required"]
    assert not result["arbitrary_recipient_allowed"]
    assert result["named_typed_recipient_required"]
    assert len(result["typed_branches_unified"]) == 3
    assert not result["full_T_L_times_theorem_closed"]
