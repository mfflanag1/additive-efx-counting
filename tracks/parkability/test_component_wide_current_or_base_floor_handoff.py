import json
from pathlib import Path

from .audit_component_wide_current_or_base_floor_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_component_wide_current_or_base_floor_replays():
    expected = json.loads(
        (ROOT / "results/component_wide_current_or_base_floor_handoff_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_component_wide_current_or_base_floor_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 3
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
