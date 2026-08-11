import json
from pathlib import Path

from .audit_anchored_mixed_margin_path_terminal_classification import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchored_mixed_margin_path_terminal_classification_replays():
    expected = json.loads(
        (ROOT / "results/anchored_mixed_margin_path_terminal_classification_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_anchored_mixed_margin_path_terminal_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["anchored_path_count"] == 6
    assert result["nonself_hole_pivot_count"] == 18
    assert result["outcome_counts"] == {
        "anchor_release": 4,
        "external_cycle": 2,
        "anchor_cycle": 12,
    }
    assert result["q_hole_excluded"]
