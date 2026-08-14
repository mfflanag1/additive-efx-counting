"""Regression test for the two-stage form-2 checkpoint analysis."""

import json
from pathlib import Path

from .analyze_exact_response_linear_cegar_checkpoint import analyze


ROOT = Path(__file__).resolve().parents[2]
SOURCES = (
    ROOT / "results/exact_response_form2_linear_allocation_cegar_fresh_v2_20260814.json",
    ROOT / "results/exact_response_form2_linear_allocation_cegar_stage2_v2_20260814.json",
)


def test_exact_response_linear_checkpoint_replays():
    result = analyze(SOURCES)
    expected = json.loads(
        (ROOT / "results/exact_response_form2_linear_cegar_checkpoint_analysis.json").read_text()
    )
    assert result == expected
    assert result["round_count"] == 33
    assert result["chosen_allocation_count"] == 264
    assert result["minimum_edge_histogram"] == {"2": 7, "3": 19, "4": 7}
    assert all(result["fixed_whole_target_patterns"].values())
