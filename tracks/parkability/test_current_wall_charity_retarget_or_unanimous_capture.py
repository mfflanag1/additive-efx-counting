import json
from pathlib import Path

from .audit_current_wall_charity_retarget_or_unanimous_capture import run


def test_current_wall_charity_retarget_or_unanimous_capture(tmp_path: Path):
    output = tmp_path / "audit.json"
    result = run(output)
    assert all(value is True or value == "unsat" for value in result["checks"].values())
    assert json.loads(output.read_text()) == result
    assert "observer safety" in result["claim_boundary"]
