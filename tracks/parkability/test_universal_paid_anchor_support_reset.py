import json
from pathlib import Path

from .audit_universal_paid_anchor_support_reset import run


ROOT = Path(__file__).resolve().parents[2]


def test_universal_paid_anchor_reset_replays():
    expected = json.loads(
        (ROOT / "results/universal_paid_anchor_support_reset_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_universal_paid_anchor_reset_is_monotone():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["finite_set_audit"]["violations"] == []
