import json
from pathlib import Path

from .audit_fixed_u_arbitrary_hole_residual_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_fixed_u_arbitrary_hole_residual_selector_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_arbitrary_hole_residual_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_fixed_u_arbitrary_hole_residual_selector_is_composed():
    result = run(ROOT)
    assert result["status"] == "DEPENDENCIES_REPLAYABLE"
    assert result["dependency_count"] == 5
