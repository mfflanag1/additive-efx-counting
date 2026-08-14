import json
from pathlib import Path

from .audit_rank_three_pi_free_crossed_provenance_import import audit


ROOT = Path(__file__).resolve().parents[2]


def test_rank_three_pi_free_crossed_provenance_import_replays():
    expected = json.loads((
        ROOT / "results" / "rank_three_pi_free_crossed_provenance_import_audit.json"
    ).read_text())
    assert audit() == expected
