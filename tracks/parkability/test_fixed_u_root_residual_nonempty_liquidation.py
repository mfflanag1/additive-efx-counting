"""Regression tests for the universal root-residual liquidation reduction."""

import json
from pathlib import Path

from .audit_fixed_u_root_residual_nonempty_liquidation import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_residual_liquidation_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/fixed_u_root_residual_nonempty_liquidation_audit.json").read_text()
    )
    assert result == expected
    assert result["status"] == "UNIVERSAL_THREE_EDGE_PRIORITY_VALID_PROBE"
    assert result["mandatory_root_response_recorded"]
    assert result["response_core_nonempty_by_declared_record_semantics"]
    assert result["response_target_is_original_root_cell"]
    assert result["strict_anchor_implies_residual_below_margin"]
    assert result["maximum_edge_count"] <= 3
    assert not result["complete_efx_endpoint_proved"]
    assert not result["post_probe_response_recurrence_closed"]
