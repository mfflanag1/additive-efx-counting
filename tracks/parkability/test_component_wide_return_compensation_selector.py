import json
from pathlib import Path

from .audit_component_wide_return_compensation_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_component_wide_return_compensation_replays():
    expected = json.loads(
        (ROOT / "results/component_wide_return_compensation_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_component_wide_return_compensation_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 2
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
    assert all(value == "unsat" for value in result["graph_checks"].values())
