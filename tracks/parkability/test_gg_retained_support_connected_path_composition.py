import json
from pathlib import Path

from .audit_gg_retained_support_connected_path_composition import run


ROOT = Path(__file__).resolve().parents[2]


def test_gg_connected_path_composition_replays():
    expected = json.loads(
        (ROOT / "results/gg_retained_support_connected_path_composition_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_gg_connected_path_dependencies_are_replayable():
    result = run(ROOT)
    assert result["status"] == "DEPENDENCIES_REPLAYABLE"
    assert result["dependency_count"] == 42
