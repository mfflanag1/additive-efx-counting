"""Regression test for the full-owner connected rank defect."""

import json
from pathlib import Path

from .audit_image_three_full_owner_connected_rank_defect import run


ROOT = Path(__file__).resolve().parents[2]


def test_image_three_maps_are_connected_but_rank_deficient():
    result = run()
    expected = json.loads(
        (ROOT / "results/image_three_full_owner_connected_rank_defect_audit.json").read_text()
    )
    assert result == expected
    assert result["map_count"] == 48
    assert result["component_size_histogram"] == {"4": 48}
    assert result["missing_source_histogram"] == {"0": 12, "1": 12, "2": 12, "3": 12}
    assert result["duplicated_source_histogram"] == {"0": 12, "1": 12, "2": 12, "3": 12}
    assert result["all_maps_connected"]
    assert result["response_rank"] == 3
    assert result["owner_component_size"] == 4
    assert not result["rank_full_for_component"]
    assert not result["rank_four_augmentation_proved"]
    assert not result["fixed_u_theorem_proved"]
