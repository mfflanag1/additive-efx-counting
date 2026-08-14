from .audit_aug14_collision_candidate_transition_admissibility import run


def test_aug14_collision_candidate_transition_admissibility() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_FLOOR_GATE_REPAIRED_T_L_TIMES_CLOSED"
    )
    assert result["governing_rules_present"]
    assert all(result["conditional_boundaries_present"].values())
    assert result["admission_theorem_proved"]
    assert result["equality_face_admission_theorem_proved"]
    assert result["base_contained_exterior_pooling_admitted"]
    assert not result["root_global_exterior_subpacket_sacrifice_admitted"]
    assert result["root_singleton_reset_supplier_star_admitted"]
    assert result["root_global_exterior_subpacket_sacrifice_scalar_cut_conditional"]
    assert not result["declared_floor_gate_open"]
    assert not result["base_containment_unconditional_from_old_global_cut"]
    assert result["charity_one_good_reset_admitted"]
    assert result["full_T_L_times_theorem_closed"]
