import json
from pathlib import Path

from .audit_closed_disjoint_desired_core_pi_capture import audit


ROOT = Path(__file__).resolve().parents[2]


def test_closed_disjoint_desired_core_pi_capture_replays():
    expected = json.loads((
        ROOT / "results" / "closed_disjoint_desired_core_pi_capture_audit.json"
    ).read_text())
    assert audit() == expected
