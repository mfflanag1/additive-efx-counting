import json
from pathlib import Path

from .audit_fixed_u_support_edge_three_no_go import audit


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/fixed_u_rank_three_root_facing_support_edge_cegar.json"


def test_support_edge_three_no_go_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_support_edge_three_no_go_audit.json").read_text()
    )
    assert audit(SOURCE, 1) == expected


def test_support_edge_bound_is_sharp_in_declared_cell():
    result = audit(SOURCE, 1)
    assert result["status"] == "SUPPORT_EDGE_BOUND_THREE_REFUTED"
    assert result["complete_efx_by_exact_edge_count"] == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 33,
    }
    assert result["recorded_four_edge_menu_size"] == 33
    assert all(result["checks"].values())
