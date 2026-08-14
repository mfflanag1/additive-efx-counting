from pathlib import Path

from .audit_ledger_normalized_root_external_star_ascent_or_price import run


ROOT = Path(__file__).resolve().parents[2]


def test_ledger_normalized_root_external_star_ascent_or_price_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "EXTERNAL_STAR_SIGNS_ROUTE_TO_ASCENT_RANK_OR_ROOT_PRICE"
    )
    assert result["root_to_hole_strict_ascent"]
    assert result["hole_to_root_trichotomy"]
    assert result["controlled_release_below_delta"]
    assert result["band_price_nonnegative_and_bounded"]
    assert result["proper_subcore_not_current_root_desired"]
    assert result["remaining_separator"] == "retired collision / holder price"
    assert not result["full_T_L_times_theorem_closed"]

