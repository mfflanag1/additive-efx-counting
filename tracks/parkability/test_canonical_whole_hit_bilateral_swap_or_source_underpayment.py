from .audit_canonical_whole_hit_bilateral_swap_or_source_underpayment import run


def test_canonical_whole_hit_bilateral_swap_or_source_underpayment() -> None:
    result = run()
    assert result["status"] == (
        "CURRENT_WHOLE_HIT_REDUCED_TO_LEDGER_FREE_SWAP_OR_SOURCE_UNDERPAYMENT"
    )
    assert result["support_cases_checked"] > 0
    assert result["whole_hit_residual_is_nonempty_and_ledger_free"]
    assert result["bilateral_swap_new_holder_is_ledger_free"]
    assert result["holder_payment_exact"]
    assert result["source_underpayment_exact"]
    assert result["holder_cannot_source_current_subbundle"]
    assert not result["full_T_L_times_theorem_closed"]
