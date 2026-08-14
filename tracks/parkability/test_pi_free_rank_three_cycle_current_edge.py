import json
from pathlib import Path

from .audit_pi_free_rank_three_cycle_current_edge import audit


ROOT = Path(__file__).parents[2]


def test_pi_free_rank_three_cycle_current_edge_replays():
    expected = json.loads((
        ROOT / "results" / "pi_free_rank_three_cycle_current_edge_audit.json"
    ).read_text())
    assert audit() == expected
    assert expected["status"] == "PI_FREE_CYCLE_CURRENT_EDGE_VERIFIED"
    assert all(expected["checks"].values())
