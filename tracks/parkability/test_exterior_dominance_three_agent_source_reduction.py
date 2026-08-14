from .audit_exterior_dominance_three_agent_source_reduction import run


def test_exterior_dominance_three_agent_source_reduction() -> None:
    result = run()
    assert result["status"] == "EXTERIOR_DOMINANCE_REDUCED_TO_AT_MOST_TWO_SOURCES"
    assert result["three_vertex_dags"] == 25
    assert result["dag_counts_by_number_of_sources"]["3"] == 1
    assert result["gg_surviving_source_sets"] == [[0], [0, 1], [0, 2]]
    assert result["root_cross_safety"]
    assert result["nonroot_root_floor_preservation"]
    assert not result["full_T_L_times_theorem_closed"]
