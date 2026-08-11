import json
from pathlib import Path

from .audit_q_donor_blockade_captured_margin_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_q_donor_blockade_handoff_replays():
    expected = json.loads(
        (ROOT / "results/q_donor_blockade_captured_margin_handoff_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_q_donor_blockade_is_captured_margin():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["handoff"]) == {"K_without_f", "K_with_f"}
