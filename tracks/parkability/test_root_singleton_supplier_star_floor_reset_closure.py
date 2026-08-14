from .audit_root_singleton_supplier_star_floor_reset_closure import run


def test_root_singleton_supplier_star_floor_reset_closure() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_HELD_T_L_TIMES_COLLISION_CLOSED_BY_FLOOR_RESET_STAR"
    )
    assert result["base_atom_star_is_strict"]
    assert result["exterior_atom_star_is_strict"]
    assert result["support_cases_checked"] > 0
    assert result["base_atom_cases"] > 0
    assert result["exterior_atom_cases"] > 0
    assert result["response_subsets_checked"] > 0
    assert result["whole_packet_response_failures"] == 0
    assert not result["old_later_floors_preserved"]
    assert result["controlled_floor_reset_used"]
    assert not result["historical_reversibility_used"]
    assert result["global_supplier_star_supplier_closed"]
    assert result["root_holder_branch_closed"]
    assert result["nonroot_holder_branch_closed_by_dependency"]
    assert result["full_T_L_times_theorem_closed"]
    assert not result["full_GG_closed"]
    assert not result["general_EFX_closed"]
