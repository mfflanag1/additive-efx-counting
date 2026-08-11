import json
from pathlib import Path

from .audit_surplus_budgeted_charity_exchange_component import run


ROOT = Path(__file__).resolve().parents[2]


def test_surplus_budgeted_charity_exchange_replays():
    expected = json.loads(
        (ROOT / "results/surplus_budgeted_charity_exchange_component_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_surplus_budgeted_charity_exchange_has_exact_witness():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
    assert result["exact_witness"]["all_agents_strict"]
    assert result["exact_witness"]["single_connected_transfer_component"]
    assert result["exact_witness"]["has_directed_cycle"]
