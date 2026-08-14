from .audit_aug14_collision_candidate_transition_admissibility import run


def test_aug14_collision_candidate_transition_admissibility() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_GLOBAL_CUT_CONDITIONAL_FLOOR_ADMISSION_OPEN"
    )
    assert result["governing_rules_present"]
    assert all(result["conditional_boundaries_present"].values())
    assert not result["admission_theorem_proved"]
    assert result["equality_face_admission_theorem_proved"]
    assert result["base_contained_exterior_pooling_admitted"]
    assert not result["root_global_exterior_subpacket_sacrifice_admitted"]
    assert result["root_global_exterior_subpacket_sacrifice_scalar_cut_conditional"]
    assert result["declared_floor_gate_open"]
    assert result["base_containment_unconditional"]
    assert result["charity_one_good_reset_admitted"]
    assert not result["full_T_L_times_theorem_closed"]
