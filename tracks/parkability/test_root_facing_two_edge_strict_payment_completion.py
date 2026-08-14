import json
from pathlib import Path

from .audit_root_facing_two_edge_strict_payment_completion import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_facing_two_edge_payment_replays_exactly():
    expected = json.loads(Path(
        "results/root_facing_two_edge_strict_payment_completion_audit.json"
    ).read_text())
    actual = run(ROOT)
    assert actual == expected
    assert all(actual["checks"].values())
