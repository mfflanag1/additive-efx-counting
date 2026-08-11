import json
from pathlib import Path

from .audit_universal_retained_bottom_support_reset import run


ROOT = Path(__file__).resolve().parents[2]


def test_retained_bottom_reset_replays():
    expected = json.loads(
        (ROOT / "results/universal_retained_bottom_support_reset_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_retained_bottom_reset_has_nested_progress():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["finite_set_audit"]["violations"] == []
    assert result["remaining_gate"] == "support-disjoint repeated-bottom Hall state"
