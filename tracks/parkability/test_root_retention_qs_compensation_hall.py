from .audit_root_retention_qs_compensation_hall import run


def test_root_retention_qs_compensation_hall():
    assert run()["status"] == "AUDIT_PASSED"
