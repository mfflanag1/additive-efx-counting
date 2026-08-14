from .audit_retirement_supplier_return_admissibility_correction import run


def test_retirement_supplier_return_admissibility_correction() -> None:
    result = run()
    assert result["status"] == (
        "HISTORICAL_REVERSAL_INVALID_STRICT_AND_EQUALITY_RELEASES_REPAIRED"
    )
    assert result["signed_provenance_identifies_historical_recipient"]
    assert not result["signed_provenance_implies_current_return_right"]
    assert result["root_safe_core_handoff_remains_admitted"]
    assert result["strict_clean_controlled_release_admitted"]
    assert result["packet_price_arithmetic_strict_branch_unconditional"]
    assert result["strict_atomwise_pool_dominance_unconditional"]
    assert result["root_equality_closed_by_packet_spread"]
    assert not result["full_T_L_times_theorem_closed"]
