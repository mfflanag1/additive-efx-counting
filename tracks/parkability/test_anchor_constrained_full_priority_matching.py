import json
from pathlib import Path

from .audit_anchor_constrained_full_priority_matching import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchor_constrained_full_priority_matching_replays():
    expected = json.loads(
        (ROOT / "results/anchor_constrained_full_priority_matching_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_anchor_constrained_full_priority_matching_is_triangular():
    result = run(ROOT)
    assert result["status"] == "ALL_CLASSIFIED"
    assert result["counts"]["relations"] == 2 ** 15
    assert result["counts"]["violations"] == 0
