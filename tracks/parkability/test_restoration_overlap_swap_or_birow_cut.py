from .audit_restoration_overlap_swap_or_birow_cut import run


def test_restoration_overlap_swap_or_birow_cut() -> None:
    result = run(__import__("pathlib").Path(__file__).resolve().parents[2])
    assert result["status"] == "PURE_OVERLAP_REDUCED_TO_STRICT_ROOT_OR_BIROW_CUT"
    assert result["root_margin_identity"]
    assert result["recipient_margin_identity"]
    assert result["recipient_floor_under_swap"]
    assert result["root_floor_under_swap"]
    assert result["proper_root_crossing_too_expensive_in_surviving_cut"]
    assert not result["full_T_L_times_theorem_closed"]
