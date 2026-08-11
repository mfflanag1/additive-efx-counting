import json
from pathlib import Path

from .audit_paid_splice_observer_failure_current_response import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_splice_observer_failure_replays():
    expected = json.loads(
        (ROOT / "results/paid_splice_observer_failure_current_response_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_paid_splice_observer_failure_has_only_named_outcomes():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 3
    assert result["current_safe_but_not_base_safe_witness"]["status"] == "sat"
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
    assert all(value == "unsat" for value in result["exact_response_checks"].values())
