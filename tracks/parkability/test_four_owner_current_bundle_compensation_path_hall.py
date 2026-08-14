from .audit_four_owner_current_bundle_compensation_path_hall import run


def test_four_owner_current_bundle_compensation_path_hall() -> None:
    result = run()
    assert result["status"] == "ALL_FIVE_SIMPLE_COMPENSATION_PATHS_EXHAUSTED"
    assert result["boolean_edge_assignments_checked"] == 128
    assert result["no_path_iff_displayed_hall_cut"]
    assert all(value > 0 for value in result["path_success_counts"].values())
    assert result["long_path_support_conserved"]
    assert result["new_holder_target_avoids_named_packet"]
    assert not result["full_T_L_times_theorem_closed"]
