#!/usr/bin/env python3
"""Regression tests for the external-observer wall extractions."""

from __future__ import annotations

from pathlib import Path

try:
    from .extract_alternating_external_observer_atomic_walls import extract as extract_atomic
    from .extract_alternating_variable_core_walls import extract as extract_variable
except ImportError:
    from extract_alternating_external_observer_atomic_walls import extract as extract_atomic
    from extract_alternating_variable_core_walls import extract as extract_variable


def test_atomic() -> None:
    result = extract_atomic()
    assert result["status"] == "ALL_ATOMIC_BLOCKER_SELECTIONS_UNSAT"
    assert result["blocker_selection_count"] == 12
    assert len(result["minimal_failure_cores"]) == 6
    assert len(result["exceptional_pair_structural_core"]) == 22


def test_bottom_split() -> None:
    root = Path(__file__).resolve().parents[2]
    result = extract_variable(
        root / "results/alternating_external_observer_0213_bq2_broad_core_audit.json"
    )
    assert result["status"] == "ALL_CORE_BLOCKER_SELECTIONS_UNSAT"
    assert result["packet_sizes"] == [1, 1, 1, 2]
    assert result["blocker_selection_count"] == 36
    assert len(result["rivals"]) == 4
    assert all(
        wall.startswith("q!>")
        for rival in result["rivals"]
        for wall in rival["possible_failure_walls"]
    )


if __name__ == "__main__":
    test_atomic()
    test_bottom_split()
    print("alternating external-observer wall tests passed")
