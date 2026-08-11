import json
from pathlib import Path

from .audit_charity_blocker_exchange_walk import run


ROOT = Path(__file__).resolve().parents[2]


def test_charity_blocker_exchange_walk_replays():
    expected = json.loads(
        (ROOT / "results/charity_blocker_exchange_walk_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_charity_blocker_exchange_walk_is_monotone():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 3
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
    assert all(value == "unsat" for value in result["terminal_checks"].values())
