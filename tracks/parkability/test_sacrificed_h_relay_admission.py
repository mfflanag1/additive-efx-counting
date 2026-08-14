import z3

from .audit_sacrificed_h_relay_admission import run


def test_sacrificed_h_relay_audit(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "AUDIT_PASSED"
    assert result["capture_negation_status"] == "unsat"
    assert z3.get_version_string()
