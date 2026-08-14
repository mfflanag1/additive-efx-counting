from .audit_root_global_supplier_star_floor_admissibility_gap import run


def test_root_global_supplier_star_floor_admissibility_gap() -> None:
    result = run()
    assert result["status"] == (
        "HISTORICAL_UNRESET_STAR_INVALID_FLOOR_RESET_REPAIR_PROVED"
    )
    assert result["positive_floor_empty_assignment_preservation_unsat"]
    assert result["candidate_empties_later_owners"]
    assert result["frozen_contract_requires_declared_floors"]
    assert not result["all_sacrificed_floors_zero_proved"]
    assert result["controlled_floor_reset_admitted"]
    assert not result["unreset_supplier_star_transition_admitted"]
    assert result["reset_supplier_star_transition_admitted"]
    assert result["conditional_exterior_dominance_scalar_chain_valid"]
    assert result["full_T_L_times_theorem_closed"]
