from .audit_nonroot_current_whole_hit_envelope_descent import run


def test_nonroot_current_whole_hit_envelope_descent() -> None:
    result = run()
    assert result["status"] == (
        "NONROOT_CURRENT_WHOLE_HIT_TERMINATES_OR_RESELECTS_ROOT"
    )
    assert result["nested_support_chains_checked"] > 0
    assert result["maximum_nonpacket_deletions_checked"] > 0
    assert result["singleton_terminal_threshold_zero"]
    assert result["released_source_and_holder_residual_avoid_named_packet"]
    assert not result["full_T_L_times_theorem_closed"]
