import json
from pathlib import Path

from .audit_paid_anchor_least_good_consumption import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_anchor_least_good_consumption_replays():
    expected = json.loads(
        (ROOT / "results/paid_anchor_least_good_consumption_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_paid_anchor_least_good_consumption_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["finite_support_audit"]["violations"] == []
