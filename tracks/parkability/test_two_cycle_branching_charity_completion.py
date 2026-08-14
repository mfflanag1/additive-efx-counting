#!/usr/bin/env python3

from pathlib import Path

from .audit_two_cycle_branching_charity_completion import run


def test_two_cycle_branching_completions():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "TWO_DISJOINT_BRANCHING_COMPLETIONS_CONSTRUCTED"
    assert len(result["records"]) == 2
    assert all(result["checks"].values())
    assert all(all(record["checks"].values()) for record in result["records"])
