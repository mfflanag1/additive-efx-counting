import json
from pathlib import Path

from .audit_root_concentration_bottom_absorption_rotation import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_concentration_bottom_absorption_rotation_replays():
    expected = json.loads(
        (ROOT / "results/root_concentration_bottom_absorption_rotation_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_root_concentration_bottom_absorption_rotation_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["potential_update"] == "V <- V union H"
