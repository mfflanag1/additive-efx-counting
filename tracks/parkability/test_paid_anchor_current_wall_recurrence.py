import json
from pathlib import Path

from .audit_paid_anchor_current_wall_recurrence import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_anchor_current_wall_recurrence_replays():
    expected = json.loads(
        (ROOT / "results/paid_anchor_current_wall_recurrence_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_paid_anchor_current_wall_recurrence_is_finite():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["finite_vector_audit"]["violations"] == []
