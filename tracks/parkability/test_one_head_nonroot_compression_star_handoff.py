#!/usr/bin/env python3
"""Focused regression tests for the one-head compression-star handoff."""

from pathlib import Path

from .audit_one_head_nonroot_compression_star_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_one_head_nonroot_compression_star_handoff_replays():
    result = run(ROOT)
    assert result["status"] == "ONE_HEAD_REDUCED_TO_ROOT_FACING_OR_COMPRESSION_STAR"
    assert result["graph_census"]["row_count"] == 28
    assert result["graph_census"]["nonroot_handoff_count"] == 25
    assert result["graph_census"]["root_facing_count"] == 3
    assert result["symbolic_checks"]["head_target_interfaces"] == 9
    assert result["symbolic_checks"]["root_strictly_improved"]


def test_only_surviving_one_head_rows_are_root_facing():
    result = run(ROOT)
    rows = result["graph_census"]["root_facing_rows"]
    assert {record["head"] for record in rows} == {"q", "a", "b"}
    assert all(record["accepted_targets"] == ["r"] for record in rows)
