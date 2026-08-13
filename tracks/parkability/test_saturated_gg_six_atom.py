import json
from pathlib import Path

from .audit_saturated_gg_six_atom import run as audit
from .decide_saturated_gg_six_atom import run as decide


ROOT = Path(__file__).resolve().parents[2]


def test_six_atom_decision_replays_exactly() -> None:
    expected = json.loads((ROOT / "results/saturated_gg_six_atom_decision.json").read_text())
    assert decide(ROOT) == expected


def test_six_atom_independent_audit_replays_exactly() -> None:
    expected = json.loads((ROOT / "results/saturated_gg_six_atom_audit.json").read_text())
    assert audit(ROOT) == expected


def test_six_atom_claim_boundary_is_bounded() -> None:
    result = json.loads((ROOT / "results/saturated_gg_six_atom_decision.json").read_text())
    assert result["status"] == "UNSAT_SIX_ATOM_SEPARATOR"
    assert result["allocation_count"] == 15625
    assert "not cap-free" in result["claim_boundary"]
    assert set(result["deletion_minimal_group_core"]) == {
        "positive_normalized",
        "current_payment",
        "response_saturation",
        "global_lex_all_allocations",
    }
