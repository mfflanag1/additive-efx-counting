import json
from pathlib import Path

from .audit_half_floor_current_wall_lift import run


def test_half_floor_current_wall_lift(tmp_path: Path):
    output = tmp_path / "audit.json"
    result = run(output)
    assert all(value == "unsat" for value in result["checks"].values())
    assert json.loads(output.read_text()) == result
    assert "enlarged W+(A-g) target" in result["claim_boundary"]
