from .audit_strict_first_priority_floor_reset_admission import run


def test_strict_first_priority_floor_reset_admission() -> None:
    result = run()
    assert result["status"] == "STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMITTED"
    assert result["strict_first_coordinate_exact"]
    assert result["reset_floors_paid_exactly"]
    assert result["strong_envy_supplies_desired_deletion"]
    assert not result["old_later_floors_preserved"]
    assert not result["floor_reset_counts_as_progress"]
    assert result["all_efx_comparisons_recomputed"]
    assert result["physical_labels_retained"]
    assert not result["full_T_L_times_theorem_closed"]
