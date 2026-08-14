from pathlib import Path

from .audit_form2_qd_swap_root_response_payment import run


def test_form2_qd_swap_root_response_payment():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "PAID_FOUR_EDGE_SWAP_OR_ROOT_Q_SEPARATORS"
    assert len(result["support_edges"]) == 4
