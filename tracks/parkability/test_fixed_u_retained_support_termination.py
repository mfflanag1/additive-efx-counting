import json
from pathlib import Path

from .audit_fixed_u_retained_support_termination import run


ROOT = Path(__file__).resolve().parents[2]


def test_fixed_u_termination_replays() -> None:
    expected = json.loads(
        (ROOT / "results/fixed_u_retained_support_termination_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_fixed_u_termination_boundary() -> None:
    result = run(ROOT)
    assert result["status"] == "RANK_THREE_REPEAT_GATE_OPEN"
    assert all(result["checks"].values())
    assert "rank-three repeat" in result["claim_boundary"]
