"""Regression tests for the referee-corrected GG composition."""

import json
from pathlib import Path

from .audit_gg_cycle_class_referee_composition import run


ROOT = Path(__file__).resolve().parents[2]


def test_gg_referee_composition_replays():
    expected = json.loads(
        (ROOT / "results/gg_cycle_class_referee_composition_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_branch_graph_has_one_open_terminal():
    result = run(ROOT)
    assert result["status"] == "SMALLEST_TERMINAL_ISOLATED"
    assert result["terminal_nodes"] == ["EFX", "PI", "T*"]
    assert result["smallest_named_terminal"] == "rank-completing paid-response splice"
    assert result["local_recurrence_response_rank"] == 1
    assert result["residual_partition_family_size"] == 4096
    assert result["efx_floor_feasible_residual_partitions"] == 0


def test_composition_does_not_claim_gg_closure():
    result = run(ROOT)
    assert "not a GG closure theorem" in result["claim_boundary"]
