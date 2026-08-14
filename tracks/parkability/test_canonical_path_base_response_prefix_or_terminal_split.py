"""Regression test for canonical path prefix payment and terminal splitting."""

import json
from pathlib import Path

from .audit_canonical_path_base_response_prefix_or_terminal_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_canonical_path_prefix_or_terminal_split_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/canonical_path_base_response_prefix_or_terminal_split_audit.json").read_text()
    )
    assert result == expected
    assert result["fixed_role_map_count"] == 12
    assert result["base_target_path_position_histogram"] == {"1": 4, "2": 4, "3": 4}
    assert result["internal_prefix_current_holder_edge_histogram"] == {"3": 4, "4": 4}
    assert result["terminal_compensator_exists"]
    assert result["terminal_payment_identities"]
    assert not result["frozen_supplier_edge_bound_proved"]
    assert not result["observer_safety_proved"]
    assert not result["terminal_separator_eliminated"]
    assert not result["fixed_u_theorem_proved"]
