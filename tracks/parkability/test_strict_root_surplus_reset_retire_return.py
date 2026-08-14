from .audit_strict_root_surplus_reset_retire_return import run


def test_strict_root_surplus_reset_retire_return(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "CONDITIONAL_AUDIT_PASSED"
    assert result["strict_root_negation_status"] == "unsat"
    assert result["reset_floor_capture_negation_status"] == "unsat"
    assert result["maximum_endpoint_edge_count"] == 2
