"""Regression test for terminal charity placement."""

import json
from pathlib import Path

from .audit_terminal_path_charity_placement_bicriteria import run


ROOT = Path(__file__).resolve().parents[2]


def test_terminal_path_charity_placement_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/terminal_path_charity_placement_bicriteria_audit.json").read_text()
    )
    assert result == expected
    assert result["terminal_payment_equivalence"]
    assert result["donor_payment_equivalence"]
    assert result["full_path_core_meets_both_thresholds"]
    assert result["current_holder_edge_bound"] == 3
    assert not result["critical_system_eliminated"]
    assert not result["fixed_u_theorem_proved"]
