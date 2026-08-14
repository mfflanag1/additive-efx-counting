from pathlib import Path

from .audit_form2_q_compensation_path_packet import run


def test_form2_q_compensation_path_packet():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "PAID_THREE_EDGE_PATH_OR_BICRITERIA_PACKET"
    assert len(result["support_edges"]) == 3
    assert result["minimal_packet_calibrations_checked"] > 0
