import json
from pathlib import Path

from .audit_joint_packet_external_sink_rerouting import run


ROOT = Path(__file__).resolve().parents[2]


def test_joint_packet_external_sink_rerouting_replays():
    expected = json.loads(
        (ROOT / "results/joint_packet_external_sink_rerouting_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_joint_packet_external_sink_rerouting_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
