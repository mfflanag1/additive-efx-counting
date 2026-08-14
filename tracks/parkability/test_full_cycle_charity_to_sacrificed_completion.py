#!/usr/bin/env python3

from pathlib import Path

from .audit_full_cycle_charity_to_sacrificed_completion import run


def test_full_cycle_d_endpoints():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "BOTH_FULL_CYCLE_D_ENDPOINTS_CONSTRUCTED"
    assert len(result["records"]) == 2
    assert all(result["checks"].values())
    assert all(all(record["checks"].values()) for record in result["records"])
