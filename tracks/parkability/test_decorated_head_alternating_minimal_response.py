from pathlib import Path

from .audit_decorated_head_alternating_minimal_response import run


ROOT = Path(__file__).resolve().parents[2]


def test_every_wall_gets_candidate_safe_head_response() -> None:
    result = run(ROOT)
    assert result["status"] == "EVERY_WALL_HAS_CANDIDATE_SAFE_ONE_OR_TWO_HEAD_RESPONSE"
    assert result["head_bound"] == 2
    assert result["strict_support_descent"] is True
    assert all(result["symbolic_checks"].values())


def test_alternating_cross_head_extraction_strictly_descends() -> None:
    result = run(ROOT)
    assert len(result["finite_state_records"]) == 16
    assert all(record["termination_forced"] for record in result["finite_state_records"])
    assert all(
        record["maximum_cross_head_handoffs"]
        == record["initial_support_size"] - 1
        for record in result["finite_state_records"]
    )
