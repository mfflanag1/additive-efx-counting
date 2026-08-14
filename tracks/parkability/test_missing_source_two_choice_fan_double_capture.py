"""Regression test for the missing-source double-capture lemma."""

import json
from pathlib import Path

from .audit_missing_source_two_choice_fan_double_capture import run


ROOT = Path(__file__).resolve().parents[2]


def test_missing_source_double_capture_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/missing_source_two_choice_fan_double_capture_audit.json").read_text()
    )
    assert result == expected
    assert result["image_size_three_maps"] == 48
    assert result["topology_split"] == {
        "both_duplicate_cores_foreign_to_missing": 24,
        "missing_is_duplicate_core_supplier": 24,
    }
    assert result["double_capture_implication"]
    assert not result["capture_reversal_proved"]
