"""Regression test for the closed-block response-merger frontier."""

import json
from pathlib import Path

from .audit_closed_base_block_cross_response_merger import run


ROOT = Path(__file__).resolve().parents[2]


def test_closed_base_block_cross_response_merger_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/closed_base_block_cross_response_merger_audit.json").read_text()
    )
    assert result == expected
    assert result["set_partition_count_on_five_vertices"] == 52
    assert result["strict_merger_checks"] > 0
    assert result["merger_bound_holds"]
    assert result["current_safe_response_extraction_inherited"]
    assert not result["current_safe_response_extraction_reencoded"]
    assert result["outsider_safety_at_saturation"]
    assert not result["response_rank_proved"]
    assert not result["fixed_u_theorem_proved"]
