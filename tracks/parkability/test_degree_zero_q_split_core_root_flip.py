"""Focused regression for the degree-zero q split-core root flip."""

from pathlib import Path

from .audit_degree_zero_q_split_core_root_flip import run


ROOT = Path(__file__).resolve().parents[2]


def test_split_core_root_flip_dependencies_replay():
    result = run(ROOT)
    assert result["status"] == "DEPENDENCIES_REPLAYABLE"
    assert result["dependency_count"] == 6
    assert result["support_records"]["ordinary_degree_zero_does_not_delete_split_support_core"]


def test_claim_boundary_keeps_source_capture_open():
    result = run(ROOT)
    assert "source-margin capture" in result["claim_boundary"]
