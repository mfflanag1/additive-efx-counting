"""Focused regression for protected-q response retention."""

from pathlib import Path

from .audit_protected_q_response_retention import run


ROOT = Path(__file__).resolve().parents[2]


def test_protected_q_retention_audit():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["protected_q_core_avoids_f"]
    assert set(result["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_degree_zero_branch_open():
    result = run(ROOT)
    assert "degree-zero q recurrence" in result["claim_boundary"]
