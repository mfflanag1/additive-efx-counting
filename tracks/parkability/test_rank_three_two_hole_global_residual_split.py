import json
from pathlib import Path

from .audit_rank_three_two_hole_global_residual_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_rank_three_global_residual_split_replays() -> None:
    expected = json.loads(
        (ROOT / "results/rank_three_two_hole_global_residual_split_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_rank_three_global_residual_split_boundary() -> None:
    result = run(ROOT)
    assert result["status"] == "ALL_RESIDUAL_CHARITY_SPLITS_CLASSIFIED"
    assert all(result["checks"].values())
    assert "capture return" in result["claim_boundary"]
