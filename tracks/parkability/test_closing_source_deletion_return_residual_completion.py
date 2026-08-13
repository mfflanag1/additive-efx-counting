"""Regression tests for universal closing-source residual completion."""

import json
from pathlib import Path

from .audit_closing_source_deletion_return_residual_completion import run


ROOT = Path(__file__).resolve().parents[2]


def test_closing_source_completion_audit_replays():
    expected = json.loads(
        (ROOT / "results/closing_source_deletion_return_residual_completion_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_all_nonself_hamiltonian_pivots_are_covered():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["hamiltonian_path_count"] == 24
    assert result["nonself_pivot_count"] == 72
    assert result["cycle_length_counts"] == {"2": 24, "3": 24, "4": 24}
    assert all(result["checks"].values())
    assert result["scalar_payment_reduction_verified"]
    assert not result["mixed_margin_termination_verified"]
    assert result["surviving_terminal"] == "rank-completing paid-response splice"


def test_closing_source_completion_claim_boundary():
    result = run(ROOT)
    assert "repeated-response termination" in result["claim_boundary"]
    assert "remain open" in result["claim_boundary"]
