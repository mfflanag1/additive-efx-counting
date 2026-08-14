from pathlib import Path

from .audit_root_facing_anchor_surplus_band import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_facing_anchor_surplus_band_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "ROOT_FACING_SURVIVOR_REDUCED_TO_CLOSED_SURPLUS_BAND"
    assert result["trichotomy_exhaustive"]
    assert result["complement_paid_below_delta"]
    assert result["band_blocks_complement_strictness"]
    assert result["band_blocks_root_reselection"]
    assert result["root_above_twice_base_closes_band"]
    assert result["surviving_band"] == "delta <= v_r(D) <= x"
    assert not result["full_T_L_times_theorem_closed"]

