import json
from pathlib import Path

from .audit_global_residual_root_facing_rigidity import run


ROOT = Path(__file__).resolve().parents[2]


def test_global_residual_root_facing_rigidity_replays():
    expected = json.loads(
        (ROOT / "results/global_residual_root_facing_rigidity_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_global_residual_root_facing_rigidity_is_composed():
    result = run(ROOT)
    assert result["status"] == "DEPENDENCIES_REPLAYABLE"
    assert result["dependency_count"] == 4
    assert result["terminal_supports"] == ["top packet", "f-only captured bottom"]
