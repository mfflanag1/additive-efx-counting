from pathlib import Path

from .audit_form2_six_branch_payment_compression import run


def test_form2_six_branch_payment_compression():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "SIX_FAILURES_IFF_THREE_SUPPLIER_CAPTURES"
    assert len(result["branches"]) == 6
    assert all(len(row["support_edges"]) == 4 for row in result["branches"])
