#!/usr/bin/env python3

from pathlib import Path

from .audit_two_survivor_charity_path_selector import run


def test_two_survivor_path_selectors():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FOUR_CAP_FREE_PATH_SELECTORS_CONSTRUCTED"
    assert len(result["records"]) == 4
    assert all(result["checks"].values())
    assert all(
        len(record["transfer_edges"]) == 4 for record in result["records"]
    )
