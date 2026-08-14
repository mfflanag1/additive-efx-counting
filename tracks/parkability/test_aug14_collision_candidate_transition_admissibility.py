from .audit_aug14_collision_candidate_transition_admissibility import run


def test_aug14_collision_candidate_transition_admissibility() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_GLOBAL_CUT_ADMITTED_AND_OLD_ROOT_CORE_CLOSES_COLLISION"
    )
    assert result["governing_rules_present"]
    assert all(result["conditional_boundaries_present"].values())
    assert not result["admission_theorem_proved"]
    assert result["equality_face_admission_theorem_proved"]
    assert result["base_contained_exterior_pooling_admitted"]
    assert result["root_global_exterior_subpacket_sacrifice_admitted"]
    assert result["base_containment_unconditional"]
    assert result["charity_one_good_reset_admitted"]
    assert result["full_T_L_times_theorem_closed"]
