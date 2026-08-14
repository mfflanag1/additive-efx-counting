import json
from pathlib import Path

from .audit_fixed_u_rank_three_relation_no_go import audit


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/fixed_u_rank_three_relation_cegar_v3.json"


def test_rank_gated_radius_three_no_go_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_rank_three_relation_no_go_audit.json").read_text()
    )
    assert audit(SOURCE, 4) == expected


def test_rank_gated_claim_boundary():
    result = audit(SOURCE, 4)
    assert result["status"] == "RANK_GATED_RADIUS_THREE_SELECTOR_REFUTED"
    assert result["response_ranks"] == {
        "support": {"ordinary": 3, "current": 3, "mixed": 3},
        "split": {"ordinary": 3, "current": 2, "mixed": 3},
        "reassembly": {"ordinary": 3, "current": 3, "mixed": 3},
    }
    assert result["efx_lex_escapes_by_exact_radius"] == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 31,
    }
    assert result["recorded_menu_matches_exact_radius_four_set"]
    assert "signed-repeat reachability" in result["claim_boundary"]
