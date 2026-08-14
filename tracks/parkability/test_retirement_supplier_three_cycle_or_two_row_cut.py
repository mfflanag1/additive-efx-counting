from .audit_retirement_supplier_three_cycle_or_two_row_cut import run


def test_retirement_supplier_three_cycle_or_two_row_cut() -> None:
    result = run()
    assert result["status"] == "SUPPLIER_CYCLE_OR_EXACT_TWO_ROW_CUT"
    assert result["support_conserved"]
    assert result["named_packet_absent_from_new_holder_target"]
    assert result["holder_payment_exact"]
    assert result["supplier_payment_exact"]
    assert result["two_row_cut_exhaustive"]
    assert result["other_retired_support_normalization_required"]
    assert not result["full_T_L_times_theorem_closed"]
