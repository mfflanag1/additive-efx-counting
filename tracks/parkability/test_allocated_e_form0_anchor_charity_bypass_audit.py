from .audit_allocated_e_form0_anchor_charity_bypass import run


def test_allocated_e_form0_anchor_charity_bypass_audit(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "UNSAT_ANCHOR_CHARITY_PARKED_BYPASS"
    assert result["full_status"] == "unsat"
    assert result["deletion_minimal_core_size"] > 0
