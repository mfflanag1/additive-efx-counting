import json
from pathlib import Path

from .audit_joint_packet_maximal_lex_donation_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_joint_packet_maximal_donation_replays():
    expected = json.loads(
        (ROOT / "results/joint_packet_maximal_lex_donation_frontier_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_joint_packet_maximal_donation_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
