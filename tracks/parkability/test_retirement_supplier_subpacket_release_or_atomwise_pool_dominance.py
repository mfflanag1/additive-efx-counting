from .audit_retirement_supplier_subpacket_release_or_atomwise_pool_dominance import run


def test_retirement_supplier_subpacket_release_or_atomwise_pool_dominance() -> None:
    result = run()
    assert result["status"] == (
        "STRICT_SUBPACKET_RELEASE_ADMITTED_WEAK_ATOMWISE_EQUALITY_OPEN"
    )
    assert result["subpacket_margin_identity_exact"]
    assert result["proper_split_cases_checked"] > 0
    assert result["proper_split_whole_target_hits"] == 0
    assert result["proper_equality_returns_checked"] > 0
    assert not result["historical_subpacket_return_transition_admitted"]
    assert result["clean_controlled_subpacket_release_admitted"]
    assert not result["multigood_atoms_strictly_above_surplus"]
    assert result["weak_atomwise_pool_charge_unconditional"]
    assert result["atomwise_pool_charge_exact"]
    assert result["summed_charge_exact"]
    assert not result["full_T_L_times_theorem_closed"]
