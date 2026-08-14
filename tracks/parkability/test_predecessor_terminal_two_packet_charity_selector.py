"""Regression test for the coupled predecessor terminal selector."""

import json
from pathlib import Path

from .audit_predecessor_terminal_two_packet_charity_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_predecessor_terminal_two_packet_charity_selector_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/predecessor_terminal_two_packet_charity_selector_audit.json").read_text()
    )
    assert result == expected
    assert result["missing_payment_equivalence"]
    assert result["terminal_payment_equivalence"]
    assert result["predecessor_payment_equivalence"]
    assert result["full_overlap_meets_missing_threshold"]
    assert result["full_path_core_meets_terminal_threshold"]
    assert result["current_holder_edge_bound"] == 4
    assert not result["three_corner_separator_eliminated"]
    assert not result["fixed_u_theorem_proved"]
