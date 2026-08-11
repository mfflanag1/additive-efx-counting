import json
from pathlib import Path

from .audit_blocked_hole_minimal_k_q_budget_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_blocked_hole_minimal_k_dichotomy_replays():
    expected = json.loads(
        (ROOT / "results/blocked_hole_minimal_k_q_budget_dichotomy_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_blocked_hole_minimal_k_dichotomy_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["alternatives"]) == 2
