from pathlib import Path

from .audit_r3_root_star_different_source_leaf_liquidation import run


def test_r3_root_star_different_source_leaf_liquidation():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "DIFFERENT_SOURCE_REDUCED_TO_TWO_TARGETS_OR_RECRUITMENT"
    assert len(result["symmetric_cases"]) == 4
    assert all(result["checks"].values())
