from pathlib import Path

from .audit_safe_center_three_offer_priority_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_safe_center_three_offer_priority_split_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "STAR_ROUTES_TO_ROOT_PRICE_OR_EXISTING_EXTERNAL_STAR"
    )
    assert result["nonroot_center_root_holder_price_identity"]
    assert result["root_center_offer_strict_over_base"]
    assert result["routes"]["center_not_root"] == [
        "root_holder_price", "two_core_two_hole"
    ]
    assert result["routes"]["center_is_root"] == [
        "retired_collision_normalization",
        "EFX",
        "one_core_three_hole_external_star",
    ]
    assert not result["full_T_L_times_theorem_closed"]
