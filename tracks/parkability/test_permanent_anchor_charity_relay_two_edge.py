from .audit_permanent_anchor_charity_relay_two_edge import run


def test_permanent_anchor_charity_relay_two_edge(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "CONDITIONAL_COMPOSITION_AUDIT_PASSED"
    assert len(result["cases"]) == 2
    assert result["maximum_support_provenance_edges"] == 2
    assert result["strict_root_negation_status"] == "unsat"
    assert result["reset_floor_capture_negation_status"] == "unsat"
