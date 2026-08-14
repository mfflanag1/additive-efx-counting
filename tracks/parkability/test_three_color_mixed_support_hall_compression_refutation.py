"""Regression test for the three-color support obstruction."""

import json
from pathlib import Path

from .audit_three_color_mixed_support_hall_compression_refutation import run


ROOT = Path(__file__).resolve().parents[2]


def test_three_color_mixed_support_counterexample_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/three_color_mixed_support_hall_compression_refutation_audit.json").read_text()
    )
    assert result == expected
    assert result["all_cores_strictly_desired"]
    assert result["all_cores_inclusion_minimal"]
    assert result["all_cores_source_safe"]
    assert result["other_observer_common_safety_realizable"]
    assert result["no_closed_represented_source_subfamily"]
    assert result["physical_pair_count"] == 6
    assert result["physical_pairs_match_expected"]
    assert not result["at_most_three_pair_reversal_exists"]
    assert not result["full_fixed_u_countermodel"]
