from pathlib import Path

from .audit_safe_center_three_offer_return_or_rejection import run


ROOT = Path(__file__).resolve().parents[2]


def test_safe_center_three_offer_return_or_rejection_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "SAFE_CENTER_STAR_ENTERS_TWO_HOLE_OR_THREE_ROW_REJECTION"
    )
    assert result["center_pays_safe_return_bundle"]
    assert result["leaf_pays_floor_and_offer"]
    assert result["return_or_rejection_exhaustive"]
    assert not result["full_T_L_times_theorem_closed"]

