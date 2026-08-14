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
    assert result["status"] == "T_L_TIMES_ROOT_FLOOR_ADMISSION_GATE_OPEN"
    assert result["terminal_nodes"] == ["EFX", "PI", "T*"]
    assert result["smallest_named_terminal"] == "generic rank-completing paid-response splice outside the enlarged-root contract"
    assert result["historical_global_typed_terminal"] == (
        "T^dagger = T_0^* dot-union T_L^*"
    )
    assert result["global_typed_terminal"] == "T^dagger = T_0^* dot-union T_L^*"
    assert result["pre_ledger_terminal"] == "T_0^*"
    assert result["post_ledger_terminal"] == "T_L^*"
    assert result["post_ledger_terminal_subtypes"] == [
        "T_{L,perp}^*", "T_{L,times}^*"
    ]
    assert result["closed_post_ledger_subtypes"] == []
    assert not result["collision_T_L_times_closed"]
    assert result["collision_T_L_times_conditional_scalar_contradiction"]
    assert len(result["post_ledger_terminal_requirements"]) == 6
    assert result["stated_four_old_core_normal_form_vacuous"]
    assert result["frozen_witnesses_escape_by_efx_rotation"]
    assert result["local_recurrence_response_rank"] == 1
    assert result["residual_partition_family_size"] == 4096
    assert result["efx_floor_feasible_residual_partitions"] == 0


def test_composition_does_not_claim_gg_closure():
    result = run(ROOT)
    assert "not a GG closure theorem" in result["claim_boundary"]
