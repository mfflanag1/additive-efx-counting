"""Regression test for the two-level terminal selector."""

import json
from pathlib import Path

from .audit_terminal_path_two_level_charity_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_terminal_path_two_level_charity_selector_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/terminal_path_two_level_charity_selector_audit.json").read_text()
    )
    assert result == expected
    assert result["q_payment_equivalence"]
    assert result["x_payment_equivalence"]
    assert result["y_payment_equivalence"]
    assert result["full_d2_meets_q_threshold"]
    assert result["full_d1_meets_x_threshold"]
    assert result["current_holder_edge_bound"] == 4
    assert not result["three_placement_separator_eliminated"]
    assert not result["fixed_u_theorem_proved"]
