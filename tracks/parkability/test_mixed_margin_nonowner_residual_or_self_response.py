import json
from pathlib import Path

from .audit_mixed_margin_nonowner_residual_or_self_response import run


ROOT = Path(__file__).resolve().parents[2]


def test_mixed_margin_nonowner_residual_or_self_response_replays():
    expected = json.loads(
        (ROOT / "results/mixed_margin_nonowner_residual_or_self_response_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_mixed_margin_nonowner_residual_or_self_response_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["outcomes"]) == 3
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
