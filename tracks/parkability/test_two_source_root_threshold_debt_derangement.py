from .audit_two_source_root_threshold_debt_derangement import run


def test_two_source_root_threshold_debt_derangement() -> None:
    result = run()
    assert result["status"] == (
        "TWO_SOURCE_FACE_REDUCED_TO_SINGLE_EDGE_HARD_CHAMPIONS_CYCLIC_DEBT"
    )
    assert result["two_source_graphs_checked"] == 3
    assert result["double_edge_pareto_closing_graphs"] == 1
    assert result["single_edge_surviving_graphs"] == 2
    assert len(result["hard_champion_patterns"]) == 3
    assert result["self_loop_free_debt_maps_checked"] == 8
    assert result["debt_cycle_counts"] == {"2": 6, "3": 2}
    assert result["all_debt_maps_have_nontrivial_cycle"]
    assert not result["debt_cycle_is_release_compatible_pi"]
    assert not result["full_T_L_times_theorem_closed"]
