from pathlib import Path

from .audit_root_anchored_one_head_two_hole_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_anchored_one_head_selector_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "ROOT_FACING_ONE_HEAD_REDUCED_TO_TWO_HOLE_OR_CRITICAL_GOOD"
    assert result["original_partition_feasible"]
    assert result["permanent_anchor_retained_by_selector"]
    assert result["outside_anchor_move_forces_root_criticality"]
    assert result["mutual_hole_walls_excluded"]


def test_root_anchored_one_head_selector_has_only_named_certificates() -> None:
    result = run(ROOT)
    assert result["surviving_certificates"] == [
        "anchor-critical least good",
        "root-floor-critical least good",
        "root-EFX-critical least good",
    ]

