import json
from pathlib import Path

from .audit_current_wall_backward_hole_capture import run


def test_current_wall_backward_hole_capture(tmp_path: Path):
    output = tmp_path / "audit.json"
    result = run(output)
    assert all(value == "unsat" for value in result["checks"].values())
    assert json.loads(output.read_text()) == result
    assert "capture uncrossing" in result["claim_boundary"]
