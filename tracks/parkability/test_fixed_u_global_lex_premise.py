import json
from pathlib import Path

from .audit_fixed_u_global_lex_premise import run


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/fixed_u_charity_tree_countermodel.json"


def test_fixed_u_global_lex_premise_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_global_lex_premise_audit.json").read_text()
    )
    assert run(SOURCE) == expected


def test_fixed_u_global_lex_premise_is_decided_exactly():
    result = run(SOURCE)
    assert result["status"] in {"GLOBAL_LEX_COUNTERMODEL", "BASE_EXCLUDED"}
    if result["status"] == "BASE_EXCLUDED":
        assert result["lex_improving_allocation"] is not None
        assert result["first_improver"] is not None
        assert result["strict_pareto_witness_available"]
        assert result["all_agents_strict"]
        assert result["charity_exchange"]
        assert result["single_connected_transfer_component"]
    else:
        assert result["solver_status"] == "unsat"
