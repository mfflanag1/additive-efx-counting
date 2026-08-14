#!/usr/bin/env python3

from pathlib import Path

from .audit_three_cycle_six_branch_charity_completion import run


def test_three_cycle_six_branches():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "SIX_CAP_FREE_BRANCHING_COMPLETIONS_CONSTRUCTED"
    assert len(result["records"]) == 6
    assert result["checks"]["branches_without_shared_target_overlap"] == 2
    assert all(
        value if isinstance(value, bool) else value == 2
        for value in result["checks"].values()
    )
    assert all(all(record["checks"].values()) for record in result["records"])
