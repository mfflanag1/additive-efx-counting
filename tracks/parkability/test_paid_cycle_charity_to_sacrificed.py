import json
from pathlib import Path

from .audit_paid_cycle_charity_to_sacrificed import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_cycle_charity_to_sacrificed_replays_exactly():
    expected = json.loads(Path(
        "results/paid_cycle_charity_to_sacrificed_audit.json"
    ).read_text())
    actual = run(ROOT)
    assert actual == expected
    assert all(all(record["checks"].values()) for record in actual["records"])
