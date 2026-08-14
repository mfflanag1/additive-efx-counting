"""Regression test for the exact mixed-core counterexample."""

import json
from pathlib import Path

from .audit_pure_cell_response_lift_local_refutation import run


ROOT = Path(__file__).resolve().parents[2]


def test_pure_cell_response_lift_counterexample_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/pure_cell_response_lift_local_refutation_audit.json").read_text()
    )
    assert result == expected
    assert result["union_strictly_desired"]
    assert result["neither_component_desired"]
    assert result["source_row_safe"]
    assert result["other_observer_rows_safe"]
    assert result["positive_additive"]
    assert not result["full_fixed_u_countermodel"]
