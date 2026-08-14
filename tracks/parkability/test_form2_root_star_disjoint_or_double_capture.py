from pathlib import Path

from .audit_form2_root_star_disjoint_or_double_capture import run


def test_form2_root_star_frontier():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "DISJOINT_ROOT_STAR_OR_DOUBLE_MARGIN_CAPTURE"
    assert len(result["support_edges"]) == 3
