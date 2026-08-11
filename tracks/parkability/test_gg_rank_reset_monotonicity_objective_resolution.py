import json
from pathlib import Path

from .audit_gg_rank_reset_monotonicity_objective_resolution import run


ROOT = Path(__file__).resolve().parents[2]


def test_rank_reset_objective_resolution_replays():
    expected = json.loads(
        (ROOT / "results/gg_rank_reset_monotonicity_objective_resolution_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_requested_potential_is_exactly_refuted():
    result = run(ROOT)
    assert result["status"] == "OBJECTIVE_EXACTLY_REFUTED_AS_STATED"
    assert result["exact_positive_additive_countermodel"]
    assert result["requested_structural_coordinates_tied"]
    assert result["raw_residual_direction_reversed_by_row_scaling"]
    assert result["corrected_historical_ledger_also_refuted"]
    assert not result["full_gg_countermodel"]
    assert result["globality_boundary_verified"]
