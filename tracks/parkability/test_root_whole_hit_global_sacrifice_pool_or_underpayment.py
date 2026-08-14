from .audit_root_whole_hit_global_sacrifice_pool_or_underpayment import run


def test_root_whole_hit_global_sacrifice_pool_or_underpayment() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_CURRENT_WHOLE_HIT_REDUCED_TO_AGGREGATE_UNDERPAYMENT_OR_EQUALITY"
    )
    assert result["root_margin_identity_exact"]
    assert result["strict_pool_keeps_root_above_base"]
    assert result["equality_pool_returns_root_to_base"]
    assert result["physical_pool_allocations_checked"] > 0
    assert result["root_and_charity_targets_avoid_named_packet"]
    assert not result["full_T_L_times_theorem_closed"]
