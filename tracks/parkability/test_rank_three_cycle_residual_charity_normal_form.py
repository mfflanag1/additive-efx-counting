#!/usr/bin/env python3

from pathlib import Path

from .audit_rank_three_cycle_residual_charity_normal_form import run


def test_cycle_residual_charity_normal_form():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "ALL_TWO_AND_THREE_CYCLE_RESIDUAL_SELECTORS_VALID"
    assert result["selector_count"] == 32
    assert all(result["checks"].values())
    assert {len(record["transfer_edges"]) for record in result["records"]} == {3, 4}
