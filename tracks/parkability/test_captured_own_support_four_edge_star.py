import json
from pathlib import Path

from .audit_captured_own_support_four_edge_star import run


ROOT = Path(__file__).resolve().parents[2]


def test_captured_support_star_replays_exactly():
    expected = json.loads(Path(
        "results/captured_own_support_four_edge_star_audit.json"
    ).read_text())
    actual = run(ROOT)
    assert actual == expected
    assert all(actual["checks"].values())
