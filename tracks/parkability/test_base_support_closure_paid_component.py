import json
from pathlib import Path

from .audit_base_support_closure_paid_component import audit


ROOT = Path(__file__).parents[2]


def test_base_support_closure_paid_component_audit_replays():
    expected = json.loads((
        ROOT / "results" / "base_support_closure_paid_component_audit.json"
    ).read_text())
    assert audit() == expected
    assert expected["status"] == "BASE_SUPPORT_CLOSURE_PAID_COMPONENT_VERIFIED"
    assert all(expected["checks"].values())
