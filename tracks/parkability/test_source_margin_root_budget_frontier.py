import json
from pathlib import Path

from .audit_source_margin_root_budget_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_source_margin_root_budget_frontier_replays():
    expected = json.loads(
        (ROOT / "results/source_margin_root_budget_frontier_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_source_margin_root_budget_frontier_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["frontier_certificates"]) == 4
    assert result["remaining_operation"] == "third-owner surplus-budgeted connected fork"
