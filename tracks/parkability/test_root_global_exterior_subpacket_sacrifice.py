from .audit_root_global_exterior_subpacket_sacrifice import run


def test_root_global_exterior_subpacket_sacrifice() -> None:
    result = run()
    assert result["status"] == (
        "CONDITIONAL_ROOT_EXTERIOR_DOMINANCE_FLOOR_ADMISSION_OPEN"
    )
    assert result["margin_identity_exact"]
    assert result["strict_test_exact"]
    assert result["strict_atomwise_cut_exact"]
    assert not result["supplier_star_floor_admission_proved"]
    assert result["summed_cut_exact"]
    assert result["support_cases_checked"] > 0
    assert result["proper_transfer_whole_packet_hits"] == 0
    assert result["full_transfer_proper_deletions_checked"] > 0
    assert result["equality_leave_one_spread_cases"] > 0
    assert not result["compatibility_premise_required"]
    assert result["equality_face_closed"]
    assert not result["multilabel_charge_branch_required"]
    assert not result["full_T_L_times_theorem_closed"]
