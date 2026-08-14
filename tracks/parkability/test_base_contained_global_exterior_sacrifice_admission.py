from .audit_base_contained_global_exterior_sacrifice_admission import run


def test_base_contained_global_exterior_sacrifice_admission() -> None:
    result = run()
    assert result["status"] == (
        "STRICT_GLOBAL_EXTERIOR_SACRIFICE_FLOOR_ADMISSION_OPEN"
    )
    assert result["strict_margin_exact"]
    assert result["singleton_target_never_strongly_envied"]
    assert result["support_cases_checked"] > 0
    assert result["root_target_whole_packet_hits"] == 0
    assert result["singleton_packet_zero_hit_cases"] > 0
    assert result["other_retired_labels_recorded"]
    assert not result["declared_floor_preservation_proved"]
    assert not result["supplier_star_transition_admitted"]
    assert not result["exterior_dominance_closed"]
    assert not result["global_multilabel_well_foundedness_proved"]
    assert not result["full_T_L_times_theorem_closed"]
