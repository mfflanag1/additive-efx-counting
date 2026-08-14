"""Regression test for the corrected reservoir-fan dichotomy."""

import json
from pathlib import Path

from .audit_normalization_bypass_three_reservoir_fan_correction import run


ROOT = Path(__file__).resolve().parents[2]


def test_corrected_reservoir_fan_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/normalization_bypass_three_reservoir_fan_correction_audit.json").read_text()
    )
    assert result == expected
    assert result["nonself_source_maps"] == 81
    assert result["surjective_maps_force_closed_family"]
    assert result["counterexample"]["has_current_supplier_two_cycle"]
    assert not result["counterexample"]["has_closed_disjoint_core_family"]
    assert not result["current_supplier_cycle_sufficient_for_generalized_pi"]
    assert not result["missing_source_capture_reversed"]
