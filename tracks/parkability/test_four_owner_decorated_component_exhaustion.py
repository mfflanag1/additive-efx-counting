import json
from pathlib import Path

from .audit_four_owner_decorated_component_exhaustion import run


ROOT = Path(__file__).resolve().parents[2]


def test_four_owner_decorated_component_exhaustion_replays():
    expected = json.loads(
        (ROOT / "results/four_owner_decorated_component_exhaustion_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_four_owner_decorated_component_exhaustion_is_complete():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["violations"] == []
    assert result["maximum_outside_owners_before_recruitment"] == 1
    assert result["outside_recruitments_before_full_union"] == 1
