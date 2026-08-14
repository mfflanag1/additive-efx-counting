import json
from pathlib import Path

from .audit_four_edge_surplus_star_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_surplus_star_selector_replays_exactly():
    expected = json.loads(Path(
        "results/four_edge_surplus_star_selector_audit.json"
    ).read_text())
    actual = run(ROOT)
    assert actual == expected
    assert all(actual["checks"].values())
