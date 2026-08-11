import json
from pathlib import Path

from .audit_paid_anchor_disjoint_recapture_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_anchor_disjoint_recapture_replays():
    expected = json.loads(
        (ROOT / "results/paid_anchor_disjoint_recapture_dichotomy_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_paid_anchor_disjoint_recapture_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 3
