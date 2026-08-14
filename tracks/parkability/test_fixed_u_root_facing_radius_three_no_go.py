import json
from pathlib import Path

from .audit_fixed_u_root_facing_radius_three_no_go import audit


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/fixed_u_rank_three_root_facing_cegar.json"


def test_root_facing_no_go_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_rank_three_root_facing_no_go_audit.json").read_text()
    )
    assert audit(SOURCE, 13) == expected


def test_root_facing_no_go_boundary():
    result = audit(SOURCE, 13)
    assert result["status"] == "ROOT_FACING_RADIUS_THREE_SELECTOR_REFUTED"
    assert result["efx_lex_escapes_by_exact_radius"] == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 44,
    }
    assert result["recorded_menu_matches_exact_radius_four_set"]
    assert all(result["checks"].values())
    assert "cap-free four-packet exchange" in result["claim_boundary"]
