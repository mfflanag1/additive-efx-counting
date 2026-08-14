from pathlib import Path

from .audit_hidden_minimum_owner_replacement_or_capture import run


def test_hidden_minimum_owner_replacement_or_capture():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "OWNER_REPLACEMENT_CAPTURE_GEOMETRY_VERIFIED"
    assert result["owner_case_count"] == 96
    assert all(result["checks"].values())
