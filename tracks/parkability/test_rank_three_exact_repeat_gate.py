import json
from pathlib import Path

from .audit_rank_three_exact_repeat_gate import run


ROOT = Path(__file__).resolve().parents[2]


def test_rank_three_gate_replays_exactly() -> None:
    expected = json.loads(
        (ROOT / "results/rank_three_exact_repeat_gate_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_rank_three_gate_claim_boundary() -> None:
    result = run(ROOT)
    assert result["status"] == "RANK_THREE_TWO_HOLE_OBSTRUCTION_EXISTS"
    assert all(result["checks"].values())
    assert not result["witness"]["rational_response_realization"]["full_GG_countermodel"]
