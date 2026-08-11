import json
from pathlib import Path

from .audit_current_safe_full_response_matching_endpoint import run


ROOT = Path(__file__).resolve().parents[2]


def test_current_safe_full_response_matching_endpoint_replays():
    expected = json.loads(
        (ROOT / "results/current_safe_full_response_matching_endpoint_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_current_safe_full_response_matching_endpoint_forces_all_checks():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
