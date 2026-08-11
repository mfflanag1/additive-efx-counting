import json
from pathlib import Path

from .audit_arbitrary_charity_packet_blocker_collapse import run


ROOT = Path(__file__).resolve().parents[2]


def test_arbitrary_charity_packet_blocker_collapse_replays():
    expected = json.loads(
        (ROOT / "results/arbitrary_charity_packet_blocker_collapse_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_arbitrary_charity_packet_blocker_collapse_forces_singleton():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["final_charity_is_singleton"]
    assert result["connected_exchange"]
    assert result["singleton_walk_dependency"]["audit_status"] == "ALL_FORCED"
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
