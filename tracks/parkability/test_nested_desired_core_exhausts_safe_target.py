from .audit_nested_desired_core_exhausts_safe_target import run


def test_nested_desired_core_exhausts_safe_target(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "CAP_FREE_NESTED_CORE_EXHAUSTION_PROVED"
    assert result["proper_residual_negation_status"] == "unsat"
    assert result["positive_singleton_desire_negation_status"] == "unsat"
