from .audit_aug14_collision_candidate_transition_admissibility import run


def test_aug14_collision_candidate_transition_admissibility() -> None:
    result = run()
    assert result["status"] == (
        "GENERIC_CANDIDATES_CONDITIONAL_EQUALITY_FACE_ADMITTED"
    )
    assert result["governing_rules_present"]
    assert all(result["conditional_boundaries_present"].values())
    assert not result["admission_theorem_proved"]
    assert result["equality_face_admission_theorem_proved"]
    assert not result["full_T_L_times_theorem_closed"]
