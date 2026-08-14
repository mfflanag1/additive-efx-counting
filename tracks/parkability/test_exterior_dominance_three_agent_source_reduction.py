from .audit_exterior_dominance_three_agent_source_reduction import run


def test_exterior_dominance_three_agent_source_reduction() -> None:
    result = run()
    assert result["status"] == (
        "EXTERIOR_DOMINANCE_REDUCED_TO_TWO_SOURCE_ROOT_THRESHOLD_DEBT"
    )
    assert result["three_vertex_dags"] == 25
    assert result["dag_counts_by_number_of_sources"]["3"] == 1
    assert result["gg_source_sets_before_cgm_closure"] == [[0], [0, 1], [0, 2]]
    assert result["gg_surviving_source_sets"] == [[0, 1], [0, 2]]
    assert result["unique_source_closed_by_cgm_corollary_7"]
    assert result["root_cross_safety"]
    assert result["nonroot_root_floor_preservation"]
    assert not result["full_T_L_times_theorem_closed"]
