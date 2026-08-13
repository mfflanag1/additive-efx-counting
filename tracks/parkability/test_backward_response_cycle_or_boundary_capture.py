from pathlib import Path

from .audit_backward_response_cycle_or_boundary_capture import run


ROOT = Path(__file__).resolve().parents[2]


def test_backward_response_identity_partition() -> None:
    result = run(ROOT)
    assert result["status"] == "BACKWARD_RESPONSE_REDUCED_TO_DECORATED_HEAD_EXCHANGE"
    assert result["anchored_path_count"] == 6
    assert result["backward_order_count"] == 36
    assert result["identity_class_counts"] == {
        "generic_nonhole_boundary_split": 10,
        "nonhole_anchor_source_release": 2,
        "nonhole_anchor_target_collision": 6,
        "owner_hole_cycle": 18,
    }


def test_backward_capture_algebra() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
    assert result["smallest_terminal"] == "GG-recurrent decorated-head exchange"
