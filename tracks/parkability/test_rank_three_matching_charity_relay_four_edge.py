from .audit_rank_three_matching_charity_relay_four_edge import run


def test_rank_three_matching_charity_relay_four_edge(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "CONDITIONAL_COMPOSITION_AUDIT_PASSED"
    assert result["nonself_rank_three_matchings_checked"] == 11
    assert result["maximum_support_provenance_edges"] == 4
    assert result["strict_root_negation_status"] == "unsat"
    assert result["reset_floor_capture_negation_status"] == "unsat"
