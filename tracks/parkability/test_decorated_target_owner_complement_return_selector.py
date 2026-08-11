import json
from pathlib import Path

from .audit_decorated_target_owner_complement_return_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_decorated_target_owner_complement_return_selector_replays():
    expected = json.loads(
        (ROOT / "results/decorated_target_owner_complement_return_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_decorated_target_owner_complement_return_selector_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["selector_family_nonempty"]
    assert len(result["smallest_remaining_operations"]) == 3
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
