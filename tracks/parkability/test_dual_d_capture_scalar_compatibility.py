import json
from pathlib import Path

from .audit_dual_d_capture_scalar_compatibility import run


def test_dual_d_capture_scalar_compatibility(tmp_path: Path):
    output = tmp_path / "audit.json"
    result = run(output)
    assert result["status"] == "SAT_EXACT_SCALAR_MODEL"
    assert all(result["checks"].values())
    assert json.loads(output.read_text()) == result
    assert "not a four-owner valuation profile" in result["claim_boundary"]
