import json
from pathlib import Path

from .audit_generalized_self_pi_exclusion import audit


ROOT = Path(__file__).resolve().parents[2]


def test_generalized_self_pi_exclusion_replays():
    expected = json.loads((
        ROOT / "results" / "generalized_self_pi_exclusion_audit.json"
    ).read_text())
    assert audit() == expected
