from .audit_root_retired_packet_old_anchor_critical_localization import run


def test_root_retired_packet_old_anchor_critical_localization() -> None:
    result = run()
    assert result["status"] == "ROOT_PACKET_LOCALIZED_TO_OLD_ANCHOR_CRITICAL_ATOMS"
    assert result["recorded_source_floor_strictly_improves"]
    assert result["critical_atom_exceeds_anchor_surplus"]
    assert result["off_anchor_support_cases_checked"] > 0
    assert result["anchor_atom_support_cases_checked"] > 0
    assert result["packet_inside_anchor_terminal_cases"] > 0
    assert result["off_anchor_atom_return_admitted"]
    assert result["noncritical_anchor_atom_release_admitted"]
    assert result["all_other_owner_floors_unchanged"]
    assert result["retirement_source_floor_preserved"]
    assert result["root_floor_preserved_by_old_or_reduced_anchor"]
    assert result["release_supplier_is_current_root"]
    assert not result["full_T_L_times_theorem_closed"]
