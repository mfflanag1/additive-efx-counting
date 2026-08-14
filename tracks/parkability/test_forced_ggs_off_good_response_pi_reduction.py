from .audit_forced_ggs_off_good_response_pi_reduction import run


def test_forced_ggs_off_good_response_pi_reduction() -> None:
    result = run()
    assert result["status"] == "OFF_GOOD_Q_AND_Q_TO_S_SOURCE_PROFILES_PI_CLOSED"
    assert result["off_good_role_profiles_checked"] == 6
    assert result["pi_closed_profiles"] == 3
    assert result["surviving_profiles"] == [["c", "c"], ["c", "s"], ["q", "c"]]
    assert result["on_good_profiles_closed"] == 0
    assert not result["overlapping_f_edges_declared_pi"]
    assert not result["full_T_L_times_theorem_closed"]
