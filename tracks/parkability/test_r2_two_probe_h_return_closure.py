from pathlib import Path

from .audit_r2_two_probe_h_return_closure import run


def test_r2_two_probe_h_return_closure():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "CONDITIONAL_R2_H_RETURN_COMPOSITION_AUDIT_PASSED"
    assert all(result["checks"].values())
