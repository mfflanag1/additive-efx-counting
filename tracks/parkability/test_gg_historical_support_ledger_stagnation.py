"""Focused regression for the historical-ledger plateau."""

from pathlib import Path

try:
    from .audit_gg_historical_support_ledger_stagnation import run
except ImportError:
    from audit_gg_historical_support_ledger_stagnation import run


ROOT = Path(__file__).resolve().parents[2]


def test_four_state_historical_ledger_plateau():
    result = run(ROOT)
    assert result["status"] == "EXACT_PLATEAU"
    assert result["maximum_response_rank"] == 3
    assert not result["full_response_sdr"]
    assert len(result["states"]) == 4
    assert result["all_states_non_efx"]
    assert result["ledger_identical_across_all_states"]


def test_claim_boundary_does_not_claim_a_dynamic_cycle():
    result = run(ROOT)
    assert "does not prove" in result["claim_boundary"]
    assert "deterministic repair rule cycles" in result["claim_boundary"]
