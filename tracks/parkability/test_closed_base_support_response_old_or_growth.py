import json
from pathlib import Path

from .audit_closed_base_support_response_old_or_growth import audit


ROOT = Path(__file__).parents[2]


def test_closed_base_support_response_old_or_growth_replays():
    expected = json.loads((
        ROOT / "results" / "closed_base_support_response_old_or_growth_audit.json"
    ).read_text())
    assert audit() == expected
    assert expected["status"] == "CLOSED_RESPONSE_OLD_OR_GROWTH_VERIFIED"
    assert all(expected["checks"].values())
