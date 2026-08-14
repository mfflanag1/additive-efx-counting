from .audit_root_retired_packet_old_anchor_critical_localization import run


def test_root_retired_packet_old_anchor_critical_localization() -> None:
    result = run()
    assert result["status"] == "ROOT_PACKET_LOCALIZED_TO_OLD_ANCHOR_CRITICAL_ATOMS"
    assert result["off_anchor_atom_clean_release_is_root_strict"]
    assert result["noncritical_anchor_atom_clean_release_is_root_strict"]
    assert result["critical_atom_exceeds_anchor_surplus"]
    assert result["critical_atom_exceeds_current_surplus"]
    assert result["current_target_critical_implies_old_anchor_critical"]
    assert result["off_anchor_support_cases_checked"] > 0
    assert result["anchor_atom_support_cases_checked"] > 0
    assert result["packet_inside_anchor_terminal_cases"] > 0
    assert result["off_anchor_atom_clean_release_admitted"]
    assert result["noncritical_anchor_atom_release_admitted"]
    assert result["all_nonsacrificed_owner_floors_unchanged"]
    assert result["designated_later_owner_auxiliary_floor_waived"]
    assert not result["historical_residual_preserving_return_used"]
    assert result["root_floor_preserved_by_old_or_reduced_anchor"]
    assert result["release_supplier_is_current_root"]
    assert not result["full_T_L_times_theorem_closed"]
