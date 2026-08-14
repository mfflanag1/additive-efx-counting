"""Regression test for the terminal omitted-core cross exchange."""

import json
from pathlib import Path

from .audit_terminal_path_omitted_core_cross_exchange_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_terminal_cross_exchange_frontier_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/terminal_path_omitted_core_cross_exchange_frontier_audit.json").read_text()
    )
    assert result == expected
    assert result["terminal_map_count"] == 4
    assert result["predecessor_duplicate_maps"] == 2
    assert result["first_source_duplicate_maps"] == 2
    assert result["cross_exchange_owner_payments"]
    assert result["overlap_capture_identity"]
    assert result["current_holder_edge_count"] == 4
    assert not result["frozen_supplier_edge_bound_proved"]
    assert not result["observer_safety_proved"]
    assert not result["capture_reversed"]
    assert not result["fixed_u_theorem_proved"]
