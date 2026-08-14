from .audit_global_exterior_dominance_base_containment_charity_reset import run


def test_global_exterior_dominance_base_containment_charity_reset() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_REDUCED_UNCONDITIONALLY_TO_CHARITY_ONE_GOOD_ON_OFF_RESPONSE"
    )
    assert result["exterior_identity_exact"]
    assert result["crossing_atom_impossible"]
    assert result["on_good_loss_band_exact"]
    assert result["reset_support_cases_checked"] > 0
    assert result["set_theoretic_crossing_atoms_seen"] > 0
    assert result["proper_packet_response_cases"] > 0
    assert result["whole_packet_on_good_cases"] > 0
    assert result["whole_packet_off_good_cases"] > 0
    assert result["whole_packet_base_root_cases"] > 0
    assert not result["signed_missing_base_return_required"]
    assert not result["multilabel_charge_branch_required"]
    assert not result["full_T_L_times_theorem_closed"]
