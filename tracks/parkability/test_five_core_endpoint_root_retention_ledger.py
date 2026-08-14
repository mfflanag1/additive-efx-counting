from .audit_five_core_endpoint_root_retention_ledger import run


def test_five_core_endpoint_root_retention_ledger():
    assert run()["status"] == "AUDIT_PASSED"
