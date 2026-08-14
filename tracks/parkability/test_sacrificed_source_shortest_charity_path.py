import json
from pathlib import Path

from .audit_sacrificed_source_shortest_charity_path import run


ROOT = Path(__file__).resolve().parents[2]


def test_shortest_charity_path_replays_exactly():
    expected = json.loads(Path(
        "results/sacrificed_source_shortest_charity_path_audit.json"
    ).read_text())
    actual = run(ROOT)
    assert actual == expected
    assert len(actual["records"]) == 4
    assert all(all(record["checks"].values()) for record in actual["records"])
