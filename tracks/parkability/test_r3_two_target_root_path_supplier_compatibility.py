from pathlib import Path

from .audit_r3_two_target_root_path_supplier_compatibility import run


def test_r3_two_target_root_path_supplier_compatibility():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FAVORABLE_ROOT_PATH_HAS_FOUR_EDGE_CANDIDATE"
    assert result["matching_count"] == 3
    assert all(result["checks"].values())
