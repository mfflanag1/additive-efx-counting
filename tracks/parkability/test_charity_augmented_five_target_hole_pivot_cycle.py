import json
from pathlib import Path

from .audit_charity_augmented_five_target_hole_pivot_cycle import run


ROOT = Path(__file__).resolve().parents[2]


def test_charity_augmented_hole_pivot_cycle_replays():
    expected = json.loads(
        (ROOT / "results/charity_augmented_five_target_hole_pivot_cycle_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_charity_augmented_hole_pivot_cycle_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["rank_four_matching_count"] == 120
    assert result["rank_preserved_every_pivot"]
    assert result["unique_hole_preserved_every_pivot"]
    assert result["cycle_sources_and_targets_distinct_before_first_repeat"]
    assert result["outside_matching_invariant"]
