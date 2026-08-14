from .audit_root_whole_hit_anchor_or_balanced_path_hall import run


def test_root_whole_hit_anchor_or_balanced_path_hall() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_WHOLE_HIT_REDUCED_TO_ANCHOR_OR_BALANCED_FIVE_PATH_CUT"
    )
    assert result["root_value_partition_exhaustive"]
    assert result["response_side_strictly_above_surplus"]
    assert result["complement_strictly_above_surplus"]
    assert result["sink_margin_identity_exact"]
    assert result["discounted_price_positive"]
    assert result["root_equality_boundary_retained"]
    assert result["five_path_cut_reused_exactly"]
    assert not result["full_T_L_times_theorem_closed"]
