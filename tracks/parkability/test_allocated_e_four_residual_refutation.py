import json
from pathlib import Path

from .audit_allocated_e_four_residual_refutation import audit


ROOT = Path(__file__).resolve().parents[2]


def test_allocated_e_four_residual_refutation_replays():
    expected = json.loads((
        ROOT / "results" / "allocated_e_four_residual_refutation_audit.json"
    ).read_text())
    assert audit() == expected
