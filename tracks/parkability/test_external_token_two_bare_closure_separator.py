import json
from pathlib import Path

from .audit_external_token_two_bare_closure_separator import audit


ROOT = Path(__file__).parents[2]


def test_external_token_two_bare_closure_separator_replays():
    expected = json.loads((
        ROOT / "results" / "external_token_two_bare_closure_separator_audit.json"
    ).read_text())
    assert audit() == expected
    assert expected["status"] == "WITHDRAWN_PI_INFERENCE"
    assert all(expected["checks"].values())
