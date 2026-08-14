import json
from pathlib import Path

from .audit_pi_free_desired_core_support_drainage import audit


ROOT = Path(__file__).resolve().parents[2]


def test_pi_free_desired_core_support_drainage_replays():
    expected = json.loads((
        ROOT / "results" / "pi_free_desired_core_support_drainage_audit.json"
    ).read_text())
    assert audit() == expected
