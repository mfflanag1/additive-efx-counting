"""Focused regression for the fixed-U q-residual selector composition."""

from pathlib import Path

try:
    from .audit_fixed_u_q_residual_global_max_selector import run
except ImportError:
    from audit_fixed_u_q_residual_global_max_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_dependencies_and_same_row_strictness():
    result = run(ROOT)
    assert result["status"] == "COMPOSED"
    assert len(result["dependency_records"]) == 3
    assert result["same_row_strict_maximum_sanity"]["both_strictly_larger"]


def test_claim_boundary_keeps_root_facing_gate_open():
    result = run(ROOT)
    assert "root-facing" in result["claim_boundary"]
    assert "GG closure" in result["claim_boundary"]
