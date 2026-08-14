from .audit_two_source_singleton_source_elimination_ggs_switch import run


def test_two_source_singleton_source_elimination_ggs_switch() -> None:
    result = run()
    assert result["status"] == (
        "SINGLETON_SOURCE_PAIR_CLOSED_SOLE_SURVIVOR_FORCES_NONROOT_GGS"
    )
    assert result["source_pair_orientations_checked"] == 4
    assert result["singleton_source_contradictions"] == 2
    assert result["forced_ggs_orientations"] == 2
    assert result["surviving_source_pair"] == ["c", "q"]
    assert result["forced_cycle_word"] == "GGS"
    assert not result["forced_cycle_is_release_compatible_pi"]
    assert not result["ledger_preserving_cycle_switch_proved"]
    assert not result["full_T_L_times_theorem_closed"]
