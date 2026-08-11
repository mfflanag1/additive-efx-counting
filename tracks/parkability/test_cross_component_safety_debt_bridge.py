import json
from pathlib import Path

from .audit_cross_component_safety_debt_bridge import run


ROOT = Path(__file__).resolve().parents[2]


def test_cross_component_safety_debt_bridge_replays():
    expected = json.loads(
        (ROOT / "results/cross_component_safety_debt_bridge_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_cross_component_safety_debt_bridge_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 2
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
    assert all(value == "unsat" for value in result["set_checks"].values())
